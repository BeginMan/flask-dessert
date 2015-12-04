# coding=utf-8
"""
return json
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""

from flask import Flask, Response,jsonify

# version1
return jsonify(
    name='beginman',
    id=1001
)

# version2
dat = {'name': 'beginman'}      # your JSON serialized data
resp = Response(
    response=dat,
    status=200,
    mimetype="application/json")
return(resp)
