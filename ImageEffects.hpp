#ifndef _IMAGE_EFFECTS_HPP
#define _IMAGE_EFFECTS_HPP
#include "util.hpp"
#include "Image.hpp"

class ImageEffects {
public:
    static Image contrastEnhance(Image img, int enhance);
};

#endif
