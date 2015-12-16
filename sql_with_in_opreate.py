#!/usr/bin/env python
# encoding: utf-8
# sqlalchemy原始sql查询，`in`操作符实践

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql://yourName:yourPasswd@yourIP/yourDBName?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)

raw = DB_Session()

phones = ("15409977765", "15409977767", "15409977768", "15409977769")
params = ','.join(('"%s",' * len(phones)).split(',')[:-1]) % phones
sql = "select phone, user_id from users where phone in (%s)" % params
result = raw.execute(sql).fetchall()
result = dict(result)


