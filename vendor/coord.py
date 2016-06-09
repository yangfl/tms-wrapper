from math import *

from .eviltransform import *


def tms2coord(x, y, z):
    return (
        degrees(atan(exp((1 - 2 * y / (1 << z)) * pi))) * 2 - 90,
        (2 * x / (1 << z) - 1) * 180)
