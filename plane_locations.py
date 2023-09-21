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

#Pick date to view
g ='g'
while g == 'g':
	month = str(input("What month do you want to view?(input as either 02 or 03)"))
	if month == '02':
		day = str(input("What day do you want to view? (days available: 11-28) "))
		if 11 <= int(day) <= 28:
			g = 'f'
		else:
			print("For February you may only choose between days 11-28")
	elif month == '03':
		day = str(input("What day do you want to view? (days available: 01-26) "))
		if 1 <= int(day) <= 26:
			g = 'f'
		else:
			print("For March you may only choose between days 01-26")
	else:
		print("Must be either 02 or 03")
		g = 'g'

#Find what stations to view
allor = str(input("Do you want to view all stations? (y or n)"))
if allor == 'n':
	print("If not what stations do you want to view?")
	while allor == 'n':
		sstations = float(input("Stariting station: (between 1001 and 1306) "))
		estations = float(input("Ending station: (between 1001 and 1306) "))
		if 1001 <= sstations <= 1306 and 1001 <= sstations <= 1306 and sstations < estations:
			allor = 'm'
		else:
			allor = 'n'
			print("Not an option, what station between 1001 and 1306?")	
elif allor == 'y':
	sstations = 1001
	estations = 1306

#Find the boundaries of the region user is looking at
wind = str(input("Do you want to view data for the entire state? (y or n)"))
if wind == 'n':
	print("If not enter your desired demensions.")
	while wind == 'n':
		min_lon = float(input("Min longitude: (between -162.5 and -142.0)"))
		max_lon = float(input("Max longitude: (between -162.5 and -142.0)"))
		if -162.5 <= min_lon <= -142.0 and -162.5 <= max_lon <= -142.0 and min_lon < max_lon:
			wind = 'g'
			wh = 'p'
			while wh == 'p':
				min_lat = float(input("Min latitude: (between 50 and 68)"))
				max_lat = float(input("Max latitude: (between 50 and 68)"))
				if 50 <= min_lat <= 68 and 50 <= max_lat <= 68 and min_lat < max_lat:
					wh = 'g'
				else:
					print("Not an option:lat must be between 50 and 68")
					wh = 'p'	
		else:
			print("Not an option:lon must be between -162.5 and -142")
			wind = 'n'
elif wind == 'y':
	min_lon = -162.5
	max_lon = -142.0
	min_lat = 50
	max_lat = 68

#Find the time frame
timestamp = input("Do you want to view the entire day of data? (y or n)")
if timestamp == 'n':
	format = "%H:%M:%S"
	while timestamp == 'n':
		s_stamp = input("What start time do you want? (HH:MM:SS)")
		# checking if format matches the date
		res1 = True
	 
		# using try-except to check for truth value
		try:
	    		res1 = bool(datetime.datetime.strptime(s_stamp, format))
		except ValueError:
	    		res1 = False
		if res1==False:
			timestamp = 'n'
			#printing result
			print("Does not  match date format: HH:MM:SS")
		if res1==True:
			timestamp = 'g'
			while timestamp == 'g':
				e_stamp = input("What end time do you want? (HH:MM:SS)")
				res2 = True
				try:
					res2 = bool(datetime.datetime.strptime(e_stamp, format))
					
				except ValueError:
					res2 = False
					timestamp = 'g'
					print("Does not  match date format: HH:MM:SS")
				if res2==True:
					s_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+s_stamp)
					e_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+e_stamp)
					if s_epoch < e_epoch:
				
						timestamp = 't'
					else: 
						print("The start time must be earlier than the end time.")
						timestamp = 'n'
elif timestamp == 'y':
	s_stamp = "00:00:00"
	e_stamp = "23:59:59"
	s_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+s_stamp)
	e_epoch = convert_UTC_to_epoch("2019-"+month+"-"+day+" "+e_stamp)

# assign directory
directory = '/scratch/irseppi/nodal_data/flightradar24/2019'+month+day+'_positions'

flight_files=[]
filenames = []
# iterate over files in directory
for filename in os.listdir(directory):
	filenames.append(filename)
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
close_flights=[]

