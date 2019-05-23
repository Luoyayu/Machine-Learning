# -*- coding:utf8-*-
import os.path
import cv2 as cv
import imutils
import os
import glob

captcha_img_folder = "generated_captcha_images"
output_img_folder = "extracted_letter_images"

captcha_img_files = glob.glob(os.path.join(captcha_img_folder, "*"))  # 保存图片的相对路径
counts = {}  # 为分割出的字符编号
# print(captcha_img_files)

for (i, captcha_img_file) in enumerate(captcha_img_files):
    print("[INFO] processing img {}/{}".format(i + 1, len(captcha_img_files)))

    # 获取图片的文件名含扩展名
    filename = os.path.basename(captcha_img_file)

    # 获取不含扩展名的文件名即是图片的验证码
    captcha_text = os.path.splitext(filename)[0]
    # print(captcha_text)

    # 读取图片并转成灰度图
    gray_img = cv.imread(captcha_img_file, 0)
    # cv.imshow('raw', cv.imread(captcha_img_file))
    # cv.waitKey(100)

    # 在灰度图周围填充8个黑色像素，不采用原作者的边缘填充，直接常亮填充 ，dst = None, value = Black
    gray_img = cv.copyMakeBorder(gray_img, 8, 8, 8, 8, cv.BORDER_CONSTANT, None, [255, 255, 255])

    # cv.imshow('gray', gray_img)
    # cv.waitKey(10)

    # 二值化 采取反二进制＋otsu's　变为纯黑白图
    ret, thresh = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

    # 检测最外层轮廓,采取方法: RETR_EXTERNAL, 轮廓近似方法：只保存拐点, 偏移: None
    # contours()-> image, contours, hierarchy
    img, contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # cv.imshow('Contours', cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0])
    # cv.waitKey(10)

    # print(contours)

    letter_img_regions = []

    for contour in contours:
        # 根据保存的轮廓的拐点获取相应的矩形轮廓
        x, y, w, h = cv.boundingRect(contour)
        # cv.imshow('bounding', cv.rectangle(img, (x, y), (x + w, y + h), (238, 130, 238), 1))
        # cv.waitKey(10)

        # 粗略处理两个字母挤压到一个轮廓的情况
        # 作者的进一步策略
        # There is no one "correct" answer other than to try different approaches and
        #  see what works for the data set.
        if w / h > 1.25:  # 宽度是长度的1.25倍以上
            half_w = int(w / 2)
            letter_img_regions.append((x, y, half_w, h))
            letter_img_regions.append((x + half_w, y, half_w, h))
        else:
            letter_img_regions.append((x, y, w, h))

    # 防止产生不好的训练集
    if len(letter_img_regions) != 4:
        # print('An error!The num of letter is', len(letter_img_regions))
        # for i in range(len(letter_img_regions)):
        #     (x, y, w, h) = letter_img_regions[i]
        #     cv.imshow('demo', cv.rectangle(img, (x, y), (x + w, y + h), (238, 130, 238), 1))
        # cv.waitKey()
        continue

    # 对轮廓排序保证自左向右处理
    letter_img_regions = sorted(letter_img_regions, key=lambda _: _[0])

    # 保存每一个轮廓内容到对应的字母文件夹内, zip 将每个轮廓与相应的字符对应起来
    for letter_bounding_box, letter_text in zip(letter_img_regions, captcha_text):

        x, y, w, h = letter_bounding_box

        # 从边缘向外２像素提取原始图像中的字母
        letter_img = gray_img[y - 2:y + h + 2, x - 2:x + w + 2]

        save_path = os.path.join(output_img_folder, letter_text)

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # 为该字符启用计数器
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        cv.imwrite(p, letter_img)

        counts[letter_text] = count + 1
