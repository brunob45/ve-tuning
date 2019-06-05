import numpy as np
import matplotlib.pyplot as plt
import json
import sys

f = open("data.json", "r")
table = json.load(f)["values"]
f.close

for j in range(16):
    for i in range(16):
        x = []
        y = []
        c = []
        # print(table[j][i])
        for z in table[j][i]:
            if z[1] is not None:
                x.append(z[0])
                y.append(abs(z[1]))
                if z[1] < 0:
                    c.append(-1)
                else:
                    c.append(1)
        if len(x) > 0:
            plt.subplot(16,16,16*(15-j)+i)
            plt.scatter(x, y, s=15, c=c)
            plt.axis([15, 100, 0, 5])


# Fixing random state for reproducibility
# np.random.seed(19680801)


# x = np.random.rand(10)
# y = np.random.rand(10)
# z = np.sqrt(x**2 + y**2)

# plt.subplot(16,16,1)
# plt.scatter(x, y, s=5)

# plt.subplot(322)
# plt.scatter(x, y, s=80, c=z, marker=(5, 0))

# verts = np.array([[-1, -1], [1, -1], [1, 1], [-1, -1]])
# plt.subplot(323)
# plt.scatter(x, y, s=80, c=z, marker=verts)

# plt.subplot(324)
# plt.scatter(x, y, s=80, c=z, marker=(5, 1))

# plt.subplot(325)
# plt.scatter(x, y, s=80, c=z, marker='+')

# plt.subplot(326)
# plt.scatter(x, y, s=80, c=z, marker=(5, 2))

plt.show()