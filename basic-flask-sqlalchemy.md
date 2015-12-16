# 一、为你的Flask应用加载Flask-SqlAlchemy扩展

	from flask import Flask
	from flask.ext.sqlalchemy import SQLAlchemy
	 
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
	db = SQLAlchemy(app)  #这个就是你以后操作数据库的对象实例了

SQLALCHEMY_DATABASE_URI格式实例：

	postgresql://scott:tiger@localhost/mydatabase
	mysql://scott:tiger@localhost/mydatabase
	oracle://scott:tiger@127.0.0.1:1521/sidname
	sqlite:////absolute/path/to/foo.db #注意：有3个斜杠+路径


# 二、建立数据库模型和初始化数据库

建立数据库模型：

	import hashlib
	from app import db  #在数据库模型文件中导入上面建立的db对象
	 
	class User(db.Model):
	    id = db.Column(db.Integer, primary_key=True)  # id
	    username = db.Column(db.String(80), unique=True)
	    email = db.Column(db.String(320), unique=True)
	    password = db.Column(db.String(32), nullable=False)
	 
	    def __init__(self, username, email, password):
	        self.username = username
	        self.email = email
	        self.password= hashlib.md5(password) 

	    def __repr__(self):
	        return "<User '{:s}'>".format(self.username)

初始化数据库也特别简单，只需要调用 db.create_all() 函数就可以了。
	
	db.create_all()

# 三、插入数据

	u = User(username='peter', email='test@example.com', password='123456')
	db.session.add(u)  		# 插入数据
	# or
	db.session.add_all([u, ....])  
	db.session.commit()  	# 只有提交事务了，才可以获取(u.id)数据的ID值。

# 四、查询数据

### 用主键获取数据：

	User.query.get(1)
	<User u'admin'>

### 通过一个精确参数进行反查：

	peter = User.query.filter_by(username='peter').first()  #注意：精确查询函数query.filter_by()，是通过传递参数进行查询；其他增强型查询函数是query.filter()，通过传递表达式进行查询。
	print(peter.id)  #如果数据不存在则返回None

### 模糊查询：

	User.query.filter(User.email.endswith('@example.com')).all()
	[<User u'admin'>, <User u'guest'>]

### 逻辑非：

	User.query.filter(User.username != 'peter').first()

	from sqlalchemy import not_
	User.query.filter(not_(User.username=='peter')).first()

### 逻辑与：
	
	from sqlalchemy import and_
	User.query.filter(and_(User.username=='peter', User.email.endswith('@example.com'))).first()

### 逻辑或：

	from sqlalchemy import or_
	User.query.filter(or_(User.username != 'peter', User.email.endswith('@example.com'))).first()

# 六、查询数据加工
排序和限制函数可以跟在query或filter后面。

排序：

	User.query.order_by(User.username) 
	[<User u'admin'>, <User u'guest'>, <User u'peter'>]

	# 降序
	User.query.order_by(User.id.desc())


限制返回的数目：

	User.query.limit(1).all()
	[<User u'admin'>]

# 七、查询数据返回

	# one
	User.query.first()

	# all
	User.query.all()

# 八、删除数据

	u = User.query.first()
	db.session.delete(u) 
	db.session.commit()

# 九、更新数据

	admin = User.query.filter_by(username='admin').first()
	admin.email = 'my_new_email@example.com'
	db.session.commit()

	user = User.query.get(5)
	user.name = 'New Name'
	db.session.commit()

	# or
	admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
	db.session.commit()


参考：[Flask-SQLAlchemy 学习](http://www.itwhy.org/%E6%95%B0%E6%8D%AE%E5%BA%93/flask-sqlalchemy-%E5%AD%A6%E4%B9%A0.html)

