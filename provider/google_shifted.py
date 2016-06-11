from vendor.pool import Pool
from vendor.combine import Combine, earth2mars

BASEURL = 'http://mt{}.google.cn/vt/x={}&y={}&z={}'
p = Pool(4)


def google_url(x, y, z):
    return BASEURL.format(p.get((x, y, z)), x, y, z)


google_combiner = Combine(google_url, earth2mars)


def fetch(x, y, z):
    return google_combiner.get(x, y, z)
