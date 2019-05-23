import torch
import torchvision
import numpy as np
import os
import sys
import argparse

import torchvision.transforms as transforms
from torchvision.utils import save_image

from torch.utils.data import DataLoader
from torchvision import datasets

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch

from PIL import Image
from matplotlib import pylab as plt
from termcolor import cprint
from abc import abstractmethod, ABCMeta
from tensorboardX import SummaryWriter

DEBUG = True
debug = lambda x: print((x if DEBUG else ''), end=('\n' if DEBUG else ''))

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
PARSER = None  # global parser
args = None  # global args
img_shape = None


def init_parser():
    global PARSER, args
    PARSER = argparse.ArgumentParser()

    args = PARSER.parse_args()


class ArgsClass:
    def __init__(self):
        self.model_name = 'vanilla gan'
        self.lr = 5e-5
        self.b1 = 0.5  # beta1
        self.b2 = 0.999  # beta2
        self.img_size = 28
        self.channels = 1
        self.epochs = 30
        self.batch_size = 64
        self.latent_dim = 100
        self.cpu_worker = 2
        self.sample_interval = 400


def init_fake_parser():
    global args
    args = ArgsClass()


# 原始 GAN
class G(nn.Module):
    def __init__(self):
        super(G, self).__init__()

        def block(in_features, out_features, normalize=True):
            layers = [nn.Linear(in_features, out_features)]
            if normalize:
                layers.append(nn.BatchNorm1d(out_features, 0.8))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers

        self.model = nn.Sequential(
            *block(args.latent_dim, 128, normalize=False),
            *block(128, 256, normalize=True),
            *block(256, 512, normalize=True),
            *block(512, 1024, normalize=True),
            nn.Linear(1024, int(np.prod(img_shape))),
            nn.Tanh()
        )

    def forward(self, z):
        imgs = self.model(z)
        imgs = imgs.view(imgs.size(0), *img_shape)
        return imgs


class D(nn.Module):
    def __init__(self):
        super(D, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(int(np.prod(img_shape)), 512),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, imgs):
        return self.model(
            imgs.view(imgs.size(0), -1)
        )


def main():
    assert (isinstance(args, ArgsClass))
    os.makedirs('images', exist_ok=True)
    os.makedirs('tf-log', exist_ok=True)
    sum_writer = SummaryWriter('tf-log')
    adversarial_loss = torch.nn.BCELoss().to(DEVICE)
    g = G().to(DEVICE)
    d = D().to(DEVICE)

    os.makedirs('data/mnist', exist_ok=True)
    dataloader = torch.utils.data.DataLoader(
        datasets.MNIST(
            'data/mnist', train=True, download=True,
            transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5], std=[0.5])
            ])
        ), batch_size=args.batch_size, shuffle=True, num_workers=args.cpu_worker
    )
    optimizer_g = optim.Adam(g.parameters(), lr=args.lr, betas=(args.b1, args.b2))
    optimizer_d = optim.Adam(d.parameters(), lr=args.lr, betas=(args.b1, args.b2))

    for epoch in range(args.epochs):
        for i, (imgs, _) in enumerate(dataloader, 0):
            valid = torch.ones((imgs.size(0), 1), dtype=torch.float32, requires_grad=False, device=DEVICE)
            fake = torch.zeros((imgs.size(0), 1), dtype=torch.float32, requires_grad=False, device=DEVICE)

            real_imgs = imgs.to(DEVICE)
            # train generator
            optimizer_g.zero_grad()
            z = torch.normal(mean=0, std=torch.ones((imgs.size(0), args.latent_dim), dtype=torch.float32)).to(DEVICE)
            gen_imgs = g(z)
            g_loss = adversarial_loss(d(gen_imgs.detach()), valid)  # 判别器是生成器的损失函数 p_{data}与p_{g}的分布差异度量
            g_loss.backward()
            optimizer_g.step()

            # train discriminatory
            optimizer_d.zero_grad()
            d_real_loss = adversarial_loss(d(real_imgs), valid)
            d_fake_loss = adversarial_loss(d(gen_imgs.detach()), fake)
            d_loss = (d_real_loss + d_fake_loss) / 2

            d_loss.backward()
            optimizer_d.step()

            if (i + 1) % 300 == 0:
                print('[Epoch %2d/%2d] [Batch %3d/%3d] [D loss: %.5f] [G loss: %.5f]' % (
                    epoch + 1, args.epochs, i + 1, len(dataloader), d_loss.item(), g_loss.item()
                ))

            batches_done = epoch * len(dataloader) + i
            sum_writer.add_scalar('loss/g_loss', g_loss.item(), batches_done)
            sum_writer.add_scalar('loss/d_loss', d_loss.item(), batches_done)

            if batches_done % args.sample_interval == 0:
                save_image(gen_imgs.data[:25], 'images/%d.png' % (batches_done), nrow=5, normalize=True)


if __name__ == '__main__':
    init_fake_parser()
    img_shape = (args.channels, args.img_size, args.img_size)
    # global DEBUG

    main()
