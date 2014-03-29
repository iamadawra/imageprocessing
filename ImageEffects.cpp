#include "ImageEffects.hpp"

Image ImageEffects::contrastEnhance(Image img, int enhance) {
    Image out(img);
    out.fImage.adjustContrast(enhance);
    return out;
}
