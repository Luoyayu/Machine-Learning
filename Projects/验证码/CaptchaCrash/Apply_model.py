from sklearn import preprocessing
from sklearn import tree
import numpy as np
import tensorflow as tf
import os
# 特征矩阵
featureList = [[1, 0], [1, 1], [0, 0], [0, 1]]
# 标签矩阵
labelList = ['a', 'b', 'c', 'a']
# 标签二进制化
print(preprocessing.LabelBinarizer().fit_transform(labelList))
# classifier = tf.estimator.LinearClassifier()

