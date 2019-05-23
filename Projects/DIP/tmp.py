import numpy as np
import cv2 as cv
import matplotlib
import matplotlib.pylab as plt

class Point:
    def __int__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f


def Linear(J, Q11, Q21, Q12=None, Q22=None, methord='bi'):
    x, y = J.x, J.y
    x1, y1 = Q11.x, Q11.y
    x2, y2 = Q22.x, Q22.y
    X = np.array([x2 - x, x - x1])
    F = np.array([[Q11.f, Q12.f], [Q21.f, Q22.f]])
    Y = np.array([y2 - y, y - y1]).T
    if methord == 'bi':
        return 1 / (x2 - x1) / (y2 - y1) * X @ F @ Y
    else:
        return (x2 - x) / (x2 - x1) * Q11.f + (x - x1) / (x2 - x1) * Q21.f


def main():
    img = cv.imread('./a.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    img_eq = cv.equalizeHist(img)
    plt.subplot(122)
    plt.imshow(img_eq, cmap='gray')
    plt.show()


if __name__ == '__main__':
   main()
