# import numpy as np
import matplotlib.pyplot as plt
import json
import sys

thresh = 0.3
scatter = True

f = open("data.json", "r")
table = json.load(f)["values"]
f.close

for j in range(16):
    plt.figure(num=str(j))
    for i in range(16):
        x = []
        y = []
        c = []
        s = []
        for z in table[j][i]:
            if z[1] is not None:
                if scatter:
                    x.append(z[0])
                else:
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
            if scatter:
                plt.scatter(x, y, s=5, c=c)
                plt.axis([15, 75, -4, 4])
            else:
                plt.plot(x, y)
                plt.axis([0, len(x)+1, -5, 5])
    plt.show()

plt.show()