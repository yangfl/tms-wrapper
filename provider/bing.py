import urllib.request
from bottle import redirect

from vendor.pool import Pool

BASEURL = 'http://r{}.tiles.ditu.live.com/tiles/r{}.png?g=100'
p = Pool(4)


def tileno(x, y, z):
    index = []
    mask = 1 << z >> 1
    while mask:
        index.append(chr(48 + (1 if x & mask else 0) +
                         (2 if y & mask else 0)))
        mask >>= 1
    return ''.join(index)


def fetch(x, y, z):
    no = tileno(x, y, z)
    redirect(BASEURL.format(p.get(no), no))
