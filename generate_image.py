import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load
from skyfield.api import Topos
from argparse import ArgumentParser

def create_image(planets, filename=None):
    plt.rcParams['axes.facecolor'] = 'black'
    azimuths = [planets[planet]['az'] for planet in planets]
    theta = [90 - planets[planet]['az'] for planet in planets]
    r = [90 - planets[planet]['alt'] for planet in planets]
    colors =["white", "purple", "red", "orange", "magenta", "green", "blue"]
    colors = colors[:len(azimuths)]

    for i, azimuth in enumerate(reversed(azimuths)):
        if(azimuth < 0):
            del theta[i]
            del r[i]
            del colors[i]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.set_rlim(0,100)
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    c = ax.scatter(theta, r, c=colors, cmap='hsv', alpha=0.75)

    if filename:
        plt.savefig(filename)
