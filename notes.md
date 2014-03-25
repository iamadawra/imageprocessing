General idea
============

The goal is to detect pixel mapping manipulations. They leave behind traceable
fingerprints in their histograms, and by creating a model of unaltered images,
we can detect these.

Model of unaltered images
-------------------------

* None of the histograms contain sudden zeros or impulsive peaks. Furthermore,
  individual histogram values do not differ greatly from the histogram's
  envelope.
* Interpolatably connected: Any histogram value can be interpolated using a
  cubic spline of all the other histogram values.
* Works very well for most unaltered images; issues with especially under- and
  overexposed images.

Fingerprints of Pixel Value Mappings
------------------------------------

Note: For rest of these notes, h' is the histogram of the modified image, h is
the histogram of the original image.

* Consider the effect of a pixel value mapping on the histogram, h'(l).
* Look at f(l) = h'(l) - h(l) and its frequency response.


### Contrast Enhancement
* Can prove that energy of DFT(h') >= energy of DFT(h). This increase in energy
  can't occur at DC (DC corresponds to sum of histogram values, i.e. the number
  of pixels).
* Thus, DFT(h') has more energy at higher frequencies; but we expect DFT of
  unaltered histograms to have high energy at DC
* We attempt to detect contrast enhancement by looking at strenght of high
  frequencies; but this can flag overexposed images as well. Use a pinch
  function to reduce color values at either saturation end (low values or high
  values). The pinch function can be seen in the ipython notebook.
