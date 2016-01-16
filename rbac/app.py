# coding=utf-8
"""
desc..
    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '1/16/16'
from flask import Flask
from flask.ext.rbac import RBAC
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['RBAC_USE_WHITE'] = True
app.config.update(
    DEBUG=True,
    SECRET_KEY='...',
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_DATABASE_URI='mysql://@127.0.0.1/app'
)

db = SQLAlchemy(app)
rbac = RBAC(app)
