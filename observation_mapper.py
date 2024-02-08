import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys
import math

PI = math.pi
PI_12 = PI/12
PI_720 = PI/720
PI_43200 = PI/43200

class RightAscension:
    def __init__(self, h, m, s):
        self.neg = False
        if h < 0:
            self.neg = True
            
        self.h = abs(h)
        self.m = m
        self.s = s

    def toRad(self):
        if not self.neg:
            return self.h * PI_12 + self.m * PI_720 + self.s * PI_43200
        else:
            return -self.h * PI_12 - self.m * PI_720 - self.s * PI_43200

    def toDeg(self):
        # won't bother, this works
        return math.degrees(self.toRad())

class Declination:
    def __init__(self, d, m, s):
        self.neg = False
        if d < 0:
            self.neg = True
            
        self.d = abs(d)
        self.m = m
        self.s = s

    def toRad(self):
        deg_decimal = self.d + self.m / 60 + self.s / 3600
        if self.neg:
            deg_decimal = -deg_decimal
        return math.radians(deg_decimal)

    def toDeg(self):
        if not self.neg:
            return self.d + self.m / 60 + self.s / 3600
        else:
            return -1 * (self.d + self.m / 60 + self.s / 3600)

def set_axes_equal(ax):
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = 0
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = 0
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = 0

    plot_radius = 0.7*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def readFile(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    return lines

def parse80(line):
    ra_str = line[32:43].strip()
    dec_str = line[44:55].strip()
    mag_str = line[65:69].strip()

    ra_str = ra_str.split(" ")
    dec_str = dec_str.split(" ")

    ra_floats = [float(element) for element in ra_str]
    dec_floats = [float(element) for element in dec_str]
    mag = float(mag_str)

    RA = RightAscension(ra_floats[0], ra_floats[1], ra_floats[2])
    DEC = Declination(dec_floats[0], dec_floats[1], dec_floats[2])

    return RA.toRad(), DEC.toRad(), mag

def main():
    args = sys.argv

    if len(args) > 1:
        filename = args[1]
    else:
        filename = input("80-column format observation filename: ")

    lines = readFile(filename)
    
    ras = []
    decs = []
    mags = []
    for line in lines:
        ra, dec, mag = parse80(line)
        ras.append(ra)
        decs.append(dec)
        mags.append(mag)

    xs = []
    ys = []
    zs = []
    sizes = []
    for i in range(len(ras)):
        xs.append(math.cos(ras[i]) * math.cos(decs[i]))
        ys.append(math.sin(ras[i]) * math.cos(decs[i]))
        zs.append(math.sin(decs[i]))
        sizes.append(((max(mags) + 1) - mags[i]) * 3)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(xs, ys, zs, s=sizes, marker='o')

    # Observer
    ax.scatter(0, 0, 0, s=20, marker="o")
    # Principal Axes
    ax.plot([0, 1], [0, 0], [0, 0], color="r")
    ax.plot([0, 0], [0, 1], [0, 0], color="g")
    ax.plot([0, 0], [0, 0], [0, 1], color="b")

    ax.set_xlabel('X (Equinox)')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Pole)')
    ax.set_title('Observations Plot')
    set_axes_equal(ax)

    plt.show()
        
main()
