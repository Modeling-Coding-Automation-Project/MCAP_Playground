#ifndef SAMPLE_MATRIX_HPP_
#define SAMPLE_MATRIX_HPP_

#include "python_numpy.hpp"

class SampleMatrix {
public:
  using FLOAT = double;
  static constexpr std::size_t MATRIX_SIZE = 3;

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

#endif // SAMPLE_MATRIX_HPP_
