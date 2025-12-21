import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import numpy as np
from sample_matrix import SampleMatrix

from helper.SIL.SIL_operator import SIL_Operator

current_dir = os.path.dirname(__file__)
generator = SIL_Operator("sample_matrix.py", current_dir)
generator.build_SIL_code()

# import MyFuncSIL
# MyFuncSIL.initialize()


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
