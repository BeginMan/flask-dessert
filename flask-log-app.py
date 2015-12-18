# coding=utf-8
"""
add log.
ps>!!不知道怎么回事在flask-script下add log不起作用，这个问题有待解决.

    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '12/18/15'

import logging
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    assert 0 == 1       # test
    return 'test'


if __name__ == '__main__':

    file_handler = logging.FileHandler('flask.log', encoding='UTF-8')
    file_handler.setLevel(logging.DEBUG)
    # logging_format = logging.Formatter(
    #     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # file_handler.setFormatter(logging_format)
    app.logger.addHandler(file_handler)

    app.run(port=8000)