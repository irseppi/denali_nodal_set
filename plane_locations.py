import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

# assign directory
directory = '/scratch/irseppi/nodal_data/flightradar24/20190220_positions'

flight_files=[]
# iterate over files in directory
for filename in os.listdir(directory):
	f = os.path.join(directory, filename)

	# checking if it is a file
	if os.path.isfile(f):
		flight_files.append(f)

color=[]
with open('colors.txt','r') as c_in:
		for line in c_in:
			c=str(line[0:7])
			color.append(c)

# Load and plot each flight path
for i, flight_file in enumerate(flight_files):
	flight_data = pd.read_csv(flight_file, sep=",")
	flight_latitudes = flight_data['latitude']
	flight_longitudes = flight_data['longitude']
	time = flight_data['snapshot_id']

	# Create a scatter plot for the flight path
	plt.scatter(flight_longitudes, flight_latitudes, c=color[i % len(color)])

	#Label time stamps with epoch time
	for s in range(len(flight_data)-1):
		time = flight_data['snapshot_id']
		plt.text(flight_longitudes[s], flight_latitudes[s], time[s], fontsize=6)

# Load the seismometer location data
seismo_data = pd.read_csv('nodes_stations.txt', sep="|")
seismo_latitudes = seismo_data['Latitude']
seismo_longitudes = seismo_data['Longitude']

# Create a scatter plot for the seismometer locations
plt.scatter(seismo_longitudes, seismo_latitudes, c='red', label='Seismometers')
plt.text(seismo_longitudes, seismo_latitudes, seismo_data['Station'], fontsize=6)

# Set labels and title
plt.xlim(-150.5,-148.5)
plt.ylim(62.2, 64.6)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Flight Paths and Seismometer Locations')
plt.legend()

# Show the plot
plt.show()
