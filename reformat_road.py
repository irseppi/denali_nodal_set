import sys
import fileinput

for i, line in enumerate(fileinput.input('PARKSHIGHWAY3.txt', inplace=1)):
    sys.stdout.write(line.replace(',0', '\n')) 

