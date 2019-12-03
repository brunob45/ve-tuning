#!/usr/bin/env python3

from tablecell import tableCell

class table3d:
    def __init__(self, size, value = 0):
        self.size = size
        self.xaxis = [0] * size
        self.yaxis = [0] * size
        self.bins = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(tableCell())
            self.bins.append(row)

    def put(self, x, y, z):
        x1 = -1
        for index in range(self.size):
            if x < self.xaxis[index]:
                x1 = index
                break
        wx = 1-(self.xaxis[x1]-x)/(self.xaxis[x1]-self.xaxis[x1-1])

        y1 = -1
        for index in range(self.size):
            if y < self.yaxis[index]:
                y1 = index
                break
        wy = 1-(self.yaxis[y1]-y)/(self.yaxis[y1]-self.yaxis[y1-1])


        if wx * wy > 0:
            self.bins[y1][x1].put(z, wx * wy)
        if wx * (1-wy) > 0:
            self.bins[y1-1][x1].put(z, wx * (1-wy))
        if (1-wx) * wy > 0:
            self.bins[y1][x1-1].put(z, (1-wx) * wy)
        if (1-wx) * (1-wy) > 0:
            self.bins[y1-1][x1-1].put(z, (1-wx) * (1-wy))
    
    def weigth(self, y, x):
        return self.bins[y][x].weigth

    def __repr__(self):
        separator = '\t'
        s = ''
        for line in self.bins:
            s2 = ''
            for value in line:
                s2 += str(round(value.trust(), 2)) + separator
            s = s2.strip(separator) + separator +'\n' + s
        return ''+ s.strip(separator+'\n') +'\n'

if __name__ == '__main__':
    t = table3d(3)
    t.xaxis = [0,1,2]
    t.yaxis = [0,1,2]
    t.put(0,2,1)
    print(t)