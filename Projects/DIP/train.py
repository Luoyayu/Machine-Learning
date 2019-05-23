from __future__ import print_function
import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
from torch.autograd import Variable

from model import _netlocalD, _netG

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default='streetview', help='cifar10 | lsun | imagenet | folder | lfw ')
parser.add_argument('--dataroot', default='dataset/train', help='path to dataset')
parser.add_argument('--workers', type=int, help='number of data loading workers', default=2)
parser.add_argument('--batchSize', type=int, default=64, help='input batch size')
parser.add_argument('--imageSize', type=int, default=128, help='the height / width of the input image to network')

parser.add_argument('--nz', type=int, default=100, help='size of the latent z vector')
parser.add_argument('--ngf', type=int, default=64)
parser.add_argument('--ndf', type=int, default=64)
parser.add_argument('--nc', type=int, default=3)
parser.add_argument('--niter', type=int, default=25, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.0002, help='learning rate, default=0.0002')
parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. default=0.5')
parser.add_argument('--cuda', action='store_true', help='enables cuda')
parser.add_argument('--ngpu', type=int, default=1, help='number of GPUs to use')
parser.add_argument('--netG', default='', help="path to netG (to continue training)")
parser.add_argument('--netD', default='', help="path to netD (to continue training)")
parser.add_argument('--outf', default='.', help='folder to output images and model checkpoints')
parser.add_argument('--manualSeed', type=int, help='manual seed')

parser.add_argument('--nBottleneck', type=int, default=4000, help='of dim for bottleneck of encoder')
parser.add_argument('--overlapPred', type=int, default=4, help='overlapping edges')
parser.add_argument('--nef', type=int, default=64, help='of encoder filters in first conv layer')
parser.add_argument('--wtl2', type=float, default=0.998, help='0 means do not use else use with this weight')
parser.add_argument('--wtlD', type=float, default=0.001, help='0 means do not use else use with this weight')

# 解析命令行参数
opt = parser.parse_args()
print(opt)

# 创建工作文件夹
try:
    os.makedirs("result/train/cropped")
    os.makedirs("result/train/real")
    os.makedirs("result/train/recon")
    os.makedirs("model")
except OSError:
    pass

# 设置种子
if opt.manualSeed is None:
    opt.manualSeed = random.randint(1, 10000)
print("Random Seed: ", opt.manualSeed)
random.seed(opt.manualSeed)
torch.manual_seed(opt.manualSeed)
# 为GPU设置种子
if opt.cuda:
    torch.cuda.manual_seed_all(opt.manualSeed)

# 开启非确定性算法优化器
cudnn.benchmark = True

# 提示开启GPU支持
if torch.cuda.is_available() and not opt.cuda:
    print("WARNING: You have a CUDA device, so you should probably run with --cuda")

# 预处理街景数据集
if opt.dataset in ['folder', 'street_view']:
    # folder dataset 普通文件夹
    dataset = dset.ImageFolder(root=opt.dataroot,
                               transform=transforms.Compose([
                                   transforms.Resize(opt.imageSize),
                                   transforms.CenterCrop(opt.imageSize),
                                   transforms.ToTensor(),
                                   transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                               ]))

elif opt.dataset == 'street_view':  # 街景数据
    transform = transforms.Compose([transforms.Resize(opt.imageSize),
                                    transforms.CenterCrop(opt.imageSize),
                                    transforms.ToTensor(),
                                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    dataset = dset.ImageFolder(root=opt.dataroot, transform=transform)

assert dataset
dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batchSize,
                                         shuffle=True, num_workers=int(opt.workers))

ngpu = int(opt.ngpu)
nz = int(opt.nz)  # # 潜在随机z向量长度 100
ngf = int(opt.ngf)  # 生成器/编码器 第一层滤波器个数 64
ndf = int(opt.ndf)  # 判别器第一层滤波器个数 64
nc = 3  # 输入图像维度
nef = int(opt.nef)  # 编码器滤第一层滤波器个数
nBottleneck = int(opt.nBottleneck)  # 瓶颈层层数4000
wtl2 = float(opt.wtl2)
overlapL2Weight = 10


# custom weights initialization called on netG and netD
def weights_init(m):
    class_name = m.__class__.__name__
    if class_name.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)  # mean variance
    elif class_name.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


