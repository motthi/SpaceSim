import spacesim
from spacesim.core import *
from spacesim.planet import *


def moonPerturbation_20210213():
    dis_earth_moon = 384400000
    earth_pos = np.array([0.0, 0.0])
    moon_pos = np.array([dis_earth_moon, 0.0])
    earth_vel = np.array([0.0, 0.0])
    moon_vel = np.array([0.0, 1022.0])

    earth = Planet(mass_earth, color='blue', fixed=True)
    moon = Planet(mass_moon, color='brown')
    nozomi = Spacecraft(500.0)

    earth.initial_pos(earth_pos)
    earth.initial_vel(earth_vel)
    moon.initial_pos(moon_pos)
    moon.initial_vel(moon_vel)
    nozomi.initial_pos(np.array([0.0, -1e8]))
    nozomi.initial_vel(np.array([2600.0, 0.0]))

    space = Space(step=2000, end=86400 * 90)
    space.append(earth)
    space.append(moon)
    space.append(nozomi)

    space.play(step_dur=10)
    #space.plotOrbit(ax_lim=(5e8, 5e8))
    space.animateOrbit(frames=len(moon.orbit), ax_lim=(5e8, 5e8), interval=1, center_obj=None)
    #space.ani.save("moon.gif", writer="imagemagick")


def solarsystem():
    sun = Sun(fixed=False)
    mercury = Mercury()
    venus = Venus()
    earth = Earth()
    mars = Mars()
    jupiter = Jupiter()
    saturn = Saturn()
    uranus = Uranus()
    neptune = Neptune()

    space = Space(step=8640, end=86400 * 785)
    space.append(sun)
    space.append(mercury)
    space.append(venus)
    space.append(earth)
    space.append(mars)
    # space.append(jupiter)
    # space.append(saturn)
    # space.append(uranus)
    # space.append(neptune)
    space.play(step_dur=10)
    center_obj = None
    lim = 3e11  # 3e11, 1e13
    ax_lim = (lim, lim)
    space.plotOrbit(ax_lim=ax_lim, center_obj=center_obj)
    space.animateOrbit(frames=len(earth.orbit), ax_lim=ax_lim, interval=1, center_obj=center_obj, orbit_length=100)
    #space.ani.save("moon.gif", writer="imagemagick")


def moonPerturbation_20210214():
    dis_earth_moon = 384400000
    earth_pos = np.array([0.0, 0.0])
    moon_pos = np.array([dis_earth_moon, 0.0])
    earth_vel = np.array([0.0, 0.0])
    moon_vel = np.array([0.0, 1022.0])

    earth = Planet(mass_earth, color='blue', fixed=True)
    moon = Planet(mass_moon, color='brown')
    nozomi = Spacecraft(500.0)

    earth.initial_pos(earth_pos)
    earth.initial_vel(earth_vel)
    moon.initial_pos(moon_pos)
    moon.initial_vel(moon_vel)
    nozomi.initial_pos(np.array([0.0, -800000]))
    nozomi.initial_vel(np.array([31560.0, 0.0]))

    space = Space(step=10, end=86400 * 120)
    space.append(earth)
    space.append(moon)
    space.append(nozomi)

    space.play(step_dur=100)
    space.plotOrbit(ax_lim=(5e8, 5e8))
    #space.animateOrbit(frames=len(moon.orbit), ax_lim=(5e9, 5e9), interval=1, center_obj=None)
    #space.ani.save("moon.gif", writer="imagemagick")


def moonPerturbation_20210218():
    dis_earth_moon = 384400000
    theta = np.pi / 17.8
    earth_pos = np.array([0.0, 0.0])
    moon_pos = cartesianToCircle(dis_earth_moon, theta)
    earth_vel = np.array([0.0, 0.0])
    moon_vel = cartesianToCircle(1022, np.pi - (np.pi / 2 - theta))

    earth = Planet(mass_earth, color='blue', fixed=True)
    moon = Planet(mass_moon, color='brown')
    nozomi = Spacecraft(500.0)

    earth.initial_pos(earth_pos)
    earth.initial_vel(earth_vel)
    moon.initial_pos(moon_pos)
    moon.initial_vel(moon_vel)
    nozomi.initial_pos(np.array([0, -1e8]))
    nozomi.initial_vel(np.array([2600.0, 0.0]))

    space = Space(step=2000, end=86400 * 320)
    space.append(earth)
    space.append(moon)
    space.append(nozomi)

    ax_lim = (1e9, 1e9)
    space.play(step_dur=5)
    # space.plotOrbit(ax_lim=ax_lim)
    space.animateOrbit(frames=len(moon.orbit), ax_lim=ax_lim, interval=1, center_obj=None)
    #space.ani.save("moon.gif", writer="imagemagick")


def moonPerturbation_20210219():
    dis_earth_moon = 384400000
    #theta = np.pi / 3.733
    theta = np.pi / 3.385 + np.pi
    earth_pos = np.array([0.0, 0.0])
    moon_pos = cartesianToCircle(dis_earth_moon, theta)
    earth_vel = np.array([0.0, 0.0])
    moon_vel = cartesianToCircle(1022, np.pi - (np.pi / 2 - theta))

    earth = Planet(mass_earth, color='blue', fixed=True)
    moon = Planet(mass_moon, color='brown')
    nozomi = Spacecraft(500.0)

    earth.initial_pos(earth_pos)
    earth.initial_vel(earth_vel)
    moon.initial_pos(moon_pos)
    moon.initial_vel(moon_vel)
    nozomi.initial_pos(np.array([0, 7.42e8]))
    nozomi.initial_vel(np.array([-140.0, 0.0]))

    space = Space(step=200, end=86400 * 120)
    space.append(earth)
    space.append(moon)
    space.append(nozomi)

    ax_lim = (2e9, 2e9)
    space.play(step_dur=100)
    space.animateOrbit(frames=len(nozomi.orbit), ax_lim=ax_lim, interval=1, center_obj=None, orbit_length=0)
    # space.plotOrbit(ax_lim=ax_lim)
    #space.ani.save("input.gif", writer="imagemagick")


if __name__ == "__main__":
    solarsystem()
