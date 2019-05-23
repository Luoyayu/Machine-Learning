import tensorflow, keras, torch, sklearn
import numpy, scipy, pandas
import matplotlib
import matplotlib.pylab as plt
import cv2, PIL
import IPython, jupyterlab
from termcolor import cprint

import os, sys

colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
def c(modules):
    for i, module in enumerate(modules):
        cprint("%-20s%-20s" % (module.__name__, module.__version__), color=colors[i%len(colors)], attrs=['bold'])

import_modules = [
        tensorflow, keras, torch, sklearn,
        numpy, scipy, pandas,
        matplotlib,
        cv2, PIL,
        IPython, jupyterlab
        ]
c(import_modules)
cprint("sys platform: "+sys.platform, color='red', attrs=['blink'])
cprint(str(sys.version_info), color='green', attrs=['blink'])

