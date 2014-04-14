import math
import sys

from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
import matplotlib
import numpy as np

import matplotlib.pyplot as plt
import numpy.fft as fft

from numpy import cos
from pylab import imshow
from matplotlib.gridspec import GridSpec

from global_contrast import *
from histogram_equalize import *

def load_gray(path):
    return ImageOps.grayscale(Image.open(path))

def show_gray(img):
    return imshow(img, cmap=plt.cm.gray)

def get_hist_fft(im):
    return fft.fft(np.array(im.histogram()))

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
    plt.plot(np.abs(fft.fftshift(fft.fft(im.histogram()))), label='original')
    plt.plot(np.abs(fft.fftshift(fft.fft(im_cont.histogram()))), label='contrast')
    plt.legend()

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'img/lena.tiff'

    im = load_gray(path)
    im_cont = ImageOps.autocontrast(im)

    gcd = GlobalContrastDetector()
    print "Energy (original): %s" % gcd.fft_energy(im)
    print "Energy (contrast): %s" % gcd.fft_energy(im_cont)

    compare_display(im, im_cont)

    im_eq = ImageOps.equalize(im)
    hed = HistogramEqualizationDetector()

    print "Distance from uniform (original): %s" % hed.distance_from_uniform(im)
    print "Distance from uniform (equalized): %s" % hed.distance_from_uniform(im_eq)

    show_gray(im)
    plt.figure()
    show_gray(im_eq)
    plt.figure()

    plt.plot(im.histogram(), label="original")
    plt.plot(im_eq.histogram(), label="equalized")
    plt.plot(hed.handle_exposure(np.array(im_eq.histogram())), label="exposure handling equalized")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
