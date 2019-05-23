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
