#!/dev/bin/python3

import sys
from table2d import table2d
from table3d import table3d
import logloader
import tableloader
import json

def get_best(values):
    bestscore = 99.9
    bestitem = None

    for v in values:
        if v[1] is not None and abs(v[1]) < bestscore:
            bestitem = v[0]
    
    return bestitem

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("missing argument: 'log.msl ve.table'")
        exit(1)

    values = logloader.load_log(sys.argv[1])
    table = tableloader.load_xml(sys.argv[2])

    try:
        f = open("data.json", 'r')
        data = json.load(f)
        f.close()
    except:
        data = {"files":[], "values":[]}
        for y in range(16):
            line = []
            for x in range(16):
                line.append([])
            data["values"].append(line)

    logname = sys.argv[1].replace('\\', '/').split('/')[-1]

    if logname in data["files"]:
        print("File already processed.")
        exit(1)

    data["files"].append(logname)

    VEtable = table3d(16, 0)
    VEtable.xaxis = table['x']
    VEtable.yaxis = table['y']
    
    AFRtable = table3d(16, 0)
    AFRtable.xaxis = table['x']
    AFRtable.yaxis = table['y']

    engineIsCold = True
    invalidAFR = 0
    for value in values:
        if engineIsCold:
            engineIsCold = value["Fuel: Warmup cor"] > 100 or value['AFR'] < 8

        elif value['Accel PW'] > 0 or value['PW'] <= 0:
            invalidAFR = 10

        elif invalidAFR == 0:
            afr = value['AFR'] * value['EGO cor1']/100
            accuracy = afr-value['AFR Target 1']

            VEtable.put(value['RPM'], value['MAP'], accuracy)
            AFRtable.put(value['RPM'], value['MAP'], value['AFR'])

        else:
            invalidAFR -= 1

    print(AFRtable)

    for y in range(16):
        for x in range(16):
            cell = data["values"][y][x]
            c = {}
            c['VE'] = table['z'][y][x]
            c['count'] = len(VEtable.bins[y][x].values)
            if VEtable.weigth(y,x) > 0:
                c['accuracy'] = round(VEtable.bins[y][x].avg(),2)
                c['std_dev'] = round(VEtable.bins[y][x].std(),2)
                
            cell.append(c)

    # tableloader.print_xml(sys.argv[2], table)

    output = open("data.json", 'w')
    json.dump(data, output, indent=2)
    output.close()
