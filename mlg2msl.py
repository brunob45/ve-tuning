#!/usr/bin/env python3

import sys
import struct

columns = []

#open datalog file
if len(sys.argv) < 2:
    print("Set file as argument")
    exit(0)

try:
    input_file = open(sys.argv[1], "rb")
except:
    print("Set valid file as argument")
    exit(0)

output_file = open("output.msl", "w")
values = input_file.read(7+13)

#decode column titles
ncol = int.from_bytes(input_file.read(2), 'big')

for _ in range(ncol):
    l = int.from_bytes(input_file.read(1), 'big')

    if l == 0: #bitfield
        l = 1

    title = input_file.read(34).decode('ascii').strip('\0')

    units = input_file.read(11).decode('ascii').strip('\0')

    input_file.read(4)

    d = int.from_bytes(input_file.read(5), "big")

    columns.append((title, units, d, l))

#decode title
byte = input_file.read(1)
while byte and byte != b'\n':
    output_file.write(byte.decode('ascii'))
    byte = input_file.read(1)
output_file.write('\n')

#decode timestamp
byte = input_file.read(1)
while byte and byte != b'\n':
    output_file.write(byte.decode('ascii'))
    byte = input_file.read(1)

#write titles to output file
first = True
for col in columns:
    t = col[0]
    if first:
        output_file.write('\n')
        first = False
    else:
        output_file.write('\t')
    output_file.write(t)

#write units to output file
first = True
for col in columns:
    u = col[1]
    if first:
        output_file.write('\n')
        first = False
    else:
        output_file.write('\t')
    output_file.write(u)

#decode values
while True:
    values = input_file.read(5)
    if len(values) < 5:
        break

    first = True
    for col in columns:
        if first:
            output_file.write('\n')
            first = False
        else:
            output_file.write('\t')

        if col[3] == 7:
            v = struct.unpack('>f', input_file.read(4))[0]
            v = round(v, col[2])
            output_file.write(str(v))

        elif col[3] == 3:
            v = struct.unpack('>h', input_file.read(2))[0]
            v /= 10**col[2]
            output_file.write(str(v))

        else:
            values = input_file.read(col[3])
            v = int.from_bytes(values, "big")/(10**col[2])
            output_file.write(str(v))
