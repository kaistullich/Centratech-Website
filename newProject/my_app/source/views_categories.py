from flask import render_template, request, redirect, url_for, flash
from my_app.source.models import CategoryForm
from my_app.source.models import cursor, conn


#-------------------- Category Handler --------------------
def categories():   
	command = """SELECT {a}.id, {a}.name
					  FROM {a} 
			  """.format(a='category')
	cursor.execute(command)
	category_data = cursor.fetchall()  
	
	return render_template('categories.html', my_list=category_data)

#-------------------- Category Key Handler --------------------
def category(key):
	command = """ SELECT *
					FROM category
					WHERE category.id = {p1}
			""".format(p1=key)
	cursor.execute(command)
	category_name = cursor.fetchall()[0][1]

	command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.image
					  FROM {a} join {b} ON {a}.category_id = {b}.id
					  WHERE {a}.category_id = {p1}
		""".format(a="product", b='category', p1=key)
	cursor.execute(command)
	product_data = cursor.fetchall()  
   
	return render_template('category.html', category_id = key, category_name=category_name, 
							my_list=product_data)

# ----------------- Category Create -----------------
def category_create():
	command = """ SELECT MAX(id)
					FROM category
			"""
	cursor.execute(command)
	next_id = cursor.fetchone() 
	category_id = next_id[0]+1
	
	form = CategoryForm(request.form)
	   
	result = None
	if request.method == 'POST' and form.validate():
		name = form.name.data
		deptPhone = form.deptPhone.data
		deptLine = form.deptLine.data
		deptManager = form.deptManager.data
		
		command = """
			INSERT INTO category 
			(id,name, deptPhone, deptLine, deptMang) VALUES 
			({i},'{n}', {dp}, {dl}, '{dm}')
			""".format(i=category_id, n=name, dp=deptPhone, dl=deptLine, dm=deptManager)
		
		cursor.execute(command)
		conn.commit()
		
		flash('The category %s, ID: %d has been created' % (name,category_id), 'success')
		return redirect(url_for('my_view.categories'))
	
	return render_template('category-create.html', form=form, result=result)