import sys
import numpy as np
import matplotlib.pyplot as plt
import json

if len(sys.argv) < 2:
    print("missing argument")
    exit(1)
try:
    values = json.load(open(sys.argv[1], "r"))
except :
    print("unable to open", sys.argv[1])
    exit(2)

RPM = []
MAP = []
VEc = []
MAT = []
CLT = []
FIT = []
size = []

for value in values:
    f = value["fitness"]

    if value["Fuel: Warmup cor"] <= 100:
        RPM.append(value["RPM"])
        MAP.append(value["MAP"])
        r = min(1, max(0, f * 5))
        g = min(1, max(0, 1-abs(f * 5)))
        b = min(1, max(0, -f * 5))
        VEc.append([r,g,b])

    MAT.append(value["MAT"])
    CLT.append(value["CLT"])
    FIT.append(f)


plt.subplot(131)
plt.scatter(MAT, FIT, c=FIT, s=20, alpha=0.1, edgecolors='none')
plt.title("MAT")
plt.grid(True)
plt.ylim(-0.3, 0.3)

plt.subplot(132)
plt.scatter(CLT, FIT, c=FIT, s=20, alpha=0.1, edgecolors='none')
plt.title("CLT")
plt.grid(True)
plt.ylim(-0.3, 0.3)

plt.subplot(133)
plt.scatter(RPM, MAP, c=VEc, s=20, alpha=0.1, edgecolors='none')
plt.title("VE")
plt.grid(True)

plt.show()