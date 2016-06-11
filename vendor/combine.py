from math import *
from functools import lru_cache
from io import BytesIO
import threading
import urllib.request
from PIL import Image

from vendor import coord


def autorange(start, stop):
    if start < stop:
        return range(start, stop + 1)
    else:
        return range(start, stop - 1, -1)


def pixel2grid(x, y, z):
    m, x = divmod(x, 256)
    n, y = divmod(y, 256)
    return x, y, z, m, n


def earth2mars(x, y, z):
    return coord.wgs2tms(*coord.wgs2gcj(*coord.tms2wgs(x, y, z)), z)


class Combine:
    def __init__(self, tile_url, tms2tgt, cache_size=128):
        self.tile_service = lru_cache(cache_size)(
            lambda x, y, z: urllib.request.urlopen(tile_url(x, y, z)).read())
        self.tms2tgt = tms2tgt

    def get(self, x, y, z):
        tgt_x, tgt_y, tgt_z, tgt_m, tgt_n = self.tms2tgt(x, y, z)
        tgt_to_x, tgt_to_y, tgt_z, tgt_to_m, tgt_to_n = self.tms2tgt(
            x + 1, y + 1, z)
        l_thread = []
        for tgt_cur_x in autorange(tgt_x, tgt_to_x):
            for tgt_cur_y in autorange(tgt_y, tgt_to_y):
                t = threading.Thread(target=lambda: self.tile_service(
                    tgt_cur_x, tgt_cur_y, tgt_z))
                t.start()
                l_thread.insert(0, t)
        tgt_img = Image.new('RGB', (
            256 * (abs(tgt_to_x - tgt_x) + 1),
            256 * (abs(tgt_to_y - tgt_y) + 1)))
        for tgt_cur_x in autorange(tgt_x, tgt_to_x):
            for tgt_cur_y in autorange(tgt_y, tgt_to_y):
                l_thread.pop().join()
                tgt_img.paste(
                    Image.open(BytesIO(self.tile_service(
                        tgt_cur_x, tgt_cur_y, tgt_z))),
                    (
                        256 * abs(tgt_cur_x - tgt_x),
                        256 * abs(tgt_cur_y - tgt_y)))
        content = BytesIO()
        tgt_img.crop((
            tgt_m, tgt_n, 256 * abs(tgt_to_x - tgt_x) + tgt_to_m,
            256 * abs(tgt_to_y - tgt_y) + tgt_to_n
        )).resize((256, 256), Image.ANTIALIAS).save(content, format='PNG')
        content.seek(0)
        return content.read()

