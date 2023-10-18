"""
Brody Soedel
Calculates the orbital velocity of a given orbit's altitude
"""

from scipy import constants as c
import math


def velocity(mass, distance, radius):
    # v = sqrt((G * M) / r)
    # improve naming
    r = distance + radius
    return math.sqrt((c.G * mass) / r)