# Load and plot each flight path
if apro =='y':
	# Load the seismometer location data
	seismo_data = pd.read_csv('nodes_stations.txt', sep="|")
	seismo_latitudes = seismo_data['Latitude']
	seismo_longitudes = seismo_data['Longitude']
	seismo_stations = seismo_data['Latitude']
	sta = seismo_data['Station']

	for i, flight_file in enumerate(flight_files):
		flight_data = pd.read_csv(flight_file, sep=",")
		flight_latitudes = flight_data['latitude']
		flight_longitudes = flight_data['longitude']
		time = flight_data['snapshot_id']
		speed = flight_data['speed']
		alt = flight_data['altitude']
		x = 'h'

		while x == 'h': 
			for s in range(len(flight_data)-1):
				for l in range(len(seismo_data)):
					if sstations <= sta[l] <= estations:
						station = str(sta[l])
						dist = distance(seismo_latitudes[l], seismo_longitudes[l], flight_latitudes[s], flight_longitudes[s])
						if dist <= 5:
							if s_epoch <= int(time[s]) <= e_epoch and min_lat <= flight_latitudes[s] <= max_lat and min_lon <= flight_longitudes[s] <= max_lon:
								t = UTCDateTime(float(time[s]))
								ht = datetime.datetime.fromtimestamp(time[s])
								h = ht.hour+9
								
								if month == '03' and int(date) > 12:
									h = ht.hour+8
								h_u = str(h+1)
								print("Wait for map")
								print("In file "+filenames[i]+":")
								fig = plt.figure()
								# Create a scatter plot for the seismometer locations
								for sd in range(len(seismo_data)):
									plt.scatter(seismo_longitudes[sd], seismo_latitudes[sd], c='red')
								for fd in range(len(flight_data)-1):
									plt.scatter(flight_longitudes[fd], flight_latitudes[fd], c=color[i % len(color)])
								for stations_up in range(len(seismo_data)):
									for flights_up in range(len(flight_data)-1):
										dist = distance(seismo_latitudes[stations_up], seismo_longitudes[stations_up], flight_latitudes[flights_up], flight_longitudes[flights_up])
										if dist <= 5:
											htn = str(UTCDateTime(float(time[flights_up])))
											htnn = datetime.datetime.fromtimestamp(time[flights_up])
											#here you see spectrograms add flight data (ie. return type of plane, speed, altitude approximate arrival over station(plot as line on spectrogram	
											t = UTCDateTime(float(time[s]))
											ht = datetime.datetime.fromtimestamp(time[s])
											h = ht.hour+9
											if month == '03' and int(date) > 12:
												h = ht.hour+8
											h_u = str(h+1)
											
											print("Station", sta[stations_up], "is", dist,"km away from the nearest time stamp at time "+htn)
											
											
											#Label stations
											plt.text(seismo_longitudes[stations_up], seismo_latitudes[stations_up], sta[stations_up], fontsize=5)
											
											plt.scatter(seismo_longitudes[stations_up], seismo_latitudes[stations_up], c='pink')
											#Label time stamps with epoch time
											plt.text(flight_longitudes[flights_up], flight_latitudes[flights_up], htn, fontsize=5)
											plt.scatter(flight_longitudes[flights_up], flight_latitudes[flights_up], c='orange')
											xx = np.vstack([seismo_longitudes[stations_up], seismo_latitudes[stations_up]])
											yy = np.vstack([flight_longitudes[flights_up],flight_latitudes[flights_up]])
											plt.plot(xx,yy, '-.', c='orange')

								
								# Set labels and title
								plt.xlim(-153, -142)
								plt.ylim(60, 65)
								plt.xlabel('Longitude')
								plt.ylabel('Latitude')
								plt.title(filenames[i])	
								plt.show(block=False)
								
								spect = input("Do you want to see a spectrogram? (y or n)")
								#add arival over location here
								while spect =='y':
									sta_spec = input("What station do you want to see a spectrogram of?")
									n = "/scratch/naalexeev/NODAL/2019-"+month+"-"+day+"T"+str(h)+":00:00.000000Z.2019-"+month+"-"+day+"T"+h_u+":00:00.000000Z."+str(sta_spec)+".mseed"
									if os.path.isfile(n):
										tr = obspy.read(n)
										tr.trim(tr[2].stats.starttime + int(str(htnn.minute))*60 - 300+int(str(htnn.second)), tr[2].stats.starttime + int(str(htnn.minute))*60 + 300+int(str(htnn.second)))
										fig1, ax1 = plt.subplots()
										#fig1.set_figwidth(5.0)
										#fig1.set_figheight(4.0)
										#ax1.set_ylim([0, 100])
										tr[2].spectrogram(axes = ax1,log=False,dbscale=True,cmap='hsv')
										fig1.show()

										# Show the plot
										tr[2].plot()
										stat = input("Do you want to see stats for the nearest timestamps? (y or n)")
										if stat == 'y':
											print("The plane is traveling at an altitude of", alt[s], "at ", speed[s] ,"km per hour.")

									spect = input("Would you like to view another station? (y or n)")
									x = 'x'
						x = 't'
							
#print map+station+distance between them+predicted arrival times use pysep to create record section of plane arrival on stations near by	 
if apro == 'n':
	for i, flight_file in enumerate(flight_files):
		flight_data = pd.read_csv(flight_file, sep=",")
		flight_latitudes = flight_data['latitude']
		flight_longitudes = flight_data['longitude']
		time = flight_data['snapshot_id']

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
				 

		
	

	# Set labels and title
	plt.xlim(min_lon, max_lon)
	plt.ylim(min_lat, max_lat)
	plt.xlabel('Longitude')
	plt.ylabel('Latitude')
	plt.title('Flight Paths and Seismometer Locations')

	# Show the plot
	plt.show()

p = input("Would you want to plot out an entire flight path? (y or n)")
if p == 'y':
	flight_p = input("Which flight do you want to plot?")
	for filename in os.listdir(directory):
		f="2019"+month+day+"_"+str(flight_p)+".csv"
		f = os.path.join(directory, f)
		flight_data = pd.read_csv(f, sep=",")
		flight_latitudes = flight_data['latitude']
		flight_longitudes = flight_data['longitude']
		time = flight_data['snapshot_id']

		#Label time stamps with epoch time
		for s in range(len(flight_data)-1):
			time = flight_data['snapshot_id']
			speed = flight_data['speed']
			alt = flight_data['altitude']

			# Create a scatter plot for the flight path
			plt.scatter(flight_longitudes[s], flight_latitudes[s], c=color[i % len(color)])
			plt.text(flight_longitudes[s], flight_latitudes[s], time[s], fontsize=5)
			plt.text(flight_longitudes[s]+.1, flight_latitudes[s]+.1, speed[s], fontsize=5)
			plt.text(flight_longitudes[s]-.1, flight_latitudes[s]-.1, alt[s], fontsize=5)
				 

		
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
	plt.title("Flights on")

	# Show the plot
	plt.show()
