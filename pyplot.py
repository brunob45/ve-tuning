import sys
import numpy as np
import matplotlib.pyplot as plt
import xml

if len(sys.argv) < 2:
    print("missing argument")
    exit(1)
try: inputfile = open(sys.argv[1], "r")
except :
    print("unable to open", sys.argv[1])
    exit(2)

inputfile.readline() # ECU signature, unused
inputfile.readline() # Log timestamp, unused
titles = inputfile.readline().strip().split('\t')
inputfile.readline() # Units, unused

values = []
RPM = []
MAP = []
AFR = []
size = []

for line in inputfile:
    capture = line.strip().replace(',', '.').split('\t')
    if len(titles) == len(capture):
        value = {}
        for index in range(len(capture)):
            value[titles[index]] = float(capture[index])
        if len(values) > 0 or value['AFR'] > 8:
            if(value['TPS'] > 1):
                values.append(value)
                RPM.append(value['RPM'])
                MAP.append(value['MAP'])
                afr = value['AFR'] * value['EGO cor1']/100
                afrtgt = value['AFR Target 1']
                v = afr-afrtgt
                # print(afr, afrtgt, v)
                # exit(0)
                if v < -0.5:
                    AFR.append(-0.5)
                elif v > 0.5:
                    AFR.append(0.5)
                else:
                    AFR.append(v)
                #size.append(min(0.5, abs(v)) * 4 + 2)
                size.append(3)


fig, ax = plt.subplots()
ax.scatter(RPM, MAP, c=AFR, s=size, alpha=0.75, edgecolors='none')
ax.grid(True)
plt.show()