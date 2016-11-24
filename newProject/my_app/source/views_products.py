from flask import render_template, request, redirect, url_for, flash
from my_app.source.models import ProductForm
from my_app.source.models import cursor, conn

#------------ THIS WILL SHOW ALL PRODUCTS TABLE -------------------
def products():
	command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name
	            FROM {a} JOIN {b} ON {a}.category_id = {b}.id
	    """.format(a="product", b='category')
	cursor.execute(command)
	product_data = cursor.fetchall()  
	
	return render_template('products.html', my_list=product_data)