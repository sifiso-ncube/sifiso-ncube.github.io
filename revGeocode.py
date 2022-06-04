# REVERSE GEOCODING TO GET THE ADDRESSES OF OUR NODE LOCATIONS


# import geopy
# from geopy.geocoders import Nominatim
import pandas as pd
import googlemaps
import os
# import linecache

# Reading the csv file
node = []
lon = []
lat = []

df = pd.read_csv("coord_WGS84.csv")
for i, row in df.iterrows():
    node.append(f"{row['Name']}")
    lon.append(f"{row['Lon']}")
    lat.append(f"{row['Lat']}")
# print(node, lon, lat)
nodes_dict = {}
for i in range(len(lat)):
    nodes_dict[i] = {'name': node[i],
                'lat': lat[i],
                'lon': lon[i]
                }
#print(nodes_dict)

#GEOCODING
gmaps_key = googlemaps.Client(key=os.environ["maps_key"])
def geocode(node_name):
    g = gmaps_key.geocode(node_name)
    lat = g[0]["geometry"]["location"]["lat"]
    long = g[0]["geometry"]["location"]["lng"]
    #print('Latitude: ' + str(lat) + ', Longitude: ' + str(long))
    return lat, long


# lat1, long1 = geocode(node_name)
# def check_location():
#     point = Point(lat1, long1)
#     polygon = Polygon([(20.953674,105.737504), (20.94494,105.743914), (20.940619,105.739696), (20.955746,105.739237)])
#     return polygon.contains(point)
#print(check_location())



# geolocator = Nominatim(user_agent = "sifisopncube@gmail.com")

# GEOCODING- if someone enters the address, so we can get the lat lon and get the node_name or location name


# REVERSE GEOCODE FROM LAT LON TO ADDRESS- so that i can get the addresses , just to see how this geocoding works
# location = geolocator.reverse("20.944215, 105.741185")                     # Example
# for i in range(len(lon)):
#     #print(lat[i])
#     location = geolocator.reverse(str(lon[i])+ ','+ str(lat[i]))
#     address.append(location.address)
# print(address)
# print(location.raw)



#
# for num in range(2, 169):
#     filteredList = []
#     result = linecache.getline("coord_WGS84.csv", num)
#     list = result.split(",")
#     for element in list:
#         if len(element) > 0:
#             filteredList.append(element)
#     node.append(filteredList[0])
#     lon.append(filteredList[1])
#     lat.append(filteredList[2].rstrip("\n"))
#     lon_lat.append([float(filteredList[1]),float(filteredList[2].rstrip("\n"))])

# df['address'] = df.apply(lambda row: geolocator.reverse((row['Lon'], row['Lat'])), axis=1)   #.apply applies a function to every row in the dataframe. lambda expressions are used to construct anonymous functions just like we use def for normal functions.for every row apply the reverse geolocation...
# print(df['address'])
# node. append(df.iloc[:, [0]])
# lon.append(df.iloc[:, [1]])
# lat.append(df.iloc[:, [2]])
