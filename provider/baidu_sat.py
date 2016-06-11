from . import baidu


BASEURL = 'http://shangetu{}.map.bdimg.com/it/u=x={};y={};z={};v=009;type=sate&fm=46'


bd_combiner = baidu.Combine(baidu.bd_url_formatter(BASEURL), baidu.tms2bd)


def fetch(x, y, z):
    if not 2 <= z <= 18:
        raise ValueError
    return bd_combiner.get(x, y, z)
