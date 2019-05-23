"""常用数字图像处理处理变量和函数
提供的变量:
    gray_ —— 灰色
    
提供的函数:
    ti  —— 匿名函数, 返回CPU时间
    cos —— 匿名函数, cos
    sin —— 匿名函数, sin
    plot_gray_img
    plot_two_gray_img
    plot_three_gray_img
    got_snr
    got_ifft_img
    got_magnitude_spectrum_img
    got_phase_angle
"""

__version__ = "0.1.0"
import numpy as np
import matplotlib
import matplotlib.pylab as plt
import scipy
import cv2 as cv
from scipy import signal
import time, os
from termcolor import cprint

# 常用变量函数
gray_ = "gray"
epsilon = 1e-11
lena_path = "/Volumes/MacMisc/Machine-Learning/DIP/lena.bmp"
ti = lambda :time.time() # ti()获取CPU时间
cos = lambda x:np.cos(x)
sin = lambda x:np.sin(x)
pi = np.pi

    
# 常用显示图像函数
def plot_gray_img(image_, title_="", w=4, h=4, cmap=None):
    """
    功能: 显示一图像
    输入: 图像, 标题【】, width【4】, height【4】, cmap【None】
    """
    plt.figure(figsize=(w, h))
    plt.axis('off');plt.title(title_)
    if cmap is not None:
        plt.imshow(image_, cmap=cmap)
    else:
        if image_.shape[-1] == 1 :
            plt.imshow(image_, cmap=gray_)
        else:
            image_ = cv.cvtColor(image_, cv.COLOR_BGR2RGB)
            plt.imshow(image_)
    plt.show()

    
def plot_two_img(img1, img2, title1="", title2="", w=8, h=8, cmap1=None, cmap2=None):
    """
    功能: 并排显示两幅图像
    """
    f = plt.figure(figsize=(w, h))
    f.subplots_adjust(wspace=0.1)
    ax1 = f.add_subplot(121, title=title1)
    ax2 = f.add_subplot(122, title=title2)
    ax1.imshow(img1, cmap=cmap1);ax1.axis('off')
    ax2.imshow(+img2, cmap=cmap2);ax2.axis('off')
    plt.show()
    
    
def plot_three_gray_img(img1, img2, img3, title1="", title2="", title3="",w=8, h=8):
    """
    功能: 并排显示三幅图像
    """
    f = plt.figure(figsize=(w,h))
    plt.subplot(131);plt.axis('off');plt.title(title1)
    plt.imshow(img1, gray_)
    plt.subplot(132);plt.axis('off');plt.title(title2)
    plt.imshow(img2, gray_)
    plt.subplot(133);plt.axis('off');plt.title(title3)
    plt.imshow(img3, gray_)
    plt.show()

    
def got_snr(Img, Img_with_noise):
    """
    输入: 原图像, 有噪声的拟合图像 
    输出: 信噪比
    """
    snr = np.sum(Img_with_noise**2)
    snr /= np.sum((Img-Img_with_noise)**2)
    return snr


def got_ifft_img(Img_ms):
    """
    输入: 中心化过的幅度值[complex]阵列
    输出: 原图像
    """
    F_ishift = np.fft.ifftshift(Img_ms)
    Img_back = np.fft.ifft2(F_ishift)
    return np.abs(Img_back)


def got_magnitude_spectrum(Img, flag=1, k=20):
    """
    输入: 
          Img: 图像
          flag: 【1】是否k*log标定
          k: 标定系数【20】
    输出: 
          if flag:
              return 中心化且log标定过的幅度值图像
          else: 
              return 幅度值[complex]阵列
    """
    Img_f  = np.fft.fft2(Img)
    Img_fs = np.fft.fftshift(Img_f)
    if flag:
        return k * np.log(np.abs(Img_fs)+epsilon)
    return Img_fs


def got_phase_angle(Img):
    """
    输入: 
          图像: Img
    输出: 
          相角阵列
    """
    Img_f  = np.fft.fft2(Img)
    Img_fs = np.fft.fftshift(Img_f)
    return np.angle(Img_fs)

def PF_2d(r, lowp, flag, d0, d1=None, n=None):
    """
    功能: 频率域上滤波器
    输入: 
        r: 图像
        lowp: 
            1: 低通滤波器
            0: 高通滤波器
        flag:
            0：理想滤波
            1: 巴特沃斯滤波
            2: 梯形滤波
            3: 高斯滤波
        d0: 低通直径
        d1: 低通直径
        n: 
            如果是巴特沃斯/指数滤波, 则是阶数【2】
    输出: 
        滤波后的图像[uint8]
    """
    nrows = cv.getOptimalDFTSize(r.shape[0])
    ncols = cv.getOptimalDFTSize(r.shape[1])
    r_bst = np.zeros((nrows,ncols))
    r_bst[:rows, :cols] = r
    r_fs = np.fft.fftshift(np.fft.fft2(r_bst))
    center = [nrows//2, ncols//2]
    H = np.zeros(r_fs.shape)
    for u in range(nrows):
        for v in range(ncols):
            duv = np.hypot(u-center[0], v-center[1])
            if flag == 0: # 理想滤波器
                H[u][v] = duv < d0 if lowp else duv > d0
            elif flag == 1: # 巴特沃斯滤波器
                H[u][v] = 1 / ((1 + (duv / d0)) ** (2*n)) if lowp \
                else 1 / ((1 + (d0 / duv)) ** (2*n))
            elif flag == 2: # 梯形滤波器
                if lowp:
                    if duv > d0:
                        H[u][v] = 1
                    elif duv > d1:
                        H[u][v] = 0
                    elif d0 <= duv and duv <= d1:
                        H[u][v] = (duv-d1)/(d0-d1)
                else:
                    if duv < d0:
                        H[u][v] = 0
                    elif duv > d0:
                        H[u][v] = 1
                    elif d1 <= duv and duv <= d0:
                        H[u][v] = (d0-d1)/(duv-d1)
            elif flag == 3: # 高斯(指数)滤波器
                if n is None:n=2
                H[u][v] = (np.e ** (-(duv**n)/(d0**n))) if lowp \
                else (1-np.e ** (-(duv**n)/(d0**n)))
    s_ext = got_ifft_img(r_fs * H)
    s = s_ext[0:r.shape[0], 0:r.shape[1]]
    return s.astype(np.uint8)

