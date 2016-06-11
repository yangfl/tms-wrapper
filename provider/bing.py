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


def bing_url(x, y, z):
    return BASEURL.format(p.get((x, y, z)), tileno(x, y, z))


def fetch(x, y, z):
    redirect(bing_url(x, y, z))
