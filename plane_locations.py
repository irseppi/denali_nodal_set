import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np
from obspy.geodetics import gps2dist_azimuth
from obspy.core import UTCDateTime
import datetime
import pytz
import obspy

def distance(lat1, lon1, lat2, lon2):
	dist = gps2dist_azimuth(lat1, lon1, lat2, lon2)
	dist_km = dist[0]/1000
	return dist_km

def convert_UTC_to_epoch(timestamp):
	tz_UTC = pytz.timezone('UTC')
	time_format = "%Y-%m-%d %H:%M:%S"
	naive_timestamp = datetime.datetime.strptime(timestamp, time_format)
	aware_timestamp = tz_UTC.localize(naive_timestamp)
	epoch = aware_timestamp.strftime("%s")
	return (int) (epoch)

month = str(input("What month do you want to view?(input as either 02 or 03)"))
day = str(input("What day do you want to view? (for month = 02: days 11-28 and for month = 03: days 01-26) "))
allor = str(input("Do you want to view all stations? (y or n)"))
if allor == 'n':
	print("If not what stations do you want to view?")
	sstations = float(input("Stariting station: (between 1001 and 1306) "))
	estations = float(input("Ending station: (between 1001 and 1306) "))
elif allor == 'y':
	sstations = 1001
	estations = 1306
wind = str(input("Do you want to view data for the entire state? (y or n)"))
if wind == 'n':
	print("If not enter your desired demensions.")
	min_lon = float(input("Min longitude: (between -162.5 and -142.0)"))
	max_lon = float(input("Max longitude: (between -162.5 and -142.0)"))
	min_lat = float(input("Min latitude: (between 50 and 68)"))
	max_lat = float(input("Max latitude: (between 50 and 68)"))
elif wind == 'y':
	min_lon = -162.5
	max_lon = -142.0
	min_lat = 50
	max_lat = 68
timestamp = input("Do you want to view the entire day of data? (y or n)")
if timestamp == 'n':
	s_stamp = input("What start time do you want? (HH:MM:SS)")
	e_stamp = input("What end time do you want? (HH:MM:SS)")
	s_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+s_stamp)
	e_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+e_stamp)
elif timestamp == 'y':
	s_stamp = "00:00:00"
	e_stamp = "23:59:59"
	s_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+s_stamp)
	e_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+e_stamp)
# assign directory
directory = '/scratch/irseppi/nodal_data/flightradar24/2019'+month+day+'_positions'

flight_files=[]
# iterate over files in directory
for filename in os.listdir(directory):
	f = os.path.join(directory, filename)
	
	# checking if it is a file
	if os.path.isfile(f):
		flight_files.append(f)
apro = input("Do you want to plot only timestamps that are 10km or less from the array? (y or n)")

color=[]
#Read in color text file to get different flights to be diffrent colors on map
with open('colors.txt','r') as c_in:
		for line in c_in:
			c=str(line[0:7])
			color.append(c)
