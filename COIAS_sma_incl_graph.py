import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import re

def get_final_all_values(file_path):
    import re

    # Lists to store extracted information
    size_values = []
    a_values = []
    i_values = []

    # Regular expressions to match the patterns
    size_pattern = re.compile(r'Size is probably (\d+) to (\d+)')
    a_pattern = re.compile(r'a=(\d+\.\d+)')
    i_pattern = re.compile(r'i=([-+]?\d*\.\d+|\d+)')

    with open(file_path, 'r') as file:
        for line in file:
            size_match = size_pattern.search(line)
            if size_match and a_match and i_match:
                size_values.append((int(size_match.group(1)), int(size_match.group(2))))

            a_match = a_pattern.search(line)
            if a_match:
                a_values.append(float(a_match.group(1)))
                if float(a_match.group(1)) > 100:
                    print(file_path + " includes a semi-major axis of > 100 AU! Are you sure this is a correct fit?")

            i_match = i_pattern.search(line)
            if i_match:
                i_values.append(float(i_match.group(1)))

    if len(size_values) == len(a_values) == len(i_values):
        return size_values, a_values, i_values
    else:
        print("Something went wrong with:", file_path)
        return None, None, None

def main(sys_args, debug=False):
    
    if len(sys_args) < 2:
        folder_path = input("Folder in which final_all.txt files are found (leave blank to use current folder): ")
        if not folder_path:
            folder_path = "./"
    else:
        folder_path = sys_args[1]
        
    final_all_files = []

    print("Reading final_all.txt files...")
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "final_all.txt":
                final_all_files.append(os.path.join(root, file))

    if debug:
        print(final_all_files)

    semimajor_axes = []
    inclinations = []
    sizes = []
    
    for file_path in final_all_files:
        new_size, new_a, new_i = get_final_all_values(file_path)
        if new_size and new_a and new_i:
            semimajor_axes = semimajor_axes + new_a
            inclinations = inclinations + new_i
            sizes = sizes + new_size

    avg_sizes_mark = [(sum(t) / len(t)) * 0.01 for t in sizes]

    xs = []
    ys = []

    for idx in range(len(semimajor_axes)):
        i = inclinations[idx]
        if i > 90:
            i = i - 90

        i = np.deg2rad(i)

        new_x = semimajor_axes[idx] * np.cos(i)
        new_y = semimajor_axes[idx] * np.sin(i)
        xs.append(new_x)
        ys.append(new_y)

    fig, ax = plt.subplots()

    # plot SMA circles
    for i in range(1, 10):
        num_points = 100

        theta = np.linspace(0, np.pi/2, num_points)

        x = i * 5 * np.cos(theta)
        y = i * 5 * np.sin(theta)

        ax.plot(x, y, c="g")
        ax.text(0, i * 5, "a=" + str(i * 5) + " AU", ha='right', va='center')

    # plot inclination lines
    line_length = 100
    num_lines = 10
    angles = np.radians(np.arange(0, 91, 10))

    x = line_length * np.cos(angles)
    y = line_length * np.sin(angles)

    for i in range(num_lines):
        ax.plot([0, x[i]], [0, y[i]], marker='o', linestyle='-', color='red')
        ax.text(x[i], y[i], "i=" + str(i*10) + "/" + str(180 - i*10) + " deg", ha='left', va='bottom')

    # plot minor planets
    ax.scatter(xs, ys, s=avg_sizes_mark, zorder=5)
        
    ax.set_aspect("equal")
    plt.xlabel("Semi-major Axis (AU)")
    plt.ylabel("Semi-major Axis (AU)")
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

