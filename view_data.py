# import numpy as np
import matplotlib.pyplot as plt
import json
import sys

thresh = 0.3

f = open("data.json", "r")
table = json.load(f)["values"]
f.close

for j in range(16):
    for i in range(16):
        x = []
        y = []
        c = []
        s = []
        for z in table[j][i]:
            if z[1] is not None:
                x.append(len(x)+1)
                y.append(z[1])
                if z[1] < -thresh:
                    c.append("red")
                elif z[1] > thresh:
                    c.append("blue")
                else:
                    c.append("green")
        if len(x) > 0:
            plt.subplot(1,16,i+1)
            plt.axis([0, len(x)+1, -5, 5])
            # plt.scatter(x, y, s=5, c=c)
            plt.plot(x, y)
    plt.show()

plt.show()