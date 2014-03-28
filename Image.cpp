#include "Image.hpp"

Image::Image(char* path) : fImage(fipImage()) {
    fImage.load(path);
}

std::vector<unsigned int> Image::getHistogram() {
    std::vector<unsigned int> *out = new std::vector<unsigned int>(256);
    fImage.getHistogram(&((*out)[0]));
    return *out;
}
