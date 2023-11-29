import json
import matplotlib.pyplot as plt

def bin_data(x, y):
    segments = 100
    data_num = len(x)

    data_per_segment = int(data_num / segments)
    
    i = 0
    db_y = []
    db_x = []
    for s in range(segments):
        sum_x = 0
        sum_y = 0
        for d in range(data_per_segment):
            sum_x += x[s * data_per_segment + d]
            sum_y += y[s * data_per_segment + d]

        avg_y = sum_y / data_per_segment
        avg_x = sum_x / data_per_segment

        db_y.append(avg_y)
        db_x.append(avg_x)

    return db_x, db_y

def standard_deviation(x, y):
    data_len = len(x)
    mean_y = sum(y) / data_len

    variance = 0
    for iy in y:
        variance += (iy - mean_y)**2

    variance = variance / data_len

    return variance**0.5

def copy_shift_line(x, y, shift):
    new_x = []
    new_y = []

    for idx in range(len(x)):
        new_x.append(x[idx])
        new_y.append(y[idx] + shift)

    return new_x, new_y

def main():
    json_file = open("data/lightcurve/lc.json", "r")
    data = json.load(json_file)

    y = data["y"]
    x = data["x"]

    dbx, dby = bin_data(x, y)
    stdev = standard_deviation(x, y)
    sdx, sdy = copy_shift_line(dbx, dby, -stdev)
    sux, suy = copy_shift_line(dbx, dby, stdev)

    plt.scatter(x, y, color="b", label="Original Data")
    plt.plot(dbx, dby, color="r", lw=2, label="Data Binning")
    plt.plot(sdx, sdy, color="orange", lw=1, label="Std. Deviation")
    plt.plot(sux, suy, color="orange", lw=1, label="Std. Deviation")
    plt.title("Light Curve")
    plt.xlabel("Time (day)")
    plt.ylabel("Brightness")
    plt.legend()
    plt.grid()
    plt.show()

main()
