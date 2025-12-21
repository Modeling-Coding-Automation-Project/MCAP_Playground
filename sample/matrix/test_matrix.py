import numpy as np


def main():
    # Create a 3x3 matrix
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

    B = np.diag([1, 2, 3])

    # Matrix addition
    C = A + B
    print("Matrix Addition, numpy result:\n", C)


if __name__ == "__main__":
    main()