# 恢复到指定 epoch
resume_epoch = 0

netG = _netG(opt)  # 编码器+判别器网络
netG.apply(weights_init)  # 初始化权重

if opt.netG != '':  # 可选导入模型
    netG.load_state_dict(torch.load(opt.netG, map_location=lambda storage, location: storage)['state_dict'])
    resume_epoch = torch.load(opt.netG)['epoch']

print(netG)

netD = _netlocalD(opt)  # 判别器网络
netD.apply(weights_init)  # 初始化判别器

if opt.netD != '':  # 可选导入模型
    netD.load_state_dict(torch.load(opt.netD, map_location=lambda storage, location: storage)['state_dict'])
    resume_epoch = torch.load(opt.netD)['epoch']

print(netD)

criterion = nn.BCELoss()  # Binary Cross Entropy
criterionMSE = nn.MSELoss()  # squared L2 norm

input_real = torch.Tensor(opt.batchSize, 3, opt.imageSize, opt.imageSize)  # 输入真实图像
input_cropped = torch.Tensor(opt.batchSize, 3, opt.imageSize, opt.imageSize)  # 遮挡图像
label = torch.Tensor(opt.batchSize)  # 标签数量
real_label = 1  # 真实图像标签
fake_label = 0  # 构造图像标签

real_center = torch.Tensor(opt.batchSize, 3, opt.imageSize / 2, opt.imageSize / 2)  # 真实图像取半大小

if opt.cuda:  # Tensor 放置于GPU上
    netD.cuda()
    netG.cuda()
    criterion.cuda()
    criterionMSE.cuda()
    input_real, input_cropped, label = input_real.cuda(), input_cropped.cuda(), label.cuda()
    real_center = real_center.cuda()

input_real = Variable(input_real)
input_cropped = Variable(input_cropped)
label = Variable(label)
real_center = Variable(real_center)

# setup optimizer
optimizerD = optim.Adam(netD.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))  # 判别器Adam优化器
optimizerG = optim.Adam(netG.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))  # 生成器Adam优化器

