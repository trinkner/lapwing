from collections import defaultdict
import json
import csv

codeDict = defaultdict()

with open('iso_codes.csv', mode='r') as codeFile:
	csv_reader = csv.DictReader(codeFile)    
	for row in csv_reader:
	    codeDict[row["3Digit"]] = row["2Digit"]


world_geo = json.loads(open('world_geo.json').read())

for f in world_geo["features"]:
	if f["properties"]["GID_0"] in codeDict.keys():
        	f["id"] = codeDict[f["properties"]["GID_0"]]
	else:
		print(f["properties"]["GID_0"] + " NOT CONVERTED")



