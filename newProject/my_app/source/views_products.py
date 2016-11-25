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

# ---------- THIS WILL SHOW A SINGLE PRODUCT ---------------------
def product(key):    
    command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.image, {a}.stock
                      FROM {a} join {b} ON {a}.category_id = {b}.id
                      WHERE {a}.id = {p1}
        """.format(a="product", b='category', p1=key)
    cursor.execute(command)
    product_data = cursor.fetchall()  
      
    if len(product_data) == 0:
        return "The key "+ key + " was not found" 
    item = product_data[0]    

    return render_template('product.html', single_product=item)

# --------------------------