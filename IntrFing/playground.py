import math
import sys

import Image
import ImageOps
import ImageChops
import matplotlib
import numpy as np

import matplotlib.pyplot as plt
import numpy.fft as fft

from numpy import cos
from pylab import imshow
from matplotlib.gridspec import GridSpec

def load_gray(path):
    return ImageOps.grayscale(Image.open(path))

def show_gray(img):
    return imshow(img, cmap=plt.cm.gray)

def get_hist_fft(im):
    return fft.fft(np.array(im.histogram()))

def pinch(N=4):
    out = np.ones(256)
    values = np.arange(256)

    first = np.where(values <= N)
    out[first] = .5 - .5 * cos(math.pi * first[0] / float(N))

    second = np.where(values >= 255 - N)
    out[second] = .5 + .5 * cos(math.pi * (second[0] - 255 + N) / N)

    return out

def fft_energy(hist_fft, c=112):
    """
    Calculate the energy of this histogram as described in the paper

    E = (1/N) * sum_{k} (beta(k) * G(k))
        * G(k) = @hist_fft
                     / 1     @c <= k <= 128
        * beta(k) = <
                     \ 0     else
        * paper suggests @c value of 112
    """
    beta = np.zeros(256)
    beta[c:128] = 1
    return np.sum(np.abs(beta * hist_fft)) / 256.0

def compare_display(im, im_cont):
    """
    Display a number of images in one figure window:
        * Original im (@im)
        * Contrast enhanced image (@im_cont)
        * @im_cont - @im (difference)
        * Histograms of @im, @im_cont
        * dft of *histogram* of @im, @im_cont
    """

    gs = GridSpec(3, 3)
    plt.subplot(gs[0,0])
    show_gray(im)
    plt.xlabel('original')

    plt.subplot(gs[0,1])
    show_gray(im_cont)
    plt.xlabel('contrast')

    plt.subplot(gs[:,2])
    show_gray(ImageChops.subtract(im_cont, im))
    plt.xlabel('subtracted')

    plt.subplot(gs[1,:-1])
    plt.plot(im.histogram(), label='original')
    plt.plot(im_cont.histogram(), label='contrast')
    plt.legend()

    plt.subplot(gs[2,:-1])
    plt.plot(np.abs(fft.fftshift(get_hist_fft(im))), label='original')
    plt.plot(np.abs(fft.fftshift(get_hist_fft(im_cont))), label='contrast')
    plt.legend()

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'img/lena.tiff'

    im = load_gray(path)
    im_cont = ImageOps.autocontrast(im)

    compare_display(im, im_cont)
    plt.show()
    print "Energy (original): %s" % (fft_energy(get_hist_fft(im)))
    print "Energy (contrast): %s" % (fft_energy(get_hist_fft(im_cont)))

if __name__ == '__main__':
    main()
