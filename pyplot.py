import sys
import numpy as np
import matplotlib.pyplot as plt
import json
import math

if len(sys.argv) < 2:
    print("missing argument")
    exit(1)
try:
    values = json.load(open(sys.argv[1], "r"))
except :
    print("unable to open", sys.argv[1])
    exit(2)


if len(sys.argv) < 3 or sys.argv[2] == '1':
    xbins = [600, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]
    x = [0] * len(xbins)
    ybins = [10, 16, 22, 28, 34, 40, 46, 52, 58, 64, 70, 76, 82, 88, 94, 100]
    y = [0] * len(ybins)
    z = []

    for index in range(len(x)-1):
        x[index] = (xbins[index]+xbins[index+1])/2
    x[-1] = float('inf')

    for index in range(len(y)-1):
        y[index] = (ybins[index]+ybins[index+1])/2
    y[-1] = float('inf')
    for j in range(len(y)):
        row = []
        for i in range(len(x)):
            row.append([])
        z.append(row)

    for value in values:
        if value["Fuel: Warmup cor"] > 100:
            continue

        done = False
        for j in range(len(y)):
            if value["MAP"] < y[j]:
                for i in range(len(x)):
                    if value["RPM"] < x[i]:
                        done = True
                        z[j][i].append(value)
                    if done: break
            if done: break

    fig = plt.figure()
    fig.patch.set_facecolor('xkcd:black')

    for j in range(len(y)):
        axisRow = False
        for i in range(len(x)):
            RPM = []
            MAP = []
            FIT = []
            v = sorted(z[j][i], key=lambda k: abs(k['fitness2']))
            for value in v:
                RPM.append(value["RPM"])
                MAP.append(value["MAP"])
                if "fitness2" in value.keys():
                    f = value["fitness2"]
                else:
                    f = value["fitness"]
                r = min(1, max(0, 10*f))
                g = min(1, max(0, -10*abs(f)+2))
                b = min(1, max(0, -10*f))
                FIT.append([r,g,b])
            if len(RPM) > 0 or j == len(y)-1:
                plt.subplot(len(y), len(x)+1, (len(y)-1-j)*(len(x)+1) + i+2)
                if j == len(y)-1:
                    plt.title(str(xbins[i]), color='w')
                plt.axis('off')
                if len(RPM) > 0:
                    alpha = 1/math.log(len(RPM)+1,2)
                    size = alpha*100
                    if i > 0 and i < len(x)-2: plt.xlim((x[i-1], x[i]))
                    if j > 0 and j < len(y)-2: plt.ylim((y[j-1], y[j]))
                    plt.scatter(RPM, MAP, c=FIT, s=size, alpha=min(1,alpha), edgecolors='none')

    for j in range(len(ybins)-1):
        plt.subplot(len(y), len(x)+1, (len(y)-1-j)*(len(x)+1) + 1)
        plt.title(str(ybins[j+1]), color='w')
        plt.axis('off')

    plt.show()
    exit(0)

else:
    MATx = []
    MATy = []
    CLTx = []
    CLTy = []

    for value in values:
        f = value["fitness"]

        MATx.append(value["MAT"])
        MATy.append(f)

        if value["Fuel: Warmup cor"] > 100:
            CLTx.append(value["CLT"])
            CLTy.append(f)


    plt.subplot(121)
    plt.scatter(MATx, MATy, c=MATy, s=20, alpha=0.1, edgecolors='none')
    plt.title("MAT")
    plt.grid(True)
    plt.ylim(-0.3, 0.3)

    plt.subplot(122)
    plt.scatter(CLTx, CLTy, c=CLTy, s=20, alpha=0.1, edgecolors='none')
    plt.title("CLT")
    plt.grid(True)
    plt.ylim(-0.3, 0.3)

    plt.show()