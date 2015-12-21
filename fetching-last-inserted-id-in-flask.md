
	from yourapp import Mymodel
	md = Mymodel()
	db.session.add(md)
	db.session.commit()

and after that you can see the id

	print md.id


