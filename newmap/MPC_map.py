import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import numpy as np
import random
import sys

class OBJECT:
    def __init__(self, name, number, epoch,
                 semimajor_axis, eccentricity,
                 inclination, long_asc_node,
                 arg_peri, mean_anom, orbit_type=None):
        
        self.name = name
        self.number = number
        self.epoch = epoch
        self.a = semimajor_axis
        self.e = eccentricity
        self.i = inclination
        self.node = long_asc_node
        self.peri = arg_peri
        self.M = mean_anom
        self.orbit_type = orbit_type

class Planet:
    def __init__(self, name, a, e, i, OMG, o, L):
        self.name = name
        self.a = a
        self.e = e
        self.i = i
        self.OMG = OMG # big omega
        self.o = o # small omega with a tilda
        self.L = L

def readJSON(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File", filename, "not found!")
    except json.JSONDecodeError as e:
        print("Error: Failed to decode JSON in", filename, "\n", e)

def generate_orbits(OBJECTs, planets, planet_colors, poly=1000):
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for n in OBJECTs:
        eccentricity = n.e
        argument_perihelion = np.radians(n.peri)
        semimajor_axis = n.a # AU
        ascending_node = np.radians(n.node)
        inclination = np.radians(n.i)
        
        
        true_anomaly = np.linspace(0, 2 * np.pi, poly)

        r = (semimajor_axis * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(true_anomaly))

        x = r * np.cos(true_anomaly)
        y = r * np.sin(true_anomaly)
        z = np.zeros_like(true_anomaly)

        print(n.i)
        print(inclination)
        print(argument_perihelion)
        print("")

        x_rot = x * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination)) - \
                y * (np.sin(argument_perihelion) * np.cos(ascending_node) + np.cos(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        y_rot = x * (np.cos(argument_perihelion) * np.sin(ascending_node) + np.sin(argument_perihelion) * np.cos(ascending_node) * np.cos(inclination)) + \
                y * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        z_rot = x * np.sin(argument_perihelion) * np.sin(inclination) + y * np.sin(argument_perihelion) * np.sin(inclination)

        color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
##        if n.orbit_type:
##            if n.orbit_type == "Atira":
##                color = "olive"
##            elif n.orbit_type == "Aten":
##                color = "cyan"
##            elif n.orbit_type == "Apollo":
##                color = "red"
##            elif n.orbit_type == "Amor":
##                color = "orange"
##            elif n.orbit_type == "Object with perihelion distance < 1.665 AU":
##                color = "purple"
##            elif n.orbit_type == "Hungaria":
##                color = "pink"
##            elif n.orbit_type == "MBA":
##                color = "gray"
##            elif n.orbit_type == "Phocaea":
##                color = "green"
##            elif n.orbit_type == "Hilda":
##                color = "brown"
##            elif n.orbit_type == "Jupiter Trojan":
##                color = "aquamarine"
##            elif n.orbit_type == "Distant Object":
##                color = "navy"

        ax.plot(x_rot, y_rot, z_rot, color=color, label=n.name)

    for p_idx in range(len(planets)):
        p = planets[p_idx]
        
        eccentricity = p.e
        argument_perihelion = np.radians(p.o)
        semimajor_axis = p.a
        ascending_node = np.radians(p.OMG)
        inclination = np.radians(p.i)
        
        true_anomaly = np.linspace(0, 2 * np.pi, 1000)

        r = (semimajor_axis * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(true_anomaly))

        x = r * np.cos(true_anomaly)
        y = r * np.sin(true_anomaly)
        z = np.zeros_like(true_anomaly)

        x_rot = x * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination)) - \
                y * (np.sin(argument_perihelion) * np.cos(ascending_node) + np.cos(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        y_rot = x * (np.cos(argument_perihelion) * np.sin(ascending_node) + np.sin(argument_perihelion) * np.cos(ascending_node) * np.cos(inclination)) + \
                y * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        z_rot = x * np.sin(argument_perihelion) * np.sin(inclination) + y * np.sin(argument_perihelion) * np.sin(inclination)

        color = planet_colors[p_idx]
        ax.plot(x_rot, y_rot, z_rot, color=color, lw=3, linestyle="--")

##    custom_legend = [Line2D([0], [0], color="olive", lw=1),
##                     Line2D([0], [0], color="cyan", lw=1),
##                     Line2D([0], [0], color="red", lw=1),
##                     Line2D([0], [0], color="orange", lw=1),
##                     Line2D([0], [0], color="purple", lw=1),
##                     Line2D([0], [0], color="pink", lw=1),
##                     Line2D([0], [0], color="gray", lw=1),
##                     Line2D([0], [0], color="green", lw=1),
##                     Line2D([0], [0], color="brown", lw=1),
##                     Line2D([0], [0], color="aquamarine", lw=1),
##                     Line2D([0], [0], color="navy", lw=1)]
    
##    ax.legend(custom_legend, ['Atira', 'Aten', 'Apollo', 'Amor',
##                              'Obj. w/ peri. dist. < 1.665 AU',
##                              'Hungaria', 'MBA', 'Phocaea',
##                              'Hilda', 'Jupiter Trojan', 'Distant Object'])


    ax.scatter(0, 0, 0, color='yellow', label='Sol Barycenter')
    
    ax.set_title('Orbit Plot')
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_xlim(-50, 50) # set map limits here
    ax.set_ylim(-50, 50)
    ax.set_zlim(-50, 50)
    ax.set_axis_off()
    plt.legend()
    plt.show()

# set filters here for which kind of objects should be plotted
def filterOBJECT(n):
    if (not n.orbit_type):
        return True
    else:
        return False

def main():
    sys_argv = sys.argv

    MAX_OBJECTS = 1e8
    orbit_poly = 1000 # how crisp the minor planet orbits should be rendered
    orbit_filepath = "orbits/orbits.json"

    if len(sys_argv) > 1:
        orbit_filepath = sys_argv[1]
    else:
        orbit_filepath_inp = input("Enter JSON file path for orbital elements (default is orbits/orbits.json):")
        if orbit_filepath_inp:
            orbit_filepath = orbit_filepath_inp
        
    print("Reading JSON orbital elements data...")
    OBJECT_data = readJSON(orbit_filepath)

    OBJECTs = []
    i = 0
    for n in OBJECT_data:
        try:
            name = n["Name"]
        except KeyError:
            name = None

        try:
            number = n["Number"]
        except KeyError:
            number = None
    
        try:
            orbit_type = n["Orbit_type"]
        except KeyError:
            orbit_type = None
        
        new_OBJECT = OBJECT(name, number, n["Epoch"],
                      n["a"], n["e"], n["i"], n["Node"],
                      n["Peri"], n["M"], orbit_type)

        if not filterOBJECT(new_OBJECT):
            OBJECTs.append(new_OBJECT)
            i += 1

        if i > MAX_OBJECTS:
            break

    planets = []
    print("Reading JSON major planet data...")
    planet_data = readJSON("orbits/planets.json")
    for p in planet_data:
        name = p["name"]
        a = float(p["a"])
        e = float(p["e"])
        i = float(p["i"])
        OMG = float(p["Omega"])
        o = float(p["-omega"])
        L = float(p["L"])

        new_planet = Planet(name, a, e, i, OMG, o, L)
        planets.append(new_planet)

    planet_colors =\
                  ["gray",
                   "sandybrown",
                   "royalblue",
                   "firebrick",
                   "peru",
                   "moccasin",
                   "powderblue",
                   "slateblue"]

    print("Generating orbit plot...")
    generate_orbits(OBJECTs, planets, planet_colors, orbit_poly)

if __name__ == "__main__":
    main()
