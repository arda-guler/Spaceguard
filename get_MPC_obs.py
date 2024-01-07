import requests
from openpyxl import load_workbook

# == INPUTS ==
spreadsheet_name = "obs.xlsx"

num_asteroids = 22

# which row the table entries begin from on the spreadsheet
# (e.g. table_offset = 5 if first entry is at C5)
table_offset = 5

# the column on which the object names/ids are kept
# (e.g. ID_col = "C" if first entry is at C5)
ID_col = "C"

observatory_suffix = "T09" # e.g. T09 = Subaru
# == == == == ==

print("Reading objects from spreadsheet...")
workbook = load_workbook(filename=spreadsheet_name)
sheet = workbook.active

asteroid_ids = []
for i in range(num_asteroids):
    asteroid_ids.append(sheet[ID_col + str(int(table_offset + i))].value + " " + observatory_suffix)

print("Retrieving observations from Minor Planet Center...")
url = "https://data.minorplanetcenter.net/api/wamo"
obs_list = asteroid_ids
result = requests.get(url, json=obs_list)
observations = result.json()

# The Flask endpoint can also provide the original WAMO string
result = requests.get(url, json={'return_type': 'string', 'obs': obs_list})
observations = result.text
observations = observations.split("\n")

print("Writing observation states into MPC_stats.txt...")
with open("MPC_stats.txt", "w") as text_file:
    for o in observations:
        text_file.write(o)
        text_file.write("\n")

print("Done!")



