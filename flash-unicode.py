#!/usr/bin/env python
# encoding: utf-8

# flash("中文")  --> raise UnicodeDecodeError

# 注意flask基于Unicode编码，所以在模板和你的程序中最好使用unicode
flash(u"中文")
# 或者设置系统编码

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

flash("中文")
