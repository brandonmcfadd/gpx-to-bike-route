from bs4 import BeautifulSoup
import json

input_file_name = input('What is the name of the file to import?\n')
input_short_ride_name = input('What is the name of the ride? (ride-name-format)\n')
input_ride_name = input('What is the name of the ride?\n')
input_ride_desc1 = input('What is the run description line 1?\n')
input_ride_desc2 = input('What is the run description line 2?\n')
input_brought_by = input('Brought to you by?\n')
with open(input_file_name, 'r') as f:
    data = f.read()
 
soup = BeautifulSoup(data, 'xml')

latitudes = []
longitudes = []
waypoints = []

track_points = soup.find_all('trkpt')
count = 0
total_length = len(track_points)
last_lat_lon = []
for point in track_points:
    count += 1
    lat = float(point.get('lat'))
    lon = float(point.get('lon'))
    latitudes.append(lat)
    longitudes.append(lon)
    if count == 1 and ([lat, lon] != last_lat_lon):
        new_waypoint = {
        "name": "Start",
        "subtitle": "Address",
        "time": "Time",
        "icon": "/images/start-button.png",
        "coordinates": [lat, lon]
      }
        print("added start point")
    elif count == total_length:
        new_waypoint = {
        "name": "Finish",
        "subtitle": "Subtitle",
        "time": "12:34",
        "icon": "/images/finish-icon.png",
        "coordinates": [lat, lon],
        "markerClass": "rotate-minus-35"
      }
    elif ([lat, lon] != last_lat_lon):
        new_waypoint = {
            "waypointOnly": "true",
            "coordinates": [lat, lon],
            "markerClass": ""
        }
    last_lat_lon = [lat, lon]
    waypoints.append(new_waypoint)

latitudes_sorted = sorted(latitudes)
longitudes_sorted = sorted(longitudes)

output_json = {
    input_short_ride_name: {
    "title": input_ride_name,
    "runInfo1": input_ride_desc1,
    "runInfo2": input_ride_desc2,
    "headerImageAlt": f"Brought to you by {input_brought_by}!",
    "trackerBounds": {
      "bottomLeft": [latitudes_sorted[0], longitudes_sorted[-1]],
      "topRight": [latitudes_sorted[-1], longitudes_sorted[0]]
    },
    "color": "#eb8334",
    "mapHeight": "550px",
    "stops": waypoints
  }
}
print(len(waypoints))
with open(f"output-{input_file_name}.json", "w+") as outfile:
    json.dump(output_json, outfile, indent=2)