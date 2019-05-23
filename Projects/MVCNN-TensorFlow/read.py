import numpy as np
import tensorflow as tf
from tensorflow.contrib.slim.nets import resnet_v2

resNet101path = "/Volumes/OTHERS/superuser/ResNet101.npy"
alexNetpath = "/Volumes/MacMisc/Machine-Learning/Projects/MVCNN-TensorFlow/alexnet_imagenet.npy"

params = np.load(alexNetpath, encoding="latin1")
# print(params)
for name in params.item().keys():
    print(name)
print(len(params.item().keys()))
