import os
import requests

mpc_send_files = []

WAMO_all_filename = "MPC_stats.txt"
MPC80_filename = "MPC_truncated.txt"
WAMO_ids_filename = "MPC_ids.txt"
numbered_filename = "MPC_numbered.txt"
WAMO_discoveries_filename = "MPC_discoveries.txt"
MPC_elements_filename = "MPC_discovery_detailed.txt"
MPC_distant_elements_filename = "MPC_distant_discovery_detailed.txt"

def truncate_lines(input_file, output_file):
    line_count = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            truncated_line = line[:80]
            outfile.write(truncated_line + '\n')
            line_count += 1

    print("Total observations: " + str(line_count))

def find_identification_lines(input_file, output_file):
    id_count = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if "identified" in line:
                outfile.write(line)
                id_count += 1

    print("Identified observations: " + str(id_count))

def find_discoveries(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if "*" in line:
                outfile.write(line)

def find_numbered(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not " " in line[0:12]:
                outfile.write(line)

def separate_distant(input_filename, output_filename):
    TNO_lines = []
    with open(input_filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_s = line.split(" ")
            sma = line_s[1]
            if float(sma[2:-1]) > 6:
                TNO_lines.append(line)

    with open(output_filename, "w") as f:
        for line in TNO_lines:
            f.write(line)

if __name__ == "__main__":
    # Get all measurement stats
    print("Reading send_mpc.txt files...")
    for root, dirs, files in os.walk("observations/"):
        for file in files:
            if file.startswith("send_mpc"):
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

    print("Writing observation states into MPC_stats.txt...")
    with open(WAMO_all_filename, "w") as text_file:
        for o in observations:
            text_file.write(o)
            text_file.write("\n")

    # Truncate into 80-column format
    print("Truncating for 80-column MPC format...")
    input_file_name = WAMO_all_filename
    output_file_name = MPC80_filename
    truncate_lines(input_file_name, output_file_name)

    # Get identified measurements
    print("Finding identifications...")
    input_file_name = WAMO_all_filename
    output_file_name = WAMO_ids_filename
    find_identification_lines(input_file_name, output_file_name)

    # get newly numbered objects
    print("Getting newly numbered measurements...")
    input_file_name = WAMO_ids_filename
    output_file_name = numbered_filename
    find_numbered(input_file_name, output_file_name)

    # Get discovery asterisks
    print("Isolating discoveries...")
    input_file_name = WAMO_ids_filename
    output_file_name = WAMO_discoveries_filename
    find_discoveries(input_file_name, output_file_name)

    # Get orbital data for discoveries
    print("Getting orbital elements from MPC...")
    with open(WAMO_discoveries_filename, "r") as file:
        lines = file.readlines()
        print("Num. of potential discoveries: " + str(len(lines)))

        outlines = []
        for line in lines:
            # packed designation
            objname = line[5:12]
            print("Getting elements for discovery object: " + objname)
            url = "https://www.minorplanetcenter.net/db_search/show_object?object_id=" + objname
            mpcpage = requests.get(url).text

            mpclines = mpcpage.split("\n")
            for l2 in mpclines:
                if "semimajor axis (AU)" in l2:
                    au = l2[57:66]
                elif "inclination" in l2:
                    inc = l2[53:60]
                elif "eccentricity" in l2:
                    ecc = l2[50:57]
                elif "uncertainty" in l2:
                    uncert = l2[87]

            try:
                au = float(au)
                inc = float(inc)
                ecc = float(ecc)
                uncert = int(uncert)
            except:
                print("Something went wrong getting orbital elements.")
                au = "no idea"
                inc = "dont know"
                ecc = "try find_orb"
                uncert = "sorry"

            outline = objname + " a=" + str(au) + ", i=" + str(inc) + ", e=" + str(ecc) + ", u=" + str(uncert) + "\n"
            outlines.append(outline)

    print("Writing discovery orbital elements to file...")
    with open(MPC_elements_filename, "w") as file:
        for l in outlines:
            file.write(l)

    print("Isolating TNO discoveries...")
    separate_distant(MPC_elements_filename, MPC_distant_elements_filename)

    print("Done!")
