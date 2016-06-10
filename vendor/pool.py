import time


class Pool:
    def __init__(self, _max, _min=0):
        self._max = _max
        self._min = _min
        self._range = self._max - self._min
        self._init = int(time.time() * 1000) % self._range

    def get(self, token):
        return (hash(token) + self._init) % self._range + self._min
