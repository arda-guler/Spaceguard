import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import numpy as np

class Asteroid:
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

def readJSON(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File", filename, "not found!")
    except json.JSONDecodeError as e:
        print("Error: Failed to decode JSON in", filename, "\n", e)

def generate_orbits(NEOs, poly=1000):
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for n in NEOs:
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

        x_rot = x * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination)) - \
                y * (np.sin(argument_perihelion) * np.cos(ascending_node) + np.cos(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        y_rot = x * (np.cos(argument_perihelion) * np.sin(ascending_node) + np.sin(argument_perihelion) * np.cos(ascending_node) * np.cos(inclination)) + \
                y * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        z_rot = x * np.sin(argument_perihelion) * np.sin(inclination) + y * np.sin(argument_perihelion) * np.sin(inclination)

        color = "k"
        if n.orbit_type:
            if n.orbit_type == "Atira":
                color = "olive"
            elif n.orbit_type == "Aten":
                color = "cyan"
            elif n.orbit_type == "Apollo":
                color = "red"
            elif n.orbit_type == "Amor":
                color = "orange"
            elif n.orbit_type == "Object with perihelion distance < 1.665 AU":
                color = "purple"
            elif n.orbit_type == "Hungaria":
                color = "pink"
            elif n.orbit_type == "MBA":
                color = "gray"
            elif n.orbit_type == "Phocaea":
                color = "green"
            elif n.orbit_type == "Hilda":
                color = "brown"
            elif n.orbit_type == "Jupiter Trojan":
                color = "aquamarine"
            elif n.orbit_type == "Distant Object":
                color = "navy"

        ax.plot(x_rot, y_rot, z_rot, color=color)

    # -- plot Earth orbit
    eccentricity = 0.0167086
    argument_perihelion = np.radians(288.1)
    semimajor_axis = 1.0000010178
    ascending_node = np.radians(174.9)
    inclination = 0
    
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

    color = "blue"
    ax.plot(x_rot, y_rot, z_rot, color=color, lw=3)
    # -- END plot Earth orbit

    custom_legend = [Line2D([0], [0], color="blue", lw=3),
                     Line2D([0], [0], color="olive", lw=1),
                     Line2D([0], [0], color="cyan", lw=1),
                     Line2D([0], [0], color="red", lw=1),
                     Line2D([0], [0], color="orange", lw=1),
                     Line2D([0], [0], color="purple", lw=1),
                     Line2D([0], [0], color="pink", lw=1),
                     Line2D([0], [0], color="gray", lw=1),
                     Line2D([0], [0], color="green", lw=1),
                     Line2D([0], [0], color="brown", lw=1),
                     Line2D([0], [0], color="aquamarine", lw=1),
                     Line2D([0], [0], color="navy", lw=1)]
    
    ax.legend(custom_legend, ['Earth', 'Atira', 'Aten', 'Apollo', 'Amor',
                              'Obj. w/ peri. dist. < 1.665 AU',
                              'Hungaria', 'MBA', 'Phocaea',
                              'Hilda', 'Jupiter Trojan', 'Distant Object'])
    
    ax.scatter(0, 0, 0, color='yellow', label='Sol Barycenter')
    
    ax.set_title('Orbit Plot')
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_xlim(-3, 3) # set map limits here
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    plt.show()

# set filters here for which kind of objects should be plotted
def filterNEO(n):
    if (not n.orbit_type):
        return True
    else:
        return False

def main():
    orbit_poly = 1000 # how crisp the minor planet orbits should be rendered

    ast = Asteroid("NoName", "Nonum", 2457551.5,
                    2.63415987, 0.6020446,
                    3.87386, 226.51723,
                    358.64359, 20.96072416)

    asteroids = [ast]

    print("Generating orbit plot...")
    generate_orbits(asteroids, orbit_poly)

main()
