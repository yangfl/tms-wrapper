from . import bing
from vendor.combine import Combine, earth2mars


bing_combiner = Combine(bing.bing_url, earth2mars)


def fetch(x, y, z):
    return bing_combiner.get(x, y, z)
