#ifndef _IMAGE_HPP
#define _IMAGE_HPP
#include "util.hpp"

class ImageEffects;

class Image {
friend class ImageEffects;

public:
    Image(char* _path);

    // Copy constructor
    Image(const Image& other);

    std::vector<unsigned int> getHistogram();

private:
    fipImage fImage;
    char* path;
};
#endif
