""" 
The following script contains tools for looking at the downloaded files and putting information about the downloaded files into a sqlite database.
"""

def parse_download_str(s):
    bad_files = {"log.txt","sql_query.sql","stations.xml"}
    if s in bad_files:
        return None
    try:
        parts = s.split(".")
        if parts[0][0:4]=="2019":
            start_time = UTCDateTime(parts[0]+"."+parts[1])
            end_time = UTCDateTime(parts[2]+"."+parts[3])
            station_id = parts[4]
            return {"start_time":start_time,"end_time":end_time,"station_id":station_id}
        else:
            return None
    except e:
        print(s)
        print(e)
        return None
parse_download_str("2019-03-07T06:00:00.000000Z.2019-03-07T07:00:00.000000Z.1236.mseed")
parse_download_str("log.txt")


conn.execute("DELETE from waveforms;")
print(conn.execute("select * from waveforms;").fetchall())
def parse_download_path(p):
    return parse_download_str(p.name)
i=0
for f in Path("/scratch/naalexeev/NODAL").iterdir():

    parsed = parse_download_path(f)

    if parsed is not None:

        conn.execute("INSERT into waveforms (station_id, start_time, end_time, path) VALUES (\"{}\", {}, {}, \"{}\");".format(
            parsed["station_id"],
            parsed["start_time"].timestamp,
            parsed["end_time"].timestamp,
            str(f)))
conn.commit()


def check_stations(start_time,end_time):
    inv = obspy.read_inventory("/scratch/naalexeev/NODAL/stations.xml")
    stations = set()
    for net in inv:
        for s in net:
  
            stations.add(s.code)
    # getting start time to be in middle of hour
    current_time = start_time
    i=0
    while current_time <=end_time:
    
            
        select_time = (current_time+20.0).timestamp

            
        exec_str = "SELECT DISTINCT station_id FROM waveforms WHERE start_time <= {} AND end_time >= {} AND path IS NOT NULL;".format(
                select_time,select_time)
     
        data = conn.execute(exec_str
                ).fetchall()
        found_stations = set()
        for row in data:
            found_stations.add(row[0])
            
            #if len(data)!=0:
        not_found_station = stations.difference(found_stations)
 
       

        for station in not_found_station:
            exec_str = "INSERT INTO waveforms (station_id,start_time, end_time, path) VALUES ('{}',{},{},NULL);".format(
                station,
                current_time.timestamp,
                current_time.timestamp+60.0*60.0)
            conn.execute(exec_str)
         
        current_time = current_time + 60.0*60.0
        conn.commit()
        
check_stations(start_time,end_time)

gaps = conn.execute("SELECT station_id,start_time from waveforms where path IS NULL ORDER BY station_id,start_time ASC LIMIT 400;").fetchall()
for (station,start_time) in gaps:
    print("{}: {}".format(station,UTCDateTime(start_time)))