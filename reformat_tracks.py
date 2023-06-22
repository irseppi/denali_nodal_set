import sys
import fileinput

# replace all occurrences of 'sit' with 'SIT' and insert a line after the 5th
for i, line in enumerate(fileinput.input('Alaska_Railroad.txt', inplace=1)):
    sys.stdout.write(line.replace(',', '   ')) 
    sys.stdout.write(line.replace(', 10 ', '\n')) 

