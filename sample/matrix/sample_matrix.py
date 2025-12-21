import numpy as np


class SampleMatrix:
    def __init__(self):
        self._data = None

    def add(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        self._data = A + B
        return self._data
