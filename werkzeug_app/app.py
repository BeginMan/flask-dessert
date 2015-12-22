# coding=utf-8
"""
desc..
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '12/22/15'
from werkzeug.wrappers import Response, Request


def application(environ, start_response):
    """
    一个基本的WSGI 应用看起来是这样的:
    >>>def application(environ, start_response):
        ...#WSGI应用与环境通信，可调用的start_response用来表明已经收到的一个响应
        ...start_response('200 OK', [('Content-Type', 'text/plain')])
        ...return ['Hello World!']
    如下是Werkzeug提供的方式
    """
    request = Request(environ)
    txt = u'信息统计接口:log:%s' % request.args.get('name', 'username')
    response = Response((txt, 'mimetype=text/plain'))
    return response(environ, start_response)
