#include "Image.hpp"

Image::Image(char* path) : fImage(fipImage()), path(path) {
    fImage.load(path);
}

Image::Image(const Image& img) : fImage(fipImage(img.fImage)) {
}

std::vector<unsigned int> Image::getHistogram() {
    std::vector<unsigned int> *out = new std::vector<unsigned int>(256);
    fImage.getHistogram(&((*out)[0]));
    return *out;
}
