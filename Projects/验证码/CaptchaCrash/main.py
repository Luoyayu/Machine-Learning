# -*- coding:utf8 -*-
from keras.models import load_model
from fit_image import resize_to_fit
from imutils import contours
import cv2 as cv
import pickle
import numpy as np
from imutils import paths
import imutils
import os

model_filename = 'captcha_crash_model.hdf5'  # 模型
model_labels_filename = "model_labels.dat"  # 模型标记

with open(model_labels_filename, 'rb') as f:
    lb = pickle.load(f)

model = load_model(model_filename)

captcha_img = input('请输入验证码图片的本地地址')
image = cv.imread(captcha_img, 0)

# 对验证码图片进行边缘填充
image = cv.copyMakeBorder(image, 20, 20, 20, 20, cv.BORDER_REPLICATE)

# Otsu's 二值化
ret, thresh = cv.threshold(
    image, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

# 找轮廓
Contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[1]
# Contours = contours.sort_contours(thresh, method="left-to-right")

# 分割字符
letter_img_regions = []

for contour in Contours:
    # 定位字符轮廓
    x, y, w, h = cv.boundingRect(contour)

    if w / h > 1.25:
        half_w = int(w / 2.0)
        letter_img_regions.append((x, y, half_w, h))
        letter_img_regions.append((x + half_w, y, half_w, h))
    else:
        letter_img_regions.append((x, y, w, h))

if (len(letter_img_regions) != 4):
    print("未检测出合适轮廓! {}".format(len(letter_img_regions)))

letter_img_regions = sorted(letter_img_regions, key=lambda x: x[0])

output_img = cv.merge([image] * 3)
predictions = []

# 处理每个字符轮廓
for letter_bounding_box in letter_img_regions:
    x, y, w, h = letter_bounding_box

    letter_img = image[y - 2:y + h, x - 2:x + w + 2]

    letter_img = resize_to_fit(letter_img, 20, 20)

    # 扩充图像的维度
    letter_img = np.expand_dims(letter_img, axis=2)
    letter_img = np.expand_dims(letter_img, axis=0)

    # 应用模型给出预测
    prediction = model.predict(letter_img)

    # 把热编码预测还原成字符
    letter = lb.inverse_transform(prediction)[0]
    predictions.append(letter)

    # 检测并绘制矩形
    cv.rectangle(output_img, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 225, 0), 1)
    cv.putText(output_img, letter, (x - 5, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

captcha_text = "".join(predictions)
print('i see the text is {}'.format(captcha_text))

cv.imshow('Crash_Captcha', output_img)
cv.waitKey(0)
# cv.imshow("Crash_Captcha", output_img)
# cv.waitKey()

