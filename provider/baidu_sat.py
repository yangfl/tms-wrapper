from . import baidu
from functools import lru_cache
import urllib.request
import urllib.error


BASEURL = 'http://shangetu0.map.bdimg.com/it/u=x={};y={};z={};v=009;type=sate&fm=46'


@lru_cache(1024)
def bd_sat_tile(x, y, z):
    print('fetch:', x, y, z)
    print(BASEURL.format(x, y, z))
    return urllib.request.urlopen(BASEURL.format(x, y, z)).read()


@lru_cache(64)
def fetch(x, y, z):
    if not 2 <= z <= 18:
        raise urllib.error.HTTPError('', 404, '', '', BytesIO())
    return baidu.fetch(x, y, z, bd_sat_tile)
