from spacesim.core import Planet
import numpy as np

dis_sun_earth = 149597870700.0
dis_sun_mercury = 57910000000.0
dis_sun_venus = 108208930000.0
dis_earth_moon = 384405000.0
dis_sun_mars = 227920000000.0
dis_sun_jupiter = 778412010000.0
dis_sun_saturn = 1426725400000.0
dis_sun_uranus = 2870990000000.0
dis_sun_neptune = 4495060000000.0
vel_sun = 0.0
vel_mercury = 47360.0
vel_venus = 35021.4
vel_earth = 29800.0
vel_moon = 1022.0
vel_mars = 24070.0
vel_jupiter = 13069.7
vel_saturn = 9672.4
vel_uranus = 6810.0
vel_neptune = 5430.0
mass_sun = 1.9884e30
mass_mercury = 3.301e23
mass_venus = 4.869e24
mass_earth = 5.974e24
mass_moon = 7.347673e22
mass_mars = 6.4171e23
mass_jupiter = 1.8986e27
mass_saturn = 5.688e26
mass_uranus = 8.686e25
mass_neptune = 1.02413e26


class Sun(Planet):
    def __init__(self, fixed=True, color='orangered', linestyle='solid', linewidth='1', markersize=7):
        super(Sun, self).__init__(mass_sun, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([0.0, 0.0]))
        self.initial_vel(np.array([0.0, 0.0]))


class Mercury(Planet):
    def __init__(self, fixed=False, color='darkgrey', linestyle='solid', linewidth='1', markersize=3):
        super(Mercury, self).__init__(mass_mercury, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_mercury, 0.0]))
        self.initial_vel(np.array([0.0, vel_mercury]))


class Venus(Planet):
    def __init__(self, fixed=False, color='sandybrown', linestyle='solid', linewidth='1', markersize=4):
        super(Venus, self).__init__(mass_venus, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_venus, 0.0]))
        self.initial_vel(np.array([0.0, vel_venus]))


class Earth(Planet):
    def __init__(self, fixed=False, color='blue', linestyle='solid', linewidth='1', markersize=4):
        super(Earth, self).__init__(mass_earth, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_earth, 0.0]))
        self.initial_vel(np.array([0.0, vel_earth]))


class Moon(Planet):
    def __init__(self, fixed=False, color='brown', linestyle='solid', linewidth='1', markersize=2):
        super(Moon, self).__init__(mass_moon, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_earth_moon, 0.0]))
        self.initial_vel(np.array([0.0, vel_moon]))


class Mars(Planet):
    def __init__(self, fixed=False, color='brown', linestyle='solid', linewidth='1', markersize=4):
        super(Mars, self).__init__(mass_mars, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_mars, 0.0]))
        self.initial_vel(np.array([0.0, vel_mars]))


class Jupiter(Planet):
    def __init__(self, fixed=False, color='tan', linestyle='solid', linewidth='1', markersize=6):
        super(Jupiter, self).__init__(mass_jupiter, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_jupiter, 0.0]))
        self.initial_vel(np.array([0.0, vel_jupiter]))


class Saturn(Planet):
    def __init__(self, fixed=False, color='darkgoldenrod', linestyle='solid', linewidth='1', markersize=6):
        super(Saturn, self).__init__(mass_saturn, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_saturn, 0.0]))
        self.initial_vel(np.array([0.0, vel_saturn]))


class Uranus(Planet):
    def __init__(self, fixed=False, color='dodgerblue', linestyle='solid', linewidth='1', markersize=6):
        super(Uranus, self).__init__(mass_uranus, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_uranus, 0.0]))
        self.initial_vel(np.array([0.0, vel_uranus]))


class Neptune(Planet):
    def __init__(self, fixed=False, color='aqua', linestyle='solid', linewidth='1', markersize=6):
        super(Neptune, self).__init__(mass_neptune, fixed=fixed, color=color, linestyle=linestyle, linewidth=linewidth, markersize=markersize)
        self.initial_pos(np.array([dis_sun_neptune, 0.0]))
        self.initial_vel(np.array([0.0, vel_neptune]))
