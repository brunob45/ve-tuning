import json
import sys
import tableloader

f = open("data.json", "r")
table = json.load(f)["values"]
f.close()

class Reading:
    def __init__(self, VE):
        self.VE = VE
        self.values = []
        self.avg = 0

    def add_value(self, value):
        self.values.append(value)
        self.avg = 0
        for v in self.values:
            self.avg += v
        v /= len(self.values)
    
    def __repr__(self):
        return str(self.avg)

output = tableloader.load_xml(sys.argv[1])

class Cell:
    def __init__(self, values):
        self.values = {}
        for v in values:
            if v[1] is None:
                continue
            key = str(v[0])
            if key not in self.values.keys():
                self.values[key] = Reading(v[0])
            self.values[key].add_value(v[1])

    def is_complete(self):
        have_lower = False
        have_higher = False
        for v in self.values.values():
            if v.avg < -0.5:
                have_lower = True
            elif v.avg > 0.5:
                have_higher = True
        return have_lower and have_higher
    
    def is_exact(self):
        have_exact = False
        for v in self.values.values():
            if v.avg < 0.5 and v.avg > -0.5:
                have_exact = True
        return have_exact


for j in range(16):
    for i in range(16):
        new_value = table[j][i][0][0]
        cell = Cell(table[j][i])
        if cell.is_exact():
            bestscore = 999
            bestitem = None
            for v in cell.values.values():
                if abs(v.avg) < bestscore:
                    bestscore = abs(v.avg)
                    bestitem = (v.VE, v.avg)
            if bestitem[1] < -0.2:
                new_value = bestitem[0] - 1
            elif bestitem[1] > 0.2:
                new_value = bestitem[0] + 1
            else:
                new_value = bestitem[0]
        elif cell.is_complete():
            max_neg_item = None
            max_neg_score = -999
            min_pos_item = None
            min_pos_score = 999
            for v in cell.values.values():
                if v.avg > 0 and v.avg < min_pos_score:
                    min_pos_score = v.avg
                    min_pos_item = v.VE
                elif v.avg < 0 and v.avg > max_neg_score:
                    max_neg_score = v.avg
                    max_neg_item = v.VE
            m = (max_neg_item - min_pos_item)/(max_neg_score-min_pos_score)
            b = max_neg_item - (m*max_neg_score)
            new_value = int(round(b,0))
        else:
            bestscore = 999
            bestitem = None
            for v in cell.values.values():
                if abs(v.avg) < bestscore:
                    bestscore = abs(v.avg)
                    bestitem = (v.VE, v.avg)
            if bestitem is not None:
                new_value = int(round(bestitem[0] + bestitem[1]*3))
        output['z'][j][i] = new_value

tableloader.print_xml(sys.argv[1], output)