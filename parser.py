#!/usr/bin/env python3

import sys
import json
import logloader
import tableloader

afrReady = False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("missing argument")
        exit(1)

    values = logloader.load_log(sys.argv[1])
    table = tableloader.load_xml(sys.argv[2])

    newLog = []

    for value in values:
        newLine = {}

        if value["AFR"] < 10:
            if value["PW"] <= 0:
                afrReady = False
            if not afrReady:
                continue
        else:
            afrReady = True

        for title in ["Time", "RPM", "MAP", "TPS", "AFR", "MAT", "CLT", "EGO cor1", "Fuel: Air cor", "PW", "Fuel: Warmup cor", "Fuel: Baro cor", "Fuel: Total cor", "Fuel: Accel enrich", "Accel PW", "VE1", "MAPdot", "RPMdot", "AFR Target 1"]:
            newLine[title] = value[title]
        newLine["Sync"] = (int(value["status1"]) & 8 == 8)
        newLine["fitness"] = (newLine["AFR"] - newLine["AFR Target 1"]) / newLine["AFR Target 1"]
        newLine["VE Target"] = round(newLine["VE1"] * (1+newLine["fitness"]),1)

        newLog.append(newLine)

    output = open(sys.argv[1] + ".json", "w+")
    json.dump(newLog, output, indent=4, sort_keys=True, separators=(',', ': '))

