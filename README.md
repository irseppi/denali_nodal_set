# Denali Nodal Set Data
This repository contains code used to look at the denali nodal set and attempt to find planes in the sismic signals.

## Code Orginization

Most of the code is contained inside of jupyter notebooks aside from prelude.py which contains shared functions usefull for looking at the data.

## Environment

The code uses the following packages, inorder to run the code install the latest version of each of the packages

- obspy for reading sismic data

- matplotlib for custom plotting

- numpy for manupulating arrays

- cartopy

- tqdm, used to display progress bars on long compute tasks

- scipy

## Downloading the Denali Nodal Set Data

The Delai Nodal set was downloaded from IRIS's PH5 archive using obspy. There was a bug in either obspy or in IRIS so the fast mass downloader could not be used. I wrote a customized downloader that saves which files were downloaded and some associated metadata into a sqlite3 database. The script runs very slowly on the GI's Lungs machines likely due to a network bottleneck. The script also supports being stopped and resumed at its stopping point if needed.


## Planes Data

Currently the planes data is from opensky, a volunteer run database of locations of planes based on listing to plane transponders. This data only covers a region over Anchorage. Another flight databse exists but it is expensive, <https://www.flightradar24.com/>. Another issue to keep in mind is that is likely that all flight databases will have significant holes as not all aircraft has transponders and I have not seen many military air craft on flightradar24, which does not appear to match what I have anacdotally seen in Alaska. 

### Getting data from OpenSky

First Carl Taipe applied for data access from <https://opensky-network.org/> and then the data was scraped from the provided sql database. I then wrote a parser in rust inorder to put the data into a sqllite database. The parser was written in rust because python would not be performant enough to parse the data in a timely manner. 
