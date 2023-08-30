import sys
import fileinput
import matplotlib.pyplot as plt
import numpy as np
import obspy
from obspy.core import UTCDateTime
import datetime

# open file in read mode
text = open("nodal_arr.arrival", "r")

day_data=[]	
night_data=[]

for line in text.readlines():
	val = line.split()
	# compare each station where arrival occured
	timestamps = UTCDateTime(float(val[1]))
	#print(timestamps)


	for x in range(11,29):

		if x <= 28:
			# Set the start and end times for the day and night periods
			day_start = UTCDateTime("2019-02-"+str(x-1)+"T15:00:00")
			day_end = UTCDateTime("2019-02-"+str(x)+"T08:08:00")
			night_start = UTCDateTime("2019-02-"+str(x)+"T08:00:00")
			night_end = UTCDateTime("2019-02-"+str(x)+"T15:00:00")
			# Filter the data to only include the day and night periods
			if day_start <= timestamps < day_end:
				day_data.append(timestamps)
			if night_start <= timestamps < night_end:
				night_data.append(timestamps)
		


		
	for y in range(2,27):
		day_start = UTCDateTime("2019-03-"+str(y-1)+"T15:00:00")
		day_end = UTCDateTime("2019-03-"+str(y)+"T08:00:00")
		night_start = UTCDateTime("2023-03-"+str(y)+"T08:00:00")
		night_end = UTCDateTime("2023-03-"+str(y)+"T15:00:00")

		# Filter the data to only include the day and night periods
		if day_start <= timestamps < day_end:
			day_data.append(timestamps)
		if night_start <= timestamps < night_end:
			night_data.append(timestamps)

	x = str(x)
	day_start = UTCDateTime("2019-02-28T15:00:00")
	day_end = UTCDateTime("2019-02-01T08:00:00")
	night_start = UTCDateTime("2023-03-01T08:00:00")
	night_end = UTCDateTime("2023-03-01T15:15:00")
	if day_start <= str(timestamps) < day_end:
		day_data.append(timestamps)
	if night_start <= str(timestamps) < night_end:
		night_data.append(timestamps)	

# Calculate the arrival times for the day and night periods
day_arrivals = len(day_data)
night_arrivals = len(night_data)

# Compare the arrival times between day and night
print("# of Day arrivals:", day_arrivals)
print("# of Night arrivals:", night_arrivals)
#print("Total # of picks",len(text.readlines()))
#wc -l filename.arrivals in Linux
#plot data as histogram
fig, ax = plt.subplots()

ax.bar(day_arrivals, night_arrivals)

ax.set_ylabel('Number of Arrivals')
ax.set_title('Number of Arrival Picks Night vs. Day')
#ax.set_xticklabels(timestamps,rotation=45)

plt.show()
