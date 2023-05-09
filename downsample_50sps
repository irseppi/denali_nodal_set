import faulthandler

from obspy import read
from pathlib import Path

faulthandler.enable()

def make_base_dir(base_dir):
	base_dir = Path(base_dir)
	if not base_dir.exists():
		current_path = Path("/")
		for parent in base_dir.parts:
			current_path = current_path/parent
			if not current_path.exists():
				current_path.mkdir()

for month in range(2,4):
	if month == 2:
		for day in range (11,29):
			BASE_DIR = "/home/irseppi/nodal_data/50sps/2019_0"+str(month)+"_"+str(day)
			make_base_dir(BASE_DIR)

			for z in range(0,4):
				for y in range(0,10):
					try:
						tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_1"+str(z)+str(y)+"*.msd")
						print('READ')
						
						tr_new = tr.copy()
						tr_new.resample(50)

						for x in range(len(tr_new)):
							save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
							print(save_name)

							save_path = (Path(BASE_DIR) / save_name)

							tr_new[x].write(str(save_path), format='MSEED')
							print('SAVED')
					except:
						continue

			for y in range(0,9):
				try:
					tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_15"+str(y)+"*.msd")
					print('READ')
					
					tr_new = tr.copy()
					tr_new.resample(50)

					for x in range(len(tr_new)):
						save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
						print(save_name)

						save_path = (Path(BASE_DIR) / save_name)

						tr_new[x].write(str(save_path), format='MSEED')
						print('SAVED')
				except:
					continue

			try:
				tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_5*.msd")
				print('READ')

				tr_new = tr.copy()

				tr_new.resample(50)

				for x in range(len(tr_new)):
					save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
					print(save_name)

					save_path = (Path(BASE_DIR) / save_name)

					tr_new[x].write(str(save_path), format='MSEED')  
					print('SAVED')
			except:
				continue
			try:
				ts = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_9*.msd")
				print('READ')

				ts_new = ts.copy()
				ts_new.resample(50)

				for x in range(len(ts_new)):
					save_name = BASE_DIR + "/ZE_{}_{}.msd".format(ts_new[x].stats.station,ts_new[x].stats.channel)
					print(save_name)

					save_path = (Path(BASE_DIR) / save_name)

					ts_new[x].write(str(save_path), format='MSEED')  
					print('SAVED')
			except:
				continue
	else: 
		for day in range (1,10):
			BASE_DIR = "/home/irseppi/nodal_data/50sps/2019_0"+str(month)+"_0"+str(day)
			make_base_dir(BASE_DIR)

			for z in range(0,4):
				for y in range(0,10):
					try:
						tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_0"+str(day)+"/ZE_1"+str(z)+str(y)+"*.msd")
						print('READ')

						tr_new = tr.copy()
						tr_new.resample(50)
			    
						for x in range(len(tr_new)):
							save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
							print(save_name)

							save_path = (Path(BASE_DIR) / save_name)

							tr_new[x].write(str(save_path), format='MSEED')  
							print('SAVED')
					except:
						continue
			for y in range(0,9):
				try:
					tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_0"+str(day)+"/ZE_15"+str(y)+"*.msd")
					print('READ')

					tr_new = tr.copy()
					tr_new.resample(50)
		    
					for x in range(len(tr_new)):
						save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
						print(save_name)

						save_path = (Path(BASE_DIR) / save_name)

						tr_new[x].write(str(save_path), format='MSEED')  
						print('SAVED')
				except:
					continue

			try:
				tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_0"+str(day)+"/ZE_5*.msd")
				print('READ')

				tr_new = tr.copy()

				tr_new.resample(50)

				for x in range(len(tr_new)):
					save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
					print(save_name)

					save_path = (Path(BASE_DIR) / save_name)

					tr_new[x].write(str(save_path), format='MSEED')  
					print('SAVED')

			except:
				continue

			try:
				ts = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_0"+str(day)+"/ZE_9*.msd")
				print('READ')

				ts_new = ts.copy()

				ts_new.resample(50)

				for x in range(len(ts_new)):
					save_name = BASE_DIR + "/ZE_{}_{}.msd".format(ts_new[x].stats.station,ts_new[x].stats.channel)
					print(save_name)

					save_path = (Path(BASE_DIR) / save_name)

					ts_new[x].write(str(save_path), format='MSEED')  
					print('SAVED')

			except:
				continue



		for day in range (10,27):
			BASE_DIR = "/home/irseppi/nodal_data/50sps/2019_0"+str(month)+"_"+str(day)
			make_base_dir(BASE_DIR)

			for z in range(0,4):
				for y in range(0,10):
					try:
						tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_1"+str(z)+str(y)+"*.msd")
						print('READ')

						tr_new = tr.copy()
						tr_new.resample(50)
			    
						for x in range(len(tr_new)):
							save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
							print(save_name)

							save_path = (Path(BASE_DIR) / save_name)

							tr_new[x].write(str(save_path), format='MSEED')  
							print('SAVED')
					except:
						continue
			for y in range(0,9):
				try:
					tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_15"+str(y)+"*.msd")
					print('READ')

					tr_new = tr.copy()
					tr_new.resample(50)
		    
					for x in range(len(tr_new)):
						save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
						print(save_name)

						save_path = (Path(BASE_DIR) / save_name)

						tr_new[x].write(str(save_path), format='MSEED')  
						print('SAVED')
				except:
					continue
			try:
				tr = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_5*.msd")
				print('READ')

				tr_new = tr.copy()

				tr_new.resample(50)

				for x in range(len(tr_new)):
					save_name = BASE_DIR + "/ZE_{}_{}.msd".format(tr_new[x].stats.station,tr_new[x].stats.channel)
					print(save_name)

					save_path = (Path(BASE_DIR) / save_name)

					tr_new[x].write(str(save_path), format='MSEED')  
					print('SAVED')
			except:
				continue

			try:
				ts = read("/home/irseppi/nodal_data/500sps/2019_0"+str(month)+"_"+str(day)+"/ZE_9*.msd")
				print('READ')

				ts_new = ts.copy()

				ts_new.resample(50)

				for x in range(len(tr_new)):
					save_name = BASE_DIR + "/ZE_{}_{}.msd".format(ts_new[x].stats.station,ts_new[x].stats.channel)
					print(save_name)

					save_path = (Path(BASE_DIR) / save_name)

					ts_new[x].write(str(save_path), format='MSEED')  
					print('SAVED')
			except:
				continue
					
