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


# Define a function to calculate the distance between two points given their latitudes and longitudes
def distance(lat1, lon1, lat2, lon2):
  # Convert degrees to radians
  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)

  # Apply the haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
  c = 2 * math.asin(math.sqrt(a))
  r = 6371 # Radius of the earth in km
  return c * r # Distance in km

# Define a function to take two different size lists of lat and lon values and compare each set of lat and lon values to all the lat and lon values in the other list and then find the shortest distance between those two points and return their index numbers
def compare_lists(list1, list2):
  # Initialize the minimum distance and the index numbers
  min_dist = float("inf")
  index1 = -1
  index2 = -1

  # Loop through the first list
  for i in range(len(list1)):
    # Get the latitude and longitude of the current point in the first list
    lat1 = list1[i][0]
    lon1 = list1[i][1]

    # Loop through the second list
    for j in range(len(list2)):
      # Get the latitude and longitude of the current point in the second list
      lat2 = list2[j][0]
      lon2 = list2[j][1]

      # Calculate the distance between the two points
      dist = distance(lat1, lon1, lat2, lon2)

      # Update the minimum distance and the index numbers if the current distance is smaller than the previous minimum distance
      if dist < min_dist:
        min_dist = dist
        index1 = i
        index2 = j

  # Return the index numbers of the two points with the shortest distance
  return index1, index2, min_dist

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


# Call the function and print the result
result = compare_lists(P1, P2)
print(result)

