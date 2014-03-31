#include "util.hpp"
#include "Image.hpp"
#include "ImageEffects.hpp"
#include <gnuplot_i.hpp>

using std::cout;
using std::endl;

void wait_for_key ()
{
    cout << endl << "Press ENTER to continue..." << endl;
    std::cin.get();
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Usage: " << std::endl
                  << argv[0] << " <image path>" << std::endl;
        exit(1);
    }

    Image img(argv[1]);

    Gnuplot g1("lines");
    g1.plot_x(img.getHistogram(), "Original");
    for (int i = 0; i < 5; ++i) {
        int contrast = (i+1) * 20;
        Image tmp = ImageEffects::contrastEnhance(img, contrast);

        char* title = (char*) malloc(30);
        sprintf(title, "Contrast: %d", contrast);
        g1.plot_x(tmp.getHistogram(), title);
    }

    wait_for_key();

    return 0;
}
