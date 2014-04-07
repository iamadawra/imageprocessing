import numpy as np
import ImageOps

import numpy.fft as fft

class HistogramEqualizationDetector(object):
    def __init__(self, alpha_fn=1, r=0.2, decision=1.5):
        self.alpha_fn = alpha_fn
        self.r = r
        self.decision = decision

    def handle_exposure(self, histogram):
        histogram = self.handle_underexposure(histogram)
        histogram = self.handle_overexposure(histogram)
        return histogram

    def handle_underexposure(self, histogram):
        """
        When underexposed images are equalized, their first couple histogram
        bins end up having 0 pixels. We shift the histogram so that 
        h'(0) = h(k+1), where k is the first non-zero bin. I'm not entirely
        sure what that "+ 1" is for, but I assume it gets rid of the impulse
        at the kth bin.

        TODO: the paper does not specify what to do with the bins on the right
        that don't have values because of the shift. Currently, we zero them
        out.
        """
        N = np.sum(histogram)
        first_non_zero = np.where((histogram != 0))[0][0]

        if first_non_zero >= 2 and histogram[first_non_zero] >= 2*N/255.0:
            # underexposed
            new_hist = np.zeros(256)
            new_hist[:255-first_non_zero-1] = histogram[first_non_zero+1:]
            return new_hist
        return histogram

    def handle_overexposure(self, histogram):
        """
        When overexposed images are equalized, the pixels with value 254 are
        mapped to output values <= 253. We drop values higher than k-1 in the
        histogram where k is the last non-zero bin. Again, not entirely sure
        what that "- 1" is for, but I Assume it gets rid of the impulse at the
        kth bin.

        TODO: the paper does not specify what to do with the bins on the left
        that don't have values because of the shift. Currently, we zero them
        out.
        """
        N = np.sum(histogram)
        last_non_zero = np.where((histogram != 0))[0][-1]

        if last_non_zero <= 253 and histogram[last_non_zero] >= 2*N/255.0:
            # overexposed
            new_hist = histogram
            new_hist[last_non_zero:] = 0
            return new_hist

        return histogram

    def alpha(self):
        return self.alpha_1() if self.alpha_fn == 1 else self.alpha_2()

    def alpha_1(self):
        """
                   /  exp(-r*k),         if 0 <= k < 128
        alpha_1 = <
                   \  exp(-r*(256-k)),   if 128 <= k <= 255
        """
        alpha_1 = np.arange(256).astype('float')
        alpha_1[:128] = np.exp(-self.r*alpha_1[:128])
        alpha_1[128:] = np.exp(-self.r*(256 - alpha_1[128:]))
        return alpha_1

    def alpha_2(self):
        """
                   /  1,   if k <= r or (256 - k) <= r
        alpha_2 = <
                   \  0,   else
        """
        alpha_2 = np.zeros(256)
        alpha_2[:self.r] = 1
        alpha_2[256-self.r:] = 1
        return alpha_2

    def distance_from_uniform(self, img):
        """
        D = 1/N * sum_{k != 0} |H(k)| alpha(k)

        We ignore k = 0 as that's the DC: the number of pixels in the image.
        """
        img = ImageOps.grayscale(img)
        histogram = np.array(img.histogram())
        histogram = self.handle_exposure(histogram)

        histogram[0] = 0
        hist_fft = fft.fft(histogram)
        return np.sum(np.abs(hist_fft) * self.alpha()) / np.sum(histogram)

    def classify(self, img):
        return self.distance_from_uniform(img) <= self.decision