for epoch in range(resume_epoch, opt.niter):  # 训练
    for i, data in enumerate(dataloader, 0):
        real_cpu, _ = data  # real_cpu 原始图像
        real_center_cpu = real_cpu[:, :,
                          int(opt.imageSize / 4):int(opt.imageSize / 4) + int(opt.imageSize / 2),
                          int(opt.imageSize / 4):int(opt.imageSize / 4) + int(opt.imageSize / 2)
                          ]

        batch_size = real_cpu.size(0)
        input_real.data.resize_(real_cpu.size()).copy_(real_cpu)
        input_cropped.data.resize_(real_cpu.size()).copy_(real_cpu)
        real_center.data.resize_(real_center_cpu.size()).copy_(real_center_cpu)  # 真实图像中间遮挡部分

        # 在原图上填充色块
        input_cropped.data[:, 0,
        int(opt.imageSize / 4 + opt.overlapPred):int(opt.imageSize / 4 + opt.imageSize / 2 - opt.overlapPred),
        int(opt.imageSize / 4 + opt.overlapPred):int(opt.imageSize / 4 + opt.imageSize / 2 - opt.overlapPred)
        ] = 2 * 117.0 / 255.0 - 1.0

        input_cropped.data[:, 1,
        int(opt.imageSize / 4 + opt.overlapPred):int(opt.imageSize / 4 + opt.imageSize / 2 - opt.overlapPred),
        int(opt.imageSize / 4 + opt.overlapPred):int(opt.imageSize / 4 + opt.imageSize / 2 - opt.overlapPred)
        ] = 2 * 104.0 / 255.0 - 1.0

        input_cropped.data[:, 2,
        int(opt.imageSize / 4 + opt.overlapPred):int(opt.imageSize / 4 + opt.imageSize / 2 - opt.overlapPred),
        int(opt.imageSize / 4 + opt.overlapPred):int(opt.imageSize / 4 + opt.imageSize / 2 - opt.overlapPred)
        ] = 2 * 123.0 / 255.0 - 1.0

        # train with real
        netD.zero_grad()  # 清除累计梯度
        label.data.resize_(batch_size).fill_(real_label)  # 填充真实标签

        output = netD(real_center)  # 判别真实中心遮挡图像
        errD_real = criterion(output, label)  # 计算二分类误差
        errD_real.backward()  # 将二分类误差反向传播
        D_x = output.data.mean()  # 判别误差Dx

        # train with fake
        # noise.data.resize_(batch_size, nz, 1, 1)
        # noise.data.normal_(0, 1)
        fake = netG(input_cropped)  # 有遮挡图像生成64*64
        label.data.fill_(fake_label)  # 填充标签
        output = netD(fake.detach())  # 判别生成图片
        errD_fake = criterion(output, label)  # 计算二分类误差
        errD_fake.backward()  # 反向传播二分类误差
        D_G_z1 = output.data.mean()  # 计算判别器误差D(G(z)), z是潜在向量
        errD = errD_real + errD_fake  # 综合误差
        optimizerD.step()  # 优化判别器

        ##############################################
        # (2) Update G network: maximize log(D(G(z)))
        ##############################################
        netG.zero_grad()  # 清空生成器累计梯度
        label.data.fill_(real_label)  # fake labels are real for generator cost
        output = netD(fake)
        errG_D = criterion(output, label)
        # errG_D.backward(retain_variables=True)

        # errG_l2 = criterionMSE(fake,real_center)
        wtl2Matrix = real_center.clone()
        wtl2Matrix.data.fill_(wtl2 * overlapL2Weight)
        wtl2Matrix.data[:, :, int(opt.overlapPred):int(opt.imageSize / 2 - opt.overlapPred),
        int(opt.overlapPred):int(opt.imageSize / 2 - opt.overlapPred)] = wtl2

        errG_l2 = (fake - real_center).pow(2)
        errG_l2 = errG_l2 * wtl2Matrix
        errG_l2 = errG_l2.mean()

        errG = (1 - wtl2) * errG_D + wtl2 * errG_l2

        errG.backward()

        D_G_z2 = output.data.mean()
        optimizerG.step()

        print('[%d/%d][%d/%d] Loss_D: %.4f Loss_G: %.4f / %.4f l_D(x): %.4f l_D(G(z)): %.4f'
              % (epoch, opt.niter, i, len(dataloader),
                 errD.data[0], errG_D.data[0], errG_l2.data[0], D_x, D_G_z1,))
        if i % 100 == 0:
            vutils.save_image(real_cpu,
                              'result/train/real/real_samples_epoch_%03d.png' % (epoch))
            vutils.save_image(input_cropped.data,
                              'result/train/cropped/cropped_samples_epoch_%03d.png' % (epoch))
            recon_image = input_cropped.clone()  # 修补的生成图像
            recon_image.data[:, :, int(opt.imageSize / 4):int(opt.imageSize / 4 + opt.imageSize / 2),
            int(opt.imageSize / 4):int(opt.imageSize / 4 + opt.imageSize / 2)] = fake.data
            vutils.save_image(recon_image.data,
                              'result/train/recon/recon_center_samples_epoch_%03d.png' % (epoch))

    # do checkpointing
    torch.save({'epoch': epoch + 1,
                'state_dict': netG.state_dict()},
               'model/netG_streetview.pth')
    torch.save({'epoch': epoch + 1,
                'state_dict': netD.state_dict()},
               'model/netlocalD.pth')
