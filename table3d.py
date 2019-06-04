#!/dev/bin/python3

class table3d:
    def __init__(self, size, value = 0):
        self.size = size
        self.xaxis = [0] * size
        self.yaxis = [0] * size
        self.bins = []
        self.weigth = []
        for i in range(size):
            self.bins.append([value]*size)
            self.weigth.append([0]*size)

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
            self.bins[y1][x1] = self.bins[y1][x1] * self.weigth[y1][x1] + z * wx * wy
            self.weigth[y1][x1] += wx * wy
            self.bins[y1][x1] /= self.weigth[y1][x1]
        if wx * (1-wy) > 0:
            self.bins[y1-1][x1] = self.bins[y1-1][x1] * self.weigth[y1-1][x1] + z * wx * (1-wy)
            self.weigth[y1-1][x1] += wx * (1-wy)
            self.bins[y1-1][x1] /= self.weigth[y1-1][x1]
        if (1-wx) * wy > 0:
            self.bins[y1][x1-1] = self.bins[y1][x1-1] * self.weigth[y1][x1-1] + z * (1-wx) * wy
            self.weigth[y1][x1-1] += (1-wx) * wy
            self.bins[y1][x1-1] /= self.weigth[y1][x1-1]
        if (1-wx) * (1-wy) > 0:
            self.bins[y1-1][x1-1] = self.bins[y1-1][x1-1] * self.weigth[y1-1][x1-1] + z * (1-wx) * (1-wy)
            self.weigth[y1-1][x1-1] += (1-wx) * (1-wy)
            self.bins[y1-1][x1-1] /= self.weigth[y1-1][x1-1]
    
    def __repr__(self):
        separator = '\t'
        s = ''
        for line in self.bins:
            s2 = ''
            for value in line:
                s2 += str(round(value, 2)) + separator
            s = s2.strip(separator) + separator +'\n' + s
        return ''+ s.strip(separator+'\n') +'\n'

if __name__ == '__main__':
    t = table3d(3)
    t.xaxis = [0,1,2]
    t.yaxis = [0,1,2]
    t.put(0,2,1)
    print(t)