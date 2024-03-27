import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def separate_floats_by_band(mag_list, color_list):
    mag_dict = {color: [] for color in set(color_list)}

    for mag, color in zip(mag_list, color_list):
        mag_dict[color].append(mag)

    return mag_dict

def plot_stacked_histogram(separated_floats):
    plt.figure(2)
    
    data_lists = list(separated_floats.values())
    labels = list(separated_floats.keys())

    plt.hist(data_lists, bins=30, stacked=True, alpha=0.7, label=labels)

    plt.xlabel('Magnitude')
    plt.ylabel('Number of objects')
    plt.title('Observation magnitudes')
    plt.legend(title='Bands', loc='upper right')
    plt.grid()
    plt.show()

def plot_mags(float_list, show=True):   
    plt.hist(float_list, bins=30, edgecolor='black')
    
    plt.xlabel('Magnitude')
    plt.ylabel('Number of objects')
    plt.title('Observation magnitudes')
    plt.grid()

    if show:
        plt.show()

def main(sys_args, debug=False):
    
    if len(sys_args) < 2:
        folder_path = input("Folder in which .txt files are found: ")
        if not folder_path:
            folder_path = "./"
    else:
        folder_path = sys_args[1]
        
    final_all_files = []

    print("Reading .txt files...")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            final_all_files.append(os.path.join(root, file))

    if debug:
        print(final_all_files)

    # get obs. properties
    H_numbers = []
    magnitudes = []
    bands = []
    
    for filepath in final_all_files:
        file = open(filepath)
        file_lines = file.readlines()

        for line in file_lines:
            H_num = int(line[0:12])

            if not H_num in H_numbers:
                H_numbers.append(H_num)
                
                line = line.split(" ")
                line = [i for i in line if i != ""] # removes all "" elements

                mag = float(line[10])
                band = line[11]

                magnitudes.append(mag)
                bands.append(band)

    print("Found " + str(len(bands)) + " objects.")

    max_mag = min(magnitudes)
    min_mag = max(magnitudes)

    print("Max. mag:", max_mag)
    print("Min. mag:", min_mag)
    
    plot_mags(magnitudes, False)
    datadict = separate_floats_by_band(magnitudes, bands)
    plot_stacked_histogram(datadict)

if __name__ == "__main__":
    main(sys.argv)

