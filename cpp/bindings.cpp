#include <pybind11/pybind11.h>

int add(int a, int b);
std::string sha256sum(std::string input);

PYBIND11_MODULE(cppmethods, m) {
    m.def("add", &add);
    m.def("sha256sum", &sha256sum);
    // m.def("bcrypt", &bcrypt);
}