import urllib.request


BASEURL = 'http://r1.tiles.ditu.live.com/tiles/r{}.png?g=100'


def tileno(x, y, z):
    index = []
    mask = 1 << z >> 1
    while mask:
        index.append(chr(48 + (1 if x & mask else 0) +
                         (2 if y & mask else 0)))
        mask >>= 1
    return ''.join(index)


def fetch(x, y, z):
    return urllib.request.urlopen(BASEURL.format(tileno(x, y, z))).read()
