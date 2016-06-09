#!/usr/bin/env python3
import urllib.error

from provider import fetch
from vendor.bottle import abort, route, run, response


@route('/<pro>/<z:int>/<x:int>/<y:int>')
def main(pro, x, y, z):
    try:
        content = fetch(pro, x, y, z)
    except urllib.error.HTTPError as err:
        abort(err.code, err.msg)
    response.set_header('Content-Type', 'image/png')
    return content


run(debug=True)
