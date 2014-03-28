#ifndef _IMAGE_HPP
#define _IMAGE_HPP
#include "util.hpp"

class Image {
public:
    Image(char* path);
    std::vector<unsigned int> getHistogram();

private:
    fipImage fImage;
};
#endif
