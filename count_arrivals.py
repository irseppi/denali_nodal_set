import sys
import fileinput
import matplotlib.pyplot as plt
import numpy as np

# explicit function to return the arrival count
def numFrequency(fileName, num):
	# open file in read mode
	text = open(fileName, "r")

	# declare count variable
	count = 0
	for line in text.readlines():
		val = line.split()
		# compare each station where arrival occured
		if int(val[0]) == int(num):
			count += 1
		else:
			continue

	# return count
	return count

lab=[]	
num=[]
for x in range(1003, 1306):
	# call function
	count=numFrequency('nodalt.arrival', x)
	if count != 0:
		lab.append(str(x))
		num.append(int(count))
	else:
		continue


#plot data as histogram
fig, ax = plt.subplots()

ax.bar(lab, num)

ax.set_ylabel('Number of Arrivals')
ax.set_title('Number of Arrival Picks by Station')
ax.set_xticklabels(lab,rotation=45)

plt.show()
