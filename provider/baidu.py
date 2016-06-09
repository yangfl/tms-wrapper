from math import *
from functools import lru_cache
from PIL import Image
import urllib.request
import urllib.error
from io import BytesIO
import threading

from vendor import coord


R = 6378137
BASEURL = 'http://online2.map.bdimg.com/onlinelabel/?qt=tile&x={}&y={}&z={}&styles=pl'


def tileno(lat, lon, z):
    lat -= 0.1703521
    lon -= 0.0103876
    r_lat = radians(lat)
    m, x = modf(radians(lon) * R / (1 << 26 - z))
    n, y = modf(log(tan(r_lat) + 1 / cos(r_lat)) * R / (1 << 26 - z))
    x = int(x)
    y = int(y)
    m = floor(256 * m)
    n = floor(256 * n)
    if n:
        n = 256 - n
    else:
        y -= 1
    return (x, y, z, m, n)


@lru_cache(1024)
def bd_tile(x, y, z):
    print('fetch:', x, y, z)
    print(BASEURL.format(x, y, z))
    return urllib.request.urlopen(BASEURL.format(x, y, z)).read()


@lru_cache(64)
def fetch(x, y, z, tile=bd_tile):
    if not 2 <= z <= 18:
        raise urllib.error.HTTPError('', 404, '', '', BytesIO())
    bd_z = z + 1

    bd_x, bd_y, _, bd_x_m, bd_y_n = tileno(
        *coord.wgs2bd(*coord.tms2coord(x, y, z)), bd_z)
    bd_x_max, bd_y_min, _, bd_x_max_m, bd_y_min_n = tileno(
        *coord.wgs2bd(*coord.tms2coord(x + 1, y + 1, z)), bd_z)
    bd_x_max += 1
    bd_y_min -= 1
    bd_x_max_m -= 1
    bd_y_min_n += 1
    new_img = Image.new(
        'RGB', (256 * (bd_x_max - bd_x), 256 * (bd_y - bd_y_min)))
    l_thread = []
    for bd_x_cur in range(bd_x, bd_x_max):
        for bd_y_cur in range(bd_y, bd_y_min, -1):
            t = threading.Thread(
                target=lambda: tile(bd_x_cur, bd_y_cur, bd_z))
            t.start()
            l_thread.append(t)
    for t in l_thread:
        t.join()
    for bd_x_cur in range(bd_x, bd_x_max):
        for bd_y_cur in range(bd_y, bd_y_min, -1):
            new_img.paste(
                Image.open(BytesIO(tile(bd_x_cur, bd_y_cur, bd_z))),
                (256 * (bd_x_cur - bd_x), 256 * (bd_y - bd_y_cur)))
    content = BytesIO()
    new_img.crop((
        bd_x_m, bd_y_n,
        256 * (bd_x_max - bd_x - 1) + bd_x_max_m,
        256 * (bd_y - bd_y_min - 1) + bd_y_min_n)
    ).resize((256, 256), Image.ANTIALIAS).save(content, format='PNG')
    content.seek(0)
    return content.read()
