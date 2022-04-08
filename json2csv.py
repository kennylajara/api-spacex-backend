import csv
import json
import time
import datetime


data = json.load(open('starlink_historical_data.json'))

file = csv.writer(open("starlink_historical_data.csv", "w", newline=''))
file.writerow(["pk", "creation_date", "longitude", "latitude", "id"])

counter = 0
for d in data:
    counter += 1
    file.writerow([
        counter,
        d["spaceTrack"]["CREATION_DATE"],
        d["longitude"],
        d["latitude"],
        d["id"],
    ])