#Add calculations for flight path time stamps that are 10km or less from the array or within array map bounds
# Load and plot each flight path
if apro =='y':
	# Load the seismometer location data
	seismo_data = pd.read_csv('nodes_stations.txt', sep="|")
	seismo_latitudes = seismo_data['Latitude']
	seismo_longitudes = seismo_data['Longitude']
	spec = input("Do you want to see spectrograms of the closeset stations? (y or n)")
	#Label stations
	for l in range(len(seismo_data)):
		sta = seismo_data['Station']
		
		if sstations <= sta[l] <= estations:
			# Create a scatter plot for the seismometer locations
			plt.scatter(seismo_longitudes[l], seismo_latitudes[l], c='red')
			plt.text(seismo_longitudes[l], seismo_latitudes[l], sta[l], fontsize=5)
			for i, flight_file in enumerate(flight_files):
				flight_data = pd.read_csv(flight_file, sep=",")
				flight_latitudes = flight_data['latitude']
				flight_longitudes = flight_data['longitude']
				time = flight_data['snapshot_id']
				
				#Label time stamps with epoch time
				for s in range(len(flight_data)-1):
					dist = distance(seismo_latitudes[l], seismo_longitudes[l], flight_latitudes[s], flight_longitudes[s])

					if dist <= 10:
						time = flight_data['snapshot_id']
						speed = flight_data['speed']
						alt = flight_data['altitude']

						if s_epoch <= int(time[s]) <= e_epoch and min_lat <= flight_latitudes[s] <= max_lat and min_lon <= flight_longitudes[s] <= max_lon:
							
							if spec == 'y':
								t = UTCDateTime(float(time[s]))
								print(t)
								h = datetime.datetime.fromtimestamp(time[s])
								
								h = h.hour+9
								print(h)
								h_u = str(h+1)
								station = str(sta[l])
								#print("/scratch/naalexeev/NODAL/2019-"+month+"-"+day+"T"+str(h)+":00:00.000000Z.2019-"+month+"-"+day+"T"+h_u+":00:00.000000Z."+station+".mseed")
								tr = obspy.read("/scratch/naalexeev/NODAL/2019-"+month+"-"+day+"T"+str(h)+":00:00.000000Z.2019-"+month+"-"+day+"T"+h_u+":00:00.000000Z."+station+".mseed")
								tr.trim(tr[2].stats.starttime, tr[0].stats.starttime + 60*60)
								tr[2].plot()

								print(tr[2])
								fig1, ax1 = plt.subplots()
								#fig1.set_figwidth(5.0)
								#fig1.set_figheight(4.0)
								#ax1.set_ylim([0, 100])
								tr[2].spectrogram(axes = ax1,log=False,dbscale=True,cmap='hsv')
								fig1.show()

							# Create a scatter plot for the flight path
							plt.scatter(flight_longitudes[s], flight_latitudes[s], c=color[i % len(color)])
							plt.text(flight_longitudes[s], flight_latitudes[s], time[s], fontsize=5)
							plt.text(flight_longitudes[s]+.1, flight_latitudes[s]+.1, speed[s], fontsize=5)
							plt.text(flight_longitudes[s]-.1, flight_latitudes[s]-.1, alt[s], fontsize=5)
							 
							#print(flight_file) 
		
#print map+station+distance between them+predicted arrival times use pysep to create record section of plane arrival on stations near by	 
if apro == 'n':
	for i, flight_file in enumerate(flight_files):
		flight_data = pd.read_csv(flight_file, sep=",")
		flight_latitudes = flight_data['latitude']
		flight_longitudes = flight_data['longitude']
		time = flight_data['snapshot_id']
		
		# Create a scatter plot for the flight path
		#plt.scatter(flight_longitudes, flight_latitudes, c=color[i % len(color)])

		#Label time stamps with epoch time
		for s in range(len(flight_data)-1):
			time = flight_data['snapshot_id']
			speed = flight_data['speed']
			alt = flight_data['altitude']

			if s_epoch <= int(time[s]) <= e_epoch and min_lat <= flight_latitudes[s] <= max_lat and min_lon <= flight_longitudes[s] <= max_lon:
				# Create a scatter plot for the flight path
				plt.scatter(flight_longitudes[s], flight_latitudes[s], c=color[i % len(color)])
				plt.text(flight_longitudes[s], flight_latitudes[s], time[s], fontsize=5)
				plt.text(flight_longitudes[s]+.1, flight_latitudes[s]+.1, speed[s], fontsize=5)
				plt.text(flight_longitudes[s]-.1, flight_latitudes[s]-.1, alt[s], fontsize=5)
				 
				#print(flight_file)

		
	# Load the seismometer location data
	seismo_data = pd.read_csv('nodes_stations.txt', sep="|")
	seismo_latitudes = seismo_data['Latitude']
	seismo_longitudes = seismo_data['Longitude']

	#Label stations
	for l in range(len(seismo_data)):
		sta = seismo_data['Station']
		if sstations <= sta[l] <= estations:
			# Create a scatter plot for the seismometer locations
			plt.scatter(seismo_longitudes[l], seismo_latitudes[l], c='red')
			plt.text(seismo_longitudes[l], seismo_latitudes[l], sta[l], fontsize=5)

# Set labels and title
plt.xlim(min_lon, max_lon)
plt.ylim(min_lat, max_lat)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Flight Paths and Seismometer Locations')

# Show the plot
plt.show()

#p = input("Would you want to plot out an entire flight path? (y or n)")
#if p == 'y':
#flight_p = input("Which flight do you want to plot?")
