import numpy as np
import ImageOps

import numpy.fft as fft

class GlobalContrastDetector(object):
    def __init__(self, Np=4, c=112, decision=100):
        self.Np = Np
        self.c = c
        self.decision = decision

    def pinch(self):
        """
        The pinch function as described in the paper.
                /  0.5 - 0.5 cos(pi*l/Np)              l <= Np
        p(l) = <   0.5 + 0.5 cos(pi*(l-255+Np)/Np) ,   l >= 255 - Np
                \  1                                    else
        """
        p = np.ones(256)
        values = np.arange(256)

        first = np.where(values <= self.Np)
        p[first] = .5 - .5 * cos(math.pi * first[0] / float(N.p))

        second = np.where(values >= 255 - N.p)
        p[second] = .5 + .5 * cos(math.pi * (second[0] - 255 + N.p) / N.p)

        return p

    def fft_energy(self, img):
        """
        Calculate the energy of this histogram as described in the paper

        E = (1/N) * sum_{k} (beta(k) * G(k))
            * G(k) = @hist_fft
                         / 1     @c <= k <= 128
            * beta(k) = <    ,
                         \ 0     else
            * paper suggests @c value of 112
        """
        img = ImageOps.grayscale(img)
        histogram = np.array(img.histogram())
        hist_fft = fft.fft(img.histogram())

        beta = np.zeros(256)
        beta[self.c:128] = 1
        return np.sum(np.abs(beta * hist_fft)) / 256.0

    def classify(self, img):
        return (self.fft_energy(img) > self.decision)
