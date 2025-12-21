#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void initialize(void) {}

// Class: SampleMatrix
// Method: add
void add(void) {}

PYBIND11_MODULE(SampleMatrixSIL, m) {
    m.def("initialize", &initialize, "Initialize the module");
    m.def("add", &add, "add method");
}
