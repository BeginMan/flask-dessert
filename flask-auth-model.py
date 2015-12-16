# coding: utf-8
# 两种常见风格的flask User model处理

# type 1:

import datetime
import sqlalchemy.exc
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash


db = SQLAlchemy()


def _utf8(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    return s


class Base(db.Model):

    __abstract__ = True

    @declared_attr
    def id(cls):
        return db.Column('id', db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(i) for i in ids]


class User(Base):

    __tablename__ = 'user'

    name = db.Column(db.String(255), unique=True, nullable=False, default='')
    email = db.Column(db.String(255), unique=True, nullable=False, default='')
    password = db.Column(db.String(255), nullable=False, default='')
    privilege = db.Column(db.Integer, default=0)
    time = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def create(cls, name, email, password):
        try:
            u = cls(name=name, email=email)
            db.session.add(u)
            db.session.commit()
            u.set_password(password)
            return u
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_auths(self):
        return Auth.query.filter_by(user_id=self.id).order_by(Auth.id.desc()).all()

    def to_dict(self):
        return {'name': self.name, 'email': self.email}


class Auth(Base):

    __tablename__ = 'auth'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'url'),
    )

    url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(64), default=lambda: gen_salt(64))
    time = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def get_or_create(cls, user_id, url):
        auth = cls.get_by_user_and_url(user_id, url)
        if auth:
            return auth
        try:
            auth = cls(user_id=user_id, url=url)
            db.session.add(auth)
            db.session.commit()
            return auth
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_user_and_url(cls, user_id, url):
        return cls.query.filter_by(user_id=user_id, url=url).first()

    @classmethod
    def get_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @property
    def user(self):
        return User.get(self.user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# or type 2
from flask.ext.login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TJWS

from flask import current_app

login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __bind_key__ ='local'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.BOOLEAN, default=False)             # 邮箱确认

    def __repr__(self):
        return '<User %r>' % self.email

    # 密码相关
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 确认相关
    def generate_confirmation_token(self, expiration=3600*24):
        """生成JWS Token"""
        s = TJWS(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """验证"""
        s = TJWS(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id):
    """加载用户的回调函数"""
    return User.query.get(int(user_id))
