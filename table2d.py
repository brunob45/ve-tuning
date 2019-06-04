#!/dev/bin/python3

class table2d:
    def __init__(self, size):
        self.size = size
        self.axe = [0] * size
        self.bins = [0] * size
        self.weigth = [0] * size
        self.min = (0, float('inf'))
        self.max = (0, float('-inf'))
    
    def put(self, x, y):
        if y < self.min[1]:
            self.min = (x, y)
        if y > self.max[1]:
            self.max = (x, y)

        x1 = -1
        for index in range(self.size):
            if x < self.axe[index]:
                x1 = index
                break

        w = 1-(self.axe[x1]-x)/(self.axe[x1]-self.axe[x1-1])
        if w > 0:
            self.bins[x1] = self.bins[x1] * self.weigth[x1] + y * w
            self.weigth[x1] += w
            self.bins[x1] /= self.weigth[x1]

        if x1 > 0:
            self.bins[x1-1] = self.bins[x1-1] * self.weigth[x1-1] + y * (1-w)
            self.weigth[x1-1] += 1-w
            self.bins[x1-1] /= self.weigth[x1-1]
    
    def __repr__(self):
        s = ""
        for index in range(self.size):
            s += str(round(self.axe[index],2)) + '\t' + str(round(self.bins[index],2)) + '\n'
        s += 'min:' + str(self.min) + ', max:' + str(self.max)
        return s

    def __getitem__(self, key):
        x1 = -1
        for index in range(self.size):
            if key < self.axe[index]:
                x1 = index
                break

        w = 1-(self.axe[x1]-key)/(self.axe[x1]-self.axe[x1-1])
        if x1 <= 0:
            return self.bins[x1]
        else:
            return self.bins[x1] * w + self.bins[x1-1] * (1-w)



if __name__ == '__main__':
    table = table2d(5)
    for index in range(table.size):
        table.axe[index] = index+1
    table.put(0, 2)
    print(table)
    table.put(2, 1)
    print(table)
    print(table[1.5])

