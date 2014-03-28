#include "util.hpp"
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

    fipImage a;
    a.load(argv[1]);

    std::vector<unsigned int> histogram(256);
    a.getHistogram(&histogram[0]);

    Gnuplot g1("lines");
    g1.plot_x(histogram);

    wait_for_key();

    return 0;
}
