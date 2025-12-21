import numpy as np


class SampleMatrix:
    def __init__(self):
        self.data = None

    def add(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        self.data = A + B
        return self.data
