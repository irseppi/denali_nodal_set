# Import the libraries
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, asin
import geopandas as gpd 
import fiona
from shapely.geometry import MultiLineString
import shapely.wkt
from shapely.geometry import Point
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import math

# Define a function to calculate the distance between two points in km
def haversine(p1, p2):
    # Convert the coordinates to radians
    lat1, lon1 = map(radians, p1)
    lat2, lon2 = map(radians, p2)

    # Calculate the differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Apply the haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371 # Earth radius in km
    return c * r


# IMPORT KML DRIVER
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

# READ KML file to a geopandas dataframe 
geo_df1 = gpd.read_file('ZE_NODAL.kml',driver='LIBKML')
geo_df2 = pd.read_csv('Alaska_Railroad.txt', sep=r"\s{2,}", engine="python", header=None)

# Create Pandas Dataframe from GeoPandas 
df1= pd.DataFrame(geo_df1)
df2= pd.DataFrame(geo_df2)

# Create GeoDataframe from GeoPandas
gdf1 = GeoDataFrame(df1) 
gdf2 = GeoDataFrame(df2)

gdf1 = gdf1.set_geometry("geometry")
boroughs_4326 = gdf1.to_crs("EPSG:4326")
boroughs_4326.crs

#Extract lat and lon
gdf1['lon'] = gdf1["geometry"].x
gdf1['lat'] = gdf1["geometry"].y

gdf2['lon'] = gdf2[0]
gdf2['lat'] = gdf2[1]

# Extract the coordinates as arrays
P1 = [gdf1['lat'].to_numpy(),gdf1['lon'].to_numpy()]
P2 = [gdf2['lat'].to_numpy(),gdf2['lon'].to_numpy()]

print("P1=\n",P1)
print("P2=\n",P2)

P1_rad = np.radians(P1)
P2_rad = np.radians(P2)

dlat = P1_rad[:,0,None] - P2_rad[:,0]
dlon = P1_rad[:,1,None] - P2_rad[:,1]

# Apply the haversine formula in a vectorized way
a = np.sin(dlat / 2) ** 2 + np.cos(P1_rad[:,0,None]) * np.cos(P2_rad[:,0]) * np.sin(dlon / 2) ** 2
c = 2 * np.arcsin(np.sqrt(a))
r = 6371 # Earth radius in km
D = c * r # Distance matrix

min_dist = D.min()
row, col = np.unravel_index(D.argmin(), D.shape)

print(f'The shortest distance is {min_dist:.3f} km between point {row} in ZE_NODAL.kml and point {col} in Alaska_Railroad.kml.')

