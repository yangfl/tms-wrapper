from math import *

from .eviltransform import *


def tms2wgs(x, y, z, m=0, n=0):
    return (
        degrees(atan(exp((1 - 2 * (y + n / 256) / (1 << z)) * pi))) * 2 - 90,
        (2 * (x + m /256) / (1 << z) - 1) * 180)


def wgs2tms(lat, lon, z):
    x, m = divmod(round((lon / 180 + 1) * (1 << (z + 7))), 256)
    r_lat = radians(lat)
    y, n = divmod(round((1 - (log(sin(r_lat) + 1) - log(cos(r_lat))) / pi) *
                        (1 << (z + 7))), 256)
    return x, y, z, m, n
