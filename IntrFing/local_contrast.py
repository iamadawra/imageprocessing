import math
import numpy as np
from PIL import Image
from PIL import ImageOps

import numpy.fft as fft
from numpy import cos

class LocalContrastDetector(object):
    def __init__(self, gcd):
        #Takes the Global Contrast Enhancement detector as an input for now
        #Maybe just transfer functionality later once trying to clean up code
        self.gcd = gcd

    def createBlackImage(self, img):
        """
        Creates a black image of the same dimensions as the input image.
        """
        imgWidth = img.size[0]
        imgHeight = img.size[1]
        blackImg = Image.new('RGB', (imgWidth,imgHeight), "black")
        return blackImg

    def generateSubImage(self, size):
        """
        Generates a sub image of size x size
        """
        return Image.new('RGB', (size, size), "black")

    def checkLocalContrast(self, img, boxSize=50):
        """
        Breaks the image into boxSize x boxSize sized chunks and applies the
        Global Contrast Enhancement algorithm to check for Local Contrast Enhancement.
        """
        #create a copy of the image
        img = img.copy()
        imgWidth, imgHeight = img.size
        currX = 0
        currY = 0
        flag = True
        while(flag):
            #print("currX+boxSize: " + str(currX+boxSize))
            #print("currY: " + str(currY))
            if currX+boxSize <= imgWidth and currY+boxSize <= imgHeight:
                #print("Checkpoint 1")
                #Case where image is being chopped up into perfect squares
                box = (currX, currY, currX + boxSize, currY + boxSize)
                #print("BOX: " + str(box))
                region = img.crop(box)
                #print("Region: " + str(region.size))
                #compare fft_energy of enhanced image with original image over here
                img.paste(self.checkLocalContrastHelper(region), box)

                #Reset currX and currY
                currX = currX + boxSize
                continue
            if currX+boxSize <= imgWidth and currY+boxSize > imgHeight:
                #print("Checkpoint 2")
                #Case where there is enough width but not enough height
                box = (currX, currY, currX + boxSize, imgHeight)
                region = img.crop(box)
                #compare fft_energy of enhanced image with original image over here
                img.paste(self.checkLocalContrastHelper(region), box)

                #Reset currX and currY
                currX = currX + boxSize
                continue
            if currX+boxSize > imgWidth and currY+boxSize <= imgHeight:
                #print("Checkpoint 3")
                #Case where there is enough height but not enough width
                box = (currX, currY, imgWidth, currY + boxSize)
                region = img.crop(box)
                #compare fft_energy of enhanced image with original image over here
                img.paste(self.checkLocalContrastHelper(region), box)

                #Reset currX and currY
                currX = 0
                currY = currY + boxSize
                continue
            else:
                #print("Checkpoint 4")
                #Case where there is not enough width and not enough height
                box = (currX, currY, imgWidth, imgHeight)
                region = img.crop(box)
                #compare fft_energy of enhanced image with original image over here
                img.paste(self.checkLocalContrastHelper(region), box)

                #Stop the loop
                flag = False

        #display the final Image        
        img.show()

    def checkLocalContrastHelper(self, img, thresholdValue=1.5):
        """
        Function to compare the contrast of a subpart of a given image.
        """
        #print("Inside checkLocalContrastHelper")
        originalImg = img
        contrastedImg = ImageOps.autocontrast(img)
        originalFFT = self.gcd.fft_energy(originalImg)
        contrastedFFT = self.gcd.fft_energy(contrastedImg)
        #print("Threshold: " + str(thresholdValue))
        #print("Value: " + str(math.fabs(originalFFT-contrastedFFT)))
        if (math.fabs(originalFFT-contrastedFFT) >= thresholdValue):
            #print("I'm here!")
            return self.blackBorderImage(img)
        return img

    def blackBorderImage(self, img, borderWidth=1):
        imageWidth, imageHeight = img.size
        #print("imageWidth: "+ str(imageWidth))
        #print("imageHeight: " + str(imageHeight))
        box = (borderWidth, borderWidth, (imageWidth - (borderWidth*2)), (imageHeight - (borderWidth*2)))
        #print("box: " + str(box))
        croppedImage = img.crop(box)
        new_im = Image.new("RGB", (imageWidth, imageHeight))   ## luckily, this is already black!
        new_im.paste(croppedImage, box)
        return new_im
