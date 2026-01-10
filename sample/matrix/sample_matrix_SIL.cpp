#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include "sample_matrix.hpp"

namespace sample_matrix_SIL {

namespace py = pybind11;

SampleMatrix sm;

void initialize(void) { sm = SampleMatrix(); }

// Class: SampleMatrix
// Method: add
py::array_t<SampleMatrix::FLOAT> add(py::array_t<SampleMatrix::FLOAT> A_in,
                                     py::array_t<SampleMatrix::FLOAT> B_in) {

  py::buffer_info A_info = A_in.request();
  py::buffer_info B_info = B_in.request();

  /* check compatibility */
  if (SampleMatrix::MATRIX_SIZE != A_info.shape[0]) {
    throw std::runtime_error("ref must have " +
                             std::to_string(SampleMatrix::MATRIX_SIZE) +
                             " columns.");
  }

  if (SampleMatrix::MATRIX_SIZE != B_info.shape[0]) {
    throw std::runtime_error("ref must have " +
                             std::to_string(SampleMatrix::MATRIX_SIZE) +
                             " columns.");
  }

  /* substitute */
  SampleMatrix::DenseMatrix_Type A;
  SampleMatrix::DiagMatrix_Type B;

  SampleMatrix::FLOAT *A_data_ptr =
      static_cast<SampleMatrix::FLOAT *>(A_info.ptr);
  for (std::size_t i = 0; i < SampleMatrix::MATRIX_SIZE; i++) {
    for (std::size_t j = 0; j < SampleMatrix::MATRIX_SIZE; j++) {

      A(i, j) = A_data_ptr[i * SampleMatrix::MATRIX_SIZE + j];
    }
  }

  SampleMatrix::FLOAT *B_data_ptr =
      static_cast<SampleMatrix::FLOAT *>(B_info.ptr);
  for (std::size_t i = 0; i < SampleMatrix::MATRIX_SIZE; i++) {
    B(i) = B_data_ptr[i * SampleMatrix::MATRIX_SIZE + i];
  }

  /* call add method */
  auto result = sm.add(A, B);

  /* return numpy array */
  py::array_t<SampleMatrix::FLOAT> output;
  output.resize({static_cast<int>(SampleMatrix::MATRIX_SIZE),
                 static_cast<int>(SampleMatrix::MATRIX_SIZE)});

  for (std::size_t i = 0; i < SampleMatrix::MATRIX_SIZE; ++i) {
    for (std::size_t j = 0; j < SampleMatrix::MATRIX_SIZE; ++j) {
      output.mutable_at(i, j) = result(i, j);
    }
  }

  return output;
}

PYBIND11_MODULE(SampleMatrixSIL, m) {
  m.def("initialize", &initialize, "Initialize the module");
  m.def("add", &add, "add method");
}

} // namespace sample_matrix_SIL
