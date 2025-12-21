#ifndef __SAMPLE_MATRIX_HPP__
#define __SAMPLE_MATRIX_HPP__

#include "python_numpy.hpp"

using FLOAT = double;
constexpr std::size_t MATRIX_SIZE = 3;

class SampleMatrix {
public:
  using DenseMatrix_Type =
      PythonNumpy::DenseMatrix_Type<FLOAT, MATRIX_SIZE, MATRIX_SIZE>;

  using DiagMatrix_Type = PythonNumpy::DiagMatrix_Type<FLOAT, MATRIX_SIZE>;

public:
  SampleMatrix();

  ~SampleMatrix();

  // Matrix addition
  DenseMatrix_Type add(const DenseMatrix_Type &A, const DiagMatrix_Type &B);

private:
  DenseMatrix_Type _data;
};

#endif // __SAMPLE_MATRIX_HPP__
