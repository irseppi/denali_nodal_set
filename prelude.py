from obspy import read, UTCDateTime,read_inventory,Stream
from obspy.geodetics import gps2dist_azimuth
import obspy
from pathlib import Path
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from itertools import islice, takewhile, repeat
from tqdm.notebook import trange, tqdm
import math

STATIONS = read_inventory("/scratch/naalexeev/NODAL/stations.xml")
NODAL_PATH = Path("/scratch/naalexeev/NODAL")
EXCLUDE_STATIONS={"5575"}
for s in range(1500,1589+1):
    EXCLUDE_STATIONS.add(str(s))
BAD_FILES = {"log.txt","sql_query.sql","stations.xml"}
"""
returns true if range a has any intersection with range b
"""
def is_in_range(range_a_start,range_a_end,range_b_start,range_b_end):
    is_start = range_a_start<range_b_start and range_a_end>range_b_start
    is_end = range_a_start <range_b_end and range_a_end>range_b_end
    is_inside = range_a_start > range_b_start and range_a_end < range_b_end
    return is_start or is_end or is_inside
def bad_files():
    return BAD_FILES
def parse_filename(name):
    if name in BAD_FILES:
        return None
    name_split = name.split(".")
    start_time = UTCDateTime(name_split[0]+"."+name_split[1])
    end_time = UTCDateTime(name_split[2]+"."+name_split[3])
    station_name = name_split[4]
    return {"start_time":start_time,"end_time":end_time,"station_name":station_name}
def get_stations_in_time(start,end):
    in_range=[]
    for file in NODAL_PATH.iterdir():
        parsed = parse_filename(file.name)
        if parsed is not None:
            if is_in_range(start,end,parsed["start_time"],parsed["end_time"]):
                in_range.append(parsed)
    return in_range

def get_streams(event_time,event_lat,event_lon,buffer_time=60.0,max_dist = 130000.0):
    stations= read_inventory("/scratch/naalexeev/NODAL/stations.xml")
    non_waveform_files = bad_files()
    data_path = Path("/scratch/naalexeev/NODAL")


    selected_traces = []
    for file in data_path.iterdir():
        if not file.name in non_waveform_files:

            stem_split = file.stem.split(".")
  
            start_time = UTCDateTime(stem_split[0]+"."+stem_split[1])
            end_time = UTCDateTime(stem_split[2]+"."+stem_split[3])
            read_start = event_time-buffer_time
            read_end = event_time+buffer_time
           
            if start_time<event_time and end_time>event_time:
                read_path = data_path/file
                #print(read_path)
                stream = read(str(read_path),starttime = read_start,endtime = read_end)
                for tr in stream:
                    #rint(tr.stats)
                    seed_id = "{}.{}..{}".format(tr.stats["network"],
                                                 tr.stats["station"],
                                                 tr.stats["channel"])
                    coords = stations.get_coordinates(seed_id)
                    #rint(coords)
                    st_lat = coords["latitude"]
                    st_lon = coords["longitude"]
                    distance =gps2dist_azimuth(st_lat,st_lon,event_lat,event_lon)[0]
                    # todo: change distance to something real
                    if distance<=max_dist:
                        
                        tr.stats.distance = distance
                        selected_traces.append(tr)
                    
                    
    stream = Stream(selected_traces)
    
    return stream

def make_plane_ax():
    ax = plt.axes(projection = ccrs.PlateCarree())
    ax.stock_img()
    ax.set_xlim(left=-167,right=-123)
    ax.set_ylim(bottom = 46, top = 73)
    return ax
def plot_planes(planes,show_title=True,ax=None,figpath=None,show=True,label=None):
    if ax is None:
        ax = make_plane_ax()
    lat = []
    lon = []
    title = ""
    for e in planes:
        title = e[1]
        lat.append(e[2])
        lon.append(e[3])
        
        #print("lat: {} lon: {}".format(o.latitude,o.longitude))
    plt.scatter(lon,lat,transform=ccrs.PlateCarree(),marker=",",label=label)
    if show_title:
        plt.title(title)
    if figpath is not None:
        plt.savefig(figpath)
    if show:
        plt.show()
"""
Returns dict with keys being icao24 and items being arrays of planes
"""
def get_planes_dict(planes): 
    new_planes = {}
    for plane in planes:
        if plane[1] in new_planes:
            new_planes[plane[1]].append(plane)
        else:
            new_planes[plane[1]] = [plane]
    return new_planes
