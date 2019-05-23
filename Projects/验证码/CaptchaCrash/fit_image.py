# -*- coding:utf8 -*-
import imutils
import cv2 as cv

def resize_to_fit(image, width, height):
    """
    保持长宽比缩放填充图片
    :param image: 输入图片
    :param width: 输出的宽度
    :param height: 输出的高度
    :return: 返回调整大小后的图片
    """
    h, w = image.shape[:2]
    if w > h:
        image = imutils.resize(image, width=width)
    else:
        image = imutils.resize(image, height=height)

    # 向两边填充图像的长和宽
    pad_h = int((height - image.shape[0]) / 2.0)
    pad_w = int((width  - image.shape[1]) / 2.0)

    image = cv.copyMakeBorder(image, pad_h, pad_w, pad_h, pad_w, cv.BORDER_REPLICATE)
    image = cv.resize(image, (width, height))
    return image