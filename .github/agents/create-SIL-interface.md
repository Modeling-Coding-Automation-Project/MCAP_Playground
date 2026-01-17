---
name: create-SIL-interface
description: Write SIL C++ code to import C++ class to Python with Pybind11, and add Pybind11 code to python file.
---

# Role
Your role is to write SIL C++ code that uses Pybind11 to create Python bindings for a given C++ class.

You will also add the necessary Pybind11 code to the corresponding Python file to ensure the class can be imported and used in Python.

# Instructions

## 1. Read C++ code.

First, user will provide you with a C++ file that contains the class definition they want to expose to Python.

Read and understand the class structure, including its member functions and variables.

## 2. Write SIL C++ skelton code.

Create "*_SIL.cpp" file. "*" is the name of the C++ file without the ".cpp" extension.

Basic style of the SIL C++ code is below:

```cpp
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include "sample_matrix.hpp"

namespace sample_matrix_SIL {

namespace py = pybind11;

void initialize(void) {}

// Class: MyFunc
// Method: increment
void increment(void) {}

// Method: decrement
void decrement(void) {}

PYBIND11_MODULE(MyFuncSIL, m) {
    m.def("initialize", &initialize, "Initialize the module");
    m.def("increment", &increment, "increment method");
    m.def("decrement", &decrement, "decrement method");
}

} // namespace sample_matrix_SIL
```

You need to write the same functions and methods as in the original C++ class, but adapted for Python using Pybind11.

## 3. Write the detail of SIL C++ function.

In the code in previous step, you only wrote the function signatures.

For example, those functions are written as below:

```cpp
double MyFunc::increment(double amount) {
  this->_value += amount;
  return this->_value;
}

double MyFunc::decrement(double amount) {
  this->_value -= amount;
  return this->_value;
}
```

Then, you need to write the detail of SIL functions as below.

```cpp
// Class: MyFunc
// Method: increment
double increment(double amount) { return myFuncInstance.increment(amount); }

// Method: decrement
double decrement(double amount) { return myFuncInstance.decrement(amount); }
```

### 3.1 Handle matrix or vector input and output.

If the C++ function takes or returns matrix or vector types, use `py::array_t` to handle them.

For example, if the C++ function is defined as below:

```cpp
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

SampleMatrix::SampleMatrix() : _data{} {}

SampleMatrix::~SampleMatrix() {}

// Matrix addition
SampleMatrix::DenseMatrix_Type
SampleMatrix::add(const SampleMatrix::DenseMatrix_Type &A,
                  const SampleMatrix::DiagMatrix_Type &B) {
  return A + B;
}
```

You can write the SIL function as below:

```cpp
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
```

## 3.2. Handle struct input and output.

If the C++ function takes or returns struct types, define equivalent struct in SIL C++ code.

For example, if the C++ struct is defined as below:

```cpp
namespace motor_parameters {

class Parameter {
public:
  double Lshaft = static_cast<double>(1.0);
  double dshaft = static_cast<double>(0.02);
  double shaftrho = static_cast<double>(7850.0);
  double G = static_cast<double>(81500000000.0);
  double Mmotor = static_cast<double>(100.0);
  double Rmotor = static_cast<double>(0.1);
  double Bmotor = static_cast<double>(0.1);
  double R = static_cast<double>(20.0);
  double Kt = static_cast<double>(10.0);
  double Bload = static_cast<double>(25.0);
};

using Parameter_Type = Parameter;

} // namespace motor_parameters
```

If you want to use this struct in SIL function, write as below:

```cpp
PYBIND11_MODULE(MotorSIL, m) {
  py::class_<motor_parameters::Parameter>(m, "Parameter")
      .def(py::init<>())
      .def_readwrite("Lshaft",
                     &motor_parameters::Parameter::Lshaft)
      .def_readwrite("dshaft",
                     &motor_parameters::Parameter::dshaft)
      .def_readwrite("shaftrho",
                     &motor_parameters::Parameter::shaftrho)
      .def_readwrite("G", &motor_parameters::Parameter::G)
      .def_readwrite("Mmotor",
                     &motor_parameters::Parameter::Mmotor)
      .def_readwrite("Rmotor",
                     &motor_parameters::Parameter::Rmotor)
      .def_readwrite("Bmotor",
                     &motor_parameters::Parameter::Bmotor)
      .def_readwrite("R", &motor_parameters::Parameter::R)
      .def_readwrite("Kt", &motor_parameters::Parameter::Kt)
      .def_readwrite("Bload",
                     &motor_parameters::Parameter::Bload);

  m.def(
      "update_parameters",
      [](const motor_parameters::Parameter &param) {
        lmpc.update_parameters(param);
      },
      "update motor parameters with Parameter struct");
}
```

## 4. Add Pybind11 code to Python file.

Finally, add the necessary Pybind11 import code to the Python file which user provided.

Write the code as below:

```python
from helper.SIL.SIL_operator import SIL_Operator

current_dir = os.path.dirname(__file__)
generator = SIL_Operator("sample_matrix.py", current_dir)
generator.build_SIL_code()

import SampleMatrixSIL
SampleMatrixSIL.initialize()
```

You need to import "SIL_Operator" from "SIL_Operator.py".

There must be the "SIL_Operator.py" in the repository. Please search and find it, and replace the import statement if necessary.

And there must be "*.py" in the repository. "*" is the name of the C++ file without the ".cpp" extension.

Replace "sample_matrix.py" with the name of that Python file.

There must be a line that uses class functions in the Python file.

For example, if the Python file has the following code:

```python
sm = SampleMatrix()

# Matrix addition
C = sm.add(A, B)
print("Matrix Addition, numpy result:\n", C)
```

Add the SIL code after "C = sm.add(A, B)" as below:

```python
# test C++ SIL result
C_sil = SampleMatrixSIL.add(A, B)
print("Matrix Addition, C++ SIL result:\n", C_sil)
```
