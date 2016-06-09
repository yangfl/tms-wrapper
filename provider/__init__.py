def fetch(pro, x, y, z):
    return __import__(pro, globals(), level=1).fetch(x, y, z)
