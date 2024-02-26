import os
import requests

mpc_send_files = []

print("Reading send_mpc.txt files...")
for root, dirs, files in os.walk("observations/"):
    for file in files:
        if file == "send_mpc.txt":
            mpc_send_files.append(os.path.join(root, file))

objects = []
old_obj_num = 0
for filepath in mpc_send_files:
    file = open(filepath)
    lines = file.readlines()

    for line in lines:
        if line.startswith("     H"):
            new_obj_str = line[5:12]
            new_obj_num = int(line[6:12])
            
            if new_obj_num > old_obj_num:
                objects.append(new_obj_str + " T09")
                old_obj_num = new_obj_num

print("Retrieving observations from Minor Planet Center...")
url = "https://data.minorplanetcenter.net/api/wamo"
obs_list = objects
result = requests.get(url, json=obs_list)
observations = result.json()

result = requests.get(url, json={'return_type': 'string', 'obs': obs_list})
observations = result.text
observations = observations.split("\n")

print("Writing observation states into MPC_stats_NEW.txt...")
with open("MPC_stats.txt", "w") as text_file:
    for o in observations:
        text_file.write(o)
        text_file.write("\n")

def truncate_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            truncated_line = line[:80]
            outfile.write(truncated_line + '\n')

print("Truncating for 80-column MPC format...")
input_file_name = 'MPC_stats.txt'
output_file_name = 'MPC_truncated.txt'

truncate_lines(input_file_name, output_file_name)

print("Finding identifications...")
def find_identification_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if "identified" in line:
                outfile.write(line)

input_file_name = 'MPC_stats.txt'
output_file_name = 'MPC_ids.txt'

find_identification_lines(input_file_name, output_file_name)

print("Done!")
