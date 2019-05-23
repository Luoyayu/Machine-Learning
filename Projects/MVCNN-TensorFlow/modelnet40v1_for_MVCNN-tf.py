# author: Tongyu Hu
# date: 2018-10-11
import os
import sys
from subprocess import run, PIPE

ROOT_PATH = "./"
DATA_PATH = "/Volumes/MacMisc/data/" + "modelnet40v1/"
VIEW_PATH = ROOT_PATH + "data/view/"
if not os.path.isdir(VIEW_PATH + '/list/'):
    os.makedirs(VIEW_PATH + '/list/')
contents = os.listdir(DATA_PATH)
try:
    contents.remove('.DS_Store')
except ValueError:
    pass

# 生成空目录
for List in ['train', 'test', 'val']:
    for category in contents:
        try:
            os.makedirs(VIEW_PATH + 'list/' + List + '/' + category)
        except FileExistsError:
            pass
print("类别目录新建完成")

for i, category in enumerate(contents):
    for _, _, files in os.walk(DATA_PATH + category + '/test', topdown=True):
        files_list = set()
        for file in files:
            last_idx = len(file) - file[::-1].find('_') - 1
            file_name = file[:last_idx] + '.off.txt'
            files_list.add(file_name)
        print('类别 %2d 数目:%3d' % (i, len(files_list)), end=" ")
        testF = open(VIEW_PATH + 'test_lists.txt', 'a')
        for x in files_list:
            testF.write(VIEW_PATH + 'list/test/' + category + '/' + x + ' ' + str(i) + '\n')
            F2 = open(VIEW_PATH + 'list/test/' + category + '/' + x, 'w')
            F2.write(str(i) + '\n12\n')
            for j in range(1, 13):
                img_path = DATA_PATH + category + '/test/' + \
                           x[:-8] + '_0' + str(j).zfill(2) + '.jpg'
                if os.path.isfile(img_path):
                    F2.write(img_path + '\n')
                else:
                    print('图片路径构造错误!' + img_path)
                    exit(1)
                    break
            F2.close()
        testF.close()
    print('%-60s 处理完成' % (DATA_PATH + category + '/test/'))

TRAIN_RADIO = 0.7
TRAIN_SIZE = 1.0

for i, category in enumerate(contents):
    for root, dirs, files in os.walk(DATA_PATH + category + '/train', topdown=True):
        files_list = set()
        for file in files:
            last_idx = len(file) - file[::-1].find('_') - 1
            file_name = file[:last_idx] + '.off.txt'
            files_list.add(file_name)
        print('类别 %2d 数目:%3d' % (i, len(files_list)), end=" ")

        trainF = open(VIEW_PATH + 'train_lists.txt', 'a')
        valF = open(VIEW_PATH + 'val_lists.txt', 'a')
        F = [trainF, valF]
        files_list = list(files_list)[:int(len(files_list) * TRAIN_SIZE)]
        for k, x in enumerate(files_list):
            train_or_val = 'train/' if k > len(files_list) * TRAIN_RADIO else 'val/'
            F[train_or_val == 'train/'].write(VIEW_PATH + 'list/' +
                                              train_or_val + category + '/' + x + ' ' + str(i) + '\n')
            F2 = open(VIEW_PATH + 'list/' + train_or_val + category + '/' + x, 'w')
            F2.write(str(i) + '\n12\n')
            for j in range(1, 13):
                img_path = DATA_PATH + category + '/train/' + x[:-8] + '_0' + str(j).zfill(2) + '.jpg'
                if os.path.isfile(img_path):
                    F2.write(img_path + '\n')
                else:
                    print('图片路径构造错误! ' + img_path)
                    exit(1)
                    break
            F2.close()
        trainF.close()
        valF.close()
    print('%-60s 处理完成' % (DATA_PATH + category + '/train/'))
