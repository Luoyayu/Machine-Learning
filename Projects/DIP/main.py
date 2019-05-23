import cv2 as cv
import numpy as np
import sys, os
import matplotlib as mpl
# mpl.use("Qt5Agg")
import matplotlib.pyplot as plt

print(mpl.get_backend())


def video_cap():
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


def read_show_pic_by_cv():
    # read and show a gray picture
    img = cv.imread('./autumn.jpg', 0)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', img)
    k = cv.waitKey(0) & 0xFF
    if k == 27:
        cv.destroyAllWindows()
    else:
        cv.imwrite('saver.jpg', img)
        cv.destroyAllWindows()


def save_cap_video_by_cv():
    cap = cv.VideoCapture(0)
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    out = cv.VideoWriter("out.MJPEG", fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv.flip(frame, 0)
            out.write(frame)
            cv.imshow('frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv.destroyAllWindows()


img = cv.imread('./autumn.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
plt.subplot(121)
plt.imshow(img, interpolation='bicubic')
plt.xticks([]), plt.yticks([])  # hidden tick value X and Y axis
plt.subplot(122)
plt.imshow(img_gray, cmap='gray', interpolation='bicubic')
plt.xticks([]), plt.yticks([])  # hidden tick value X and Y axis
plt.show()
# save_cap_video_by_cv()
