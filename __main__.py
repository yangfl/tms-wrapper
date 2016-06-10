#!/usr/bin/env python3
import urllib.error
try:
    import gevent.pywsgi
except ImportError:
    gevent = None


from provider import fetch
from bottle import Bottle, abort, route, run, response


app = Bottle()


@app.route('/<pro>/<z:int>/<x:int>/<y:int>')
def main(pro, x, y, z):
    try:
        content = fetch(pro, x, y, z)
    except urllib.error.HTTPError as err:
        abort(err.code, err.msg)
    response.set_header('Content-Type', 'image/png')
    return content



if gevent:
    server = gevent.pywsgi.WSGIServer(("0.0.0.0", 8080), app)
    server.serve_forever()
else:
    run(app, debug=True, server='gevent')
