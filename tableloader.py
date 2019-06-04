import xml.etree.ElementTree as ET
import sys

def load_xml(filename):
    try:
        ET.register_namespace('', "http://www.EFIAnalytics.com/:table")
        tree = ET.parse(filename)
        root = tree.getroot()

        RPM = root[2][0].text.strip().split('\n')
        for index in range(len(RPM)):
            RPM[index] = int(RPM[index])
        
        MAP = root[2][1].text.strip().split('\n')
        for index in range(len(MAP)):
            MAP[index] = int(round(float(MAP[index])))
        
        VE = root[2][2].text.strip().split('\n')
        for y in range(len(VE)):
            line = VE[y].strip().split(' ')
            for x in range(len(line)):
                line[x] = int(round(float(line[x])))
            VE[y] = line

        table = {}
        table["x"]=RPM
        table["y"]=MAP
        table["z"]=VE

        return table

    except:
        print("fichier", sys.argv[1], "inaccessible.")
        return None

def print_xml(filename, table):
    s = "\n"
    for y in range(16):
        for x in range(16):
            s += str(table['z'][y][x]) + '.0 '
        s += '\n'
    
    try:
        ET.register_namespace('', "http://www.EFIAnalytics.com/:table")
        tree = ET.parse(filename)
        root = tree.getroot()
        VE = root[2][2].text = s
        tree.write(filename, encoding="utf-8", xml_declaration=True)
    except:
        print("failed to save new table into", filename)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Speficier un fichier.")
        exit(1)
    table = load_xml(sys.argv[1])
    print(table)
