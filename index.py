from multiprocessing.sharedctypes import Value
from operator import ge
import folium
from numpy import append
import requests
import json

map = folium.Map(location=[39.8283, -98.5795], zoom_start=3, tiles="Stamen Terrain")

fg = folium.FeatureGroup(name="My Map")

#for coordinates in [[38.2, -99.1],[39.2, -97.1]]:
    #fg.add_child(folium.Marker(location=coordinates, popup="Hello, I am a Marker", icon=folium.Icon(color='green')))

#map.add_child(fg)

#map.save("Map1.html")


# ----- Request data of earthquakes and store it in a JSON file named eqs.json -----
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson" # Request json data of all earthquakes in the last hour
r = requests.get(URL)
requested_data = r.json()

eqData = 'eqs.json'
with open(eqData, 'w') as filetowrite:
    json.dump(requested_data, filetowrite, indent=4)



# Read JSON file and parse out data for markers
f_open = open('eqs.json') # open the file

data = json.load(f_open) # return JSON object as a dict

list_of_earthquakes = {} # list of earthquakes
eqid = 0

for features in data['features']:
    x = features['properties']
    z = features['geometry']

    eqid += 1
    mag = x.get('mag')
    coordinates = z.get('coordinates')
    title = x.get('title')
   
    list_of_earthquakes.setdefault(eqid, []).append(mag)
    list_of_earthquakes.setdefault(eqid, []).append(title)
    list_of_earthquakes.setdefault(eqid, []).append(coordinates)



for key, value in list_of_earthquakes.items():
    del value[2][-1]
    value[2].reverse()
    


for key, value in list_of_earthquakes.items():
    fg.add_child(folium.Marker(location=list_of_earthquakes[key][2], popup=list_of_earthquakes[key][1], icon=folium.Icon(color='green')))
    folium.Circle(
        location = list_of_earthquakes[key][2],
        popup = list_of_earthquakes[key][1],
        radius = float(list_of_earthquakes[key][0])*100000,
        color = 'crimson',
        fill = True,
        fill_color = 'crimson'
    ).add_to(map)


map.add_child(fg)

map.save("Map1.html")