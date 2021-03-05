import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm
import copy
if 'ipykernel' in sys.modules:
    from tqdm import tqdm_notebook as tqdm    # Jupyter Notebook
else:
    from tqdm import tqdm    # ipython, python script, ...


def cartesianToCircle(r, theta):
    return np.array([r * np.cos(theta), r * np.sin(theta)])


class Space():
    def __init__(self, step=1, end=1000):
        self.objects = []
        self.G = 6.67259 * pow(10, -11)
        self.step = step
        self.time = 0.0
        self.endTime = end
        self.step_dur = 1

    def append(self, obj):
        self.objects.append(obj)

    def play(self, step_dur=1):
        self.step_dur = step_dur
        step_num = int(self.endTime / self.step)
        for i in tqdm(range(step_num)):
            isAppend = False
            if(i % self.step_dur == 0):
                isAppend = True
            self.updateOrbit(isAppend)

    def updateOrbit(self, isAppend=True):
        for obj in self.objects:
            if(obj.fixed is True):
                continue
            k1 = obj.v
            l1 = self.f(obj, obj.x, k1)
            k2 = obj.v + l1 * self.step / 2
            l2 = self.f(obj, obj.x + k1 * self.step / 2, k2)
            k3 = obj.v + l2 * self.step / 2
            l3 = self.f(obj, obj.x + k2 * self.step / 2, k3)
            k4 = obj.v + l3 * self.step
            l4 = self.f(obj, obj.x + k3 * self.step, k4)

            k = (k1 + 2 * k2 + 2 * k3 + k4) / 6
            l = (l1 + 2 * l2 + 2 * l3 + l4) / 6

            obj.x += k * self.step
            obj.v += l * self.step
            if(isAppend is True):
                obj.orbit.append(copy.copy(obj.x))
        self.time += self.step

    def f(self, obj, x, v):
        f = np.array(self.uGravity(obj, x))
        if(type(obj) is Spacecraft):
            f += self.injectionF(obj, v) / obj.mass
        return f

    def injectionF(self, obj, v):
        f = np.zeros(len(v))
        for injection in obj.injection:
            if(self.time >= injection['start'] and self.time <= injection['start'] + injection['last']):
                unitVectorV = v / np.linalg.norm(v) if(np.linalg.norm(v) > 1e-10) else np.array([1.0, 0.0])
                if(len(v) == 2):
                    R = np.array([[np.cos(injection['theta']), -np.sin(injection['theta'])], [np.sin(injection['theta']), np.cos(injection['theta'])]])
                    unitVector = np.dot(R, unitVectorV)
                    thurst = injection['force'] * unitVector
                elif(len(v) == 3):
                    thurst = np.array([
                        injection['force'] * np.cos(injection['theta']) * np.cos(injection['phi']),
                        injection['force'] * np.sin(injection['theta']) * np.cos(injection['phi']),
                        injection['force'] * np.cos(injection['theta']) * np.sin(injection['phi'])
                    ])
                f += thurst
        return f

    def uGravity(self, obj, x):
        if(len(x) == 2):
            f = [0.0, 0.0]
        elif(len(x) == 3):
            f = [0.0, 0.0, 0.0]
        for other in self.objects:
            if(obj is other or type(other) is Spacecraft):
                continue
            r = np.sqrt(np.sum((x - other.x)**2))
            f += self.G * other.mass * (other.x - x) / (r**3)
        return f

    def plotOrbit(self, center_obj=None, ax_lim=(1e9, 1e9), loc=None, bbox_to_anchor=None, borderaxespad=1):
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
                    ax.scatter(obj.x[0], obj.x[1], c=obj.color, marker='.', s=int(obj.markersize), label=obj.name)
                else:
                    ax.plot(orbit[:, 0], orbit[:, 1], color=obj.color, linestyle=obj.linestyle, linewidth=obj.linewidth, label=obj.name)
        else:
            for obj in self.objects:
                if obj is center_obj:
                    ax.scatter(0, 0, c=obj.color, marker='.', s=int(obj.markersize), label=obj.name)
                else:
                    c_orbit = np.array(center_obj.orbit)
                    if(obj.fixed is True):
                        ax.plot(-c_orbit[:, 0], c_orbit[:, 1], color=obj.color, linestyle=obj.linestyle, linewidth=obj.linewidth, label=obj.name)
                    else:
                        orbit = np.array(obj.orbit)
                        ax.plot(orbit[:, 0] - c_orbit[:, 0], orbit[:, 1] - c_orbit[:, 1], color=obj.color, linestyle=obj.linestyle, linewidth=obj.linewidth, label=obj.name)
        ax.legend(loc=loc, bbox_to_anchor=bbox_to_anchor, borderaxespad=borderaxespad)
        plt.show()

    def animateOrbit(self, interval=100, frames=100, center_obj=None, ax_lim=(1e9, 1e9), orbit_length=float('inf'), time='day', loc=None, bbox_to_anchor=None, borderaxespad=1):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        ax.set_xlim(-ax_lim[0], ax_lim[0])
        ax.set_ylim(-ax_lim[1], ax_lim[1])
        elems = []
        self.ani = animation.FuncAnimation(
            fig, self.animateOrbitFrame, fargs=(elems, ax, center_obj, orbit_length, time, loc, bbox_to_anchor, borderaxespad),
            interval=interval, frames=frames,
            repeat=False
        )
        plt.show()

    def animateOrbitFrame(self, i, elems, ax, center_obj, orbit_length, time, loc, bbox_to_anchor, borderaxespad):
        while elems:
            elems.pop().remove()
        time_str = i * self.step * self.step_dur
        if(time == 'year'):
            time_str = str(int(time_str // (86400 * 365))) + ' years'
        elif(time == 'day'):
            time_str = str(int(time_str // 86400)) + ' days'
        elif(time == 'hour'):
            time_str = str(int(time_str // 3600)) + ' hours'
        elif(time == 'min'):
            time_str = str(int(time_str // 60)) + ' minutes'
        else:
            time_str = str(time_str) + ' sec'
        elems.append(
            ax.text(
                ax.get_xlim()[0] * 0.95, ax.get_ylim()[1] * 0.90,
                str(time_str),
                fontsize=10
            )
        )
        if(center_obj is None):
            for obj in self.objects:
                if(obj.fixed is True):
                    elems.append(ax.scatter(obj.x[0], obj.x[1], c=obj.color, marker='.', s=int(obj.markersize), label=obj.name))
                else:
                    orbit = np.array(obj.orbit)
                    elems.append(ax.scatter(orbit[i, 0], orbit[i, 1], c=obj.color, marker='.', s=int(obj.markersize), label=obj.name))
                    elems += ax.plot(
                        orbit[max(i - orbit_length, 0):i, 0], orbit[max(i - orbit_length, 0):i, 1],
                        color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                    )
        else:
            for obj in self.objects:
                if obj is center_obj:
                    elems.append(ax.scatter(0, 0, color=obj.color, marker='.', s=int(obj.markersize), label=obj.name))
                else:
                    c_orbit = np.array(center_obj.orbit)
                    if(obj.fixed is True):
                        elems.append(ax.scatter(obj.x[0] - c_orbit[i, 0], obj.x[1] - c_orbit[i, 1], c=obj.color, marker='.', s=int(obj.markersize), label=obj.name))
                        elems += ax.plot(
                            obj.x[0] - c_orbit[max(i - orbit_length, 0):i, 0], obj.x[1] - c_orbit[max(i - orbit_length, 0):i, 1],
                            color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                        )
                    else:
                        orbit = np.array(obj.orbit)
                        elems.append(ax.scatter(orbit[i, 0] - c_orbit[i, 0], orbit[i, 1] - c_orbit[i, 1], c=obj.color, marker='.', s=int(obj.markersize), label=obj.name))
                        elems += ax.plot(
                            orbit[max(i - orbit_length, 0):i, 0] - c_orbit[max(i - orbit_length, 0):i, 0], orbit[max(i - orbit_length, 0):i, 1] - c_orbit[max(i - orbit_length, 0):i, 1],
                            color='black', linestyle='dashed', linewidth='0.5', markersize=obj.markersize
                        )
        ax.legend(loc=loc, bbox_to_anchor=bbox_to_anchor, borderaxespad=borderaxespad)


class Planet():
    def __init__(self, mass, color='red', fixed=False, linestyle='solid', linewidth='1', markersize='5', name=None):
        self.mass = mass
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.markersize = markersize
        self.fixed = fixed
        self.name = name
        self.x = None
        self.v = None
        self.orbit = []

    def initial_pos(self, pos):
        self.x = pos
        self.orbit = []
        self.orbit.append(copy.copy(self.x))

    def initial_vel(self, vel):
        self.v = vel

    @ classmethod
    @ property
    def mass(self):
        return self.mass


class Spacecraft:
    def __init__(self, mass, color='green', linestyle='solid', linewidth='1', markersize='1', name=None):
        self.mass = mass
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.markersize = markersize
        self.fixed = False
        self.name = name
        self.x = None
        self.v = None
        self.orbit = []
        self.injection = []

    def initial_pos(self, pos):
        self.x = pos
        self.orbit = []
        self.orbit.append(copy.copy(self.x))

    def initial_vel(self, vel):
        self.v = vel

    def appendInjection(self, start, last, force, theta, phi=0.0):
        dic = {'start': start, 'last': last, 'force': force, 'theta': theta, 'phi': phi}
        self.injection.append(dic)

    def resetInjection(self):
        self.injection = []
