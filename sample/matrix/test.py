import numpy as np
from sample_matrix import SampleMatrix


def main():
    # Create a 3x3 matrix
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

    B = np.diag([1, 2, 3])

    sm = SampleMatrix()

    # Matrix addition
    C = sm.add(A, B)
    print("Matrix Addition, numpy result:\n", C)


if __name__ == "__main__":
    main()
