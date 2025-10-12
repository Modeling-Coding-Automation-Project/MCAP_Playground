import numpy as np


class MyFunc:
    def __init__(self, x):
        self.x = x

    def compute(self):
        return np.sin(self.x) + np.cos(self.x)
