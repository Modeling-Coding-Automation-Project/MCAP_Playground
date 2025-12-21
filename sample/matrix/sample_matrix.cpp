#include "sample_matrix.hpp"

SampleMatrix::SampleMatrix() : _data{} {}

SampleMatrix::~SampleMatrix() {}

// Matrix addition
SampleMatrix::DenseMatrix_Type
SampleMatrix::add(const SampleMatrix::DenseMatrix_Type &A,
                  const SampleMatrix::DiagMatrix_Type &B) {
  return A + B;
}