def plot_many_planes(planes,show_title=True,ax=None,figpath=None):
    new_planes = get_planes_dict(planes)
    if ax is None:
        ax = make_plane_ax()
    for plane in new_planes:
        plot_planes(new_planes[plane],ax=ax,show=False,label=plane)
    plt.legend()
    if figpath is not None:
        plt.savefig(figpath)
    plt.show()


def get_stream(sample_rate,date,stream_limit=1):
    end_time = date.replace(hour=23).replace(minute=59)
    print(date)
    print(end_time)
    traces = []
    non_waveform_files = bad_files()
    for file in NODAL_PATH.iterdir():
        if stream_limit is not None:
            if stream_limit<=len(traces):
                return Stream(traces)
        file_info = parse_filename(file.name)
        if file_info is not None:
            if is_in_range(date,end_time,file_info["start_time"],file_info["end_time"]):
                st = read(file)
                st = st.slice(date,end_time)
                if sample_rate is not None:
                    st.resample(sample_rate)
                for tr in st:
                    traces.append(tr)
    return Stream(traces)
def get_file_path(start_time,station_id):
    start_time = start_time.replace(minute=0,second=0)
    end_time = (start_time+60.0*60.0).replace(minute=0,second=0)
    file_name = "{}.{}.{}.mseed".format(start_time,end_time,station_id)
    return {"path":NODAL_PATH / file_name,"start_time":start_time,"end_time":end_time}
def get_hours_in_day(time,debug=False):
    time = time.replace(minute=0,second=0,microsecond=0)
    if debug:
        print("time: {}, second: {}".format(time,time.second))
    out_times = []
    for i in range(0,24):
        out_times.append(time.replace(hour=i))
    return out_times
def get_day_paths(time,station_id,debug=False):
    out_paths = []
    for date in get_hours_in_day(time,debug=debug):
        out_paths.append(get_file_path(date,station_id))
    return out_paths
def load_day_traces(time,station_id,debug=False):
    paths = get_day_paths(time,station_id,debug=debug)
    traces = {}
    for path in paths:
        if debug:
            print("attempting to load path: {}".format(path["path"]))
        if path["path"].exists():
            stream = read(path["path"])
            stream = stream.slice(path["start_time"],path["end_time"])
            for tr in stream:
                channel = tr.stats["channel"]
                if channel in traces:
                    traces[channel].append(tr)
                else:
                    traces[channel] = [tr]
    traces_out = {}
    for chan in traces:
        traces_out[chan] = traces[chan][0]
        for i in range(1,len(traces[chan])):
            traces_out[chan]+=traces[chan][i]
    final_traces = []
    for chan in traces_out:
        final_traces.append(traces_out[chan])
    return final_traces
def load_day(time,resample_rate=None):
    traces_out = []
    for station in STATIONS[0]:
        temp_traces = load_day_traces(time,station.code)
        if len(temp_traces)!=0:
            for tr in temp_traces:
                if resample_rate is not None:
                    tr.resample(resample_rate)
                traces_out.append(tr)
    return Stream(traces_out)

def plot_spectrogram(start_station,end_station,event_time,buffer,image_save_path = None,debug=False):
    fig,ax = plt.subplots(end_station-start_station+1,3)
    fig.set_figwidth(50.0)
    fig.set_figheight(60.0)

    for i in trange(start_station,end_station+1):
        station_day = Stream(load_day_traces(event_time,str(i),debug=debug))
        if debug:
            print(station_day)
        station_slice = station_day.slice(event_time-buffer,event_time+buffer)
        for j,tr in enumerate(station_slice):
            tr.spectrogram(axes=ax[i-start_station,j],dbscale=True)
            ax[i-start_station,j].set_title("{}.{}".format(tr.stats["station"],tr.stats["channel"]))
    if not image_save_path is None:
        plt.savefig(image_save_path)
    plt.show()
def split_every(n, iterable):
    """
    Slice an iterable into chunks of n elements
    :type n: int
    :type iterable: Iterable
    :rtype: Iterator
    """
    iterator = iter(iterable)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))
class SkipIter:
    def __init__(self,iterator,skip_num=10):
        self.iterator=iter(iterator)
        self.skip_num = skip_num
    def __iter__(self):
        return self
    def __next__(self):
        t_out = self.iterator.__next__()
        for i in range(1,self.skip_num):
            t_out = self.iterator.__next__()
        return t_out
    def __len__(self):
        return int(math.floor(len(self.iterator)/skip_num))
def get_stations_by_lat_lon():
    l = []
    for station in STATIONS[0]:
        l.append({"lat":station.latitude,"station":station,"lon":station.longitude})
    l.sort(key = lambda s: s["lat"])
    return l