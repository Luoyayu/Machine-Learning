# -*- coding:utf8 -*-
import pickle
from imutils import paths
import os.path
import numpy as np
import cv2 as cv
from fit_image import resize_to_fit
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense

# 快速构建一个
letter_img_folder = "extracted_letter_images"  # 字符
model_filename = 'captcha_crash_model.hdf5'  # 模型
model_labels_filename = "model_labels.dat"  # 标记

# 初始化数据集和标记集
data = []
labels = []

# 循环处理字符图片
for img_file in paths.list_images(letter_img_folder):
    img = cv.imread(img_file, 0)  # 读入灰度字符
    # print("before", img)
    img = resize_to_fit(img, 20, 20)  # 调整图像大小为20*20
    img = np.expand_dims(img, axis=2)  # 把图像加到第三轴上便于keras处理
    # print("after", img)
    label = img_file.split(os.path.sep)[-2]  # 根据路径分隔符提取标记

    # 添加元数据
    data.append(img)
    labels.append(label)

data = np.array(data, dtype="float") / 255.0  # 归一化为[0,1] 优化训练
labels = np.array(labels)

# 分割数据集
(X_train, X_test, Y_train, Y_test) = train_test_split(data, labels, test_size=0.25, random_state=0)

# 调整为热编码
# TODO: 待学习 one-hot encoding
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# 序列化保存模型
with open(model_labels_filename, 'wb') as f:
    pickle.dump(lb, f)

# 建立神经网络，采用序贯模型
model = Sequential()

# 添加第一个带有max pooling(对邻域内特征点取最大)的卷积网络层
model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# 添加第二个带有max pooling的卷积层
model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# 具有500节点的隐藏层
model.add(Flatten())
model.add(Dense(500, activation="relu"))

# 具有32节点的神经网络输出层, 激活函数为softmax多类判别
model.add(Dense(32, activation="softmax"))

# 编译模型,　softmax对应的多类对数损失函数, adma优化器, 指标为精度
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# 训练神经网络
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=32, epochs=10, verbose=1)

# 保存模型
model.save(model_filename)
