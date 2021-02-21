import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm
import copy


def cartesianToCircle(r, theta):
    return np.array([r * np.cos(theta), r * np.sin(theta)])


class Space():
    def __init__(self, step=1, end=1000):
        self.objects = []
        self.G = 6.67259 * pow(10, -11)
        self.step = step
        self.time = 0.0
        self.endTime = end

    def append(self, obj):
        self.objects.append(obj)

    def play(self, step_dur=1):
        step_num = int(self.endTime / self.step)
        for i in tqdm(range(step_num)):
            isAppend = False
            if(i % step_dur == 0):
                isAppend = True
            self.updateOrbit(isAppend)

    def updateOrbit(self, isAppend=True):
        for obj in self.objects:
            if(obj.fixed is True):
                continue
            k1 = obj.v
            l1 = self.f(obj, obj.x)
            k2 = obj.v + l1 * self.step / 2
            l2 = self.f(obj, obj.x + k1 * self.step / 2)
            k3 = obj.v + l2 * self.step / 2
            l3 = self.f(obj, obj.x + k2 * self.step / 2)
            k4 = obj.v + l3 * self.step
            l4 = self.f(obj, obj.x + k3 * self.step)

            k = (k1 + 2 * k2 + 2 * k3 + k4) / 6
            l = (l1 + 2 * l2 + 2 * l3 + l4) / 6

            obj.x += k * self.step
            obj.v += l * self.step
            # print(obj.orbit)
            if(isAppend is True):
                obj.orbit.append(copy.copy(obj.x))
            # print(obj.orbit)
        self.time += self.step

    def f(self, obj, x):
        f = 0.0
        for other in self.objects:
            if(obj is other or other is Spacecraft):
                continue
            r = np.sqrt(np.sum((x - other.x)**2))
            f += self.G * other.mass * (other.x - x) / (r**3)
        return f

    def plotOrbit(self, center_obj=None, ax_lim=(1e9, 1e9)):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        if(ax_lim is not None):
            ax.set_xlim(-ax_lim[0], ax_lim[0])
            ax.set_ylim(-ax_lim[1], ax_lim[1])
        if(center_obj is None):
            for obj in self.objects:
                orbit = np.array(obj.orbit)
                if(obj.fixed is True):
                    ax.plot(obj.x[0], obj.x[1], color=obj.color, marker='o', markersize=obj.markersize)
                else:
                    ax.plot(orbit[:, 0], orbit[:, 1], color=obj.color, linestyle=obj.linestyle, linewidth=obj.linewidth)
        else:
            for obj in self.objects:
                if obj is center_obj:
                    ax.plot(0, 0, color=obj.color, marker='o', markersize=obj.markersize)
                else:
                    if(obj.fixed is True):
                        c_orbit = np.array(center_obj.orbit)
                        ax.plot(-c_orbit[:, 0], c_orbit[:, 1], color=obj.color, linestyle=obj.linestyle, linewidth=obj.linewidth)
                    else:
                        orbit = np.array(obj.orbit)
                        c_orbit = np.array(center_obj.orbit)
                        ax.plot(orbit[:, 0] - c_orbit[:, 0], orbit[:, 1] - c_orbit[:, 1], color=obj.color, linestyle=obj.linestyle, linewidth=obj.linewidth)
        # plt.legend()
        ax.set_aspect('equal')
        plt.show()

    def animateOrbit(self, interval=100, frames=100, center_obj=None, ax_lim=(1e9, 1e9), orbit_length=float('inf')):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.set_xlim(-ax_lim[0], ax_lim[0])
        ax.set_ylim(-ax_lim[1], ax_lim[1])
        elems = []
        self.ani = animation.FuncAnimation(
            fig, self.animateOrbitFrame, fargs=(elems, ax, center_obj, orbit_length),
            interval=interval, frames=frames,
            repeat=False
        )
        plt.show()

    def animateOrbitFrame(self, i, elems, ax, center_obj, orbit_length):
        while elems:
            elems.pop().remove()
        if(center_obj is None):
            for obj in self.objects:
                if(obj.fixed is True):
                    elems += ax.plot(obj.x[0], obj.x[1], color=obj.color, marker='o', markersize=obj.markersize)
                else:
                    orbit = np.array(obj.orbit)
                    elems += ax.plot(orbit[i, 0], orbit[i, 1], color=obj.color, marker='o', markersize=obj.markersize)
                    if(i > orbit_length):
                        elems += ax.plot(
                            orbit[i - orbit_length:i, 0], orbit[i - orbit_length:i, 1],
                            color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                        )
                    else:
                        elems += ax.plot(orbit[:i, 0], orbit[:i, 1], color='black', linestyle='dashed', linewidth='0.5')
                        elems += ax.plot(
                            orbit[i - orbit_length:i, 0], orbit[i - orbit_length:i, 1],
                            color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                        )
        else:
            for obj in self.objects:
                if obj is center_obj:
                    elems += ax.plot(0, 0, color=obj.color, marker='o', markersize=obj.markersize)
                else:
                    if(obj.fixed is True):
                        pass
                        # elems += ax.plot(obj.x[0] - center_obj.x[:, 0], obj.x[1] - center_obj[:, 1], color=obj.color, marker='o')
                    else:
                        orbit = np.array(obj.orbit)
                        c_orbit = np.array(center_obj.orbit)
                        elems += ax.plot(orbit[i, 0] - c_orbit[i, 0], orbit[i, 1] - c_orbit[i, 1], color=obj.color, marker='o', markersize=obj.markersize)
                        if(i > orbit_length):
                            elems += ax.plot(
                                orbit[i - orbit_length:i, 0] - c_orbit[i - orbit_length:i, 0], orbit[i - orbit_length:i, 1] - c_orbit[i - orbit_length:i, 1],
                                color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                            )
                        else:
                            elems += ax.plot(
                                orbit[:i, 0] - c_orbit[:i, 0], orbit[:i, 1] - c_orbit[:i, 1],
                                color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                            )


class Planet():
    def __init__(self, mass, color='red', fixed=False, linestyle='solid', linewidth='1', markersize='5'):
        self.mass = mass
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.markersize = markersize
        self.fixed = fixed
        self.x = None
        self.v = None
        self.orbit = []

    def initial_pos(self, pos):
        self.x = pos
        self.orbit = []
        self.orbit.append(copy.copy(self.x))

    def initial_vel(self, vel):
        self.v = vel

    @classmethod
    @property
    def mass(self):
        return self.mass


class Spacecraft:
    def __init__(self, mass, color='green', linestyle='solid', linewidth='1', markersize='1'):
        self.mass = mass
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.markersize = markersize
        self.fixed = False
        self.x = None
        self.v = None
        self.orbit = []

    def initial_pos(self, pos):
        self.x = pos
        self.orbit = []
        self.orbit.append(copy.copy(self.x))

    def initial_vel(self, vel):
        self.v = vel
