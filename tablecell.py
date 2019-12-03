#!/dev/bin/env python3

import numpy as np

class tableCell:
    def __init__(self, value=0):
        self.sum = value
        self.weigth = 0
        self.values = []
    
    def put(self, value, weigth):
        if weigth > 0:
            self.values.append(value)
            self.sum = (self.sum * self.weigth) + (value * weigth)
            self.weigth += weigth
            self.sum /= self.weigth

    def avg(self):
        return self.sum

    def std(self):
        return np.std(self.values)

    def trust(self):
        if len(self.values) <= 1:
            return 0
        return np.log(len(self.values) / self.std())
