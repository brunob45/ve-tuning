import sys

def load_log(filename):
    try:
        inputfile = open(filename, "r", encoding='latin-1')
        
        tunerstudio = len(inputfile.readline()) > 32 # ECU signature, unused
        inputfile.readline() # Log timestamp, unused
        titles = inputfile.readline().strip().split('\t')
        inputfile.readline() # Units, unused

        values = []

        for line in inputfile:
            capture = line.strip().replace(',', '.').split('\t')
            if len(titles) == len(capture):
                value = {}
                for index in range(len(capture)):
                    value[titles[index]] = float(capture[index])
                values.append(value)

        return values
    except:
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("missing argument")
        exit(1)
        
    print(load_log(sys.argv[1]))