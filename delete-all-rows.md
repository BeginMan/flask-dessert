对于批量删除,如果使用`db.session.delete`则会报错：

	>>> users = models.User.query.all()
	>>> db.session.delete(users)

	# but it errs out: UnmappedInstanceError: Class '__builtin__.list' is not mapped

参考[sqlalchemy文档](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.delete)，可这样操作：

	User.query.delete()
	# Returns the number of rows deleted, excluding any cascades


