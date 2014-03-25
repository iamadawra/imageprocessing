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

* Consider the effect of a pixel value mapping on the histogram, h'(l).
* Look at f(l) = h'(l) - h(l) and its frequency response.
