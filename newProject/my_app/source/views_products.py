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

# ------------------ PRODUCT SEARCHING ---------------------------

def product_search():  
    name = request.args.get('name')
    price = request.args.get('price')
    price_greater_equal = request.args.get('price_ge')
    price_smaller_equal = request.args.get('price_se')
    category = request.args.get('category')
    brand = request.args.get('brand')
    year = request.args.get('year')
    rating = request.args.get('rating')
    stock = request.args.get('stock')
    
    condition = ""
    if name != None:
        condition += "product.name LIKE '%" +name+ "%'"
    if price != None:
        if condition !="":
            condition += " AND "
        condition += "product.price=" +str(price)
    if category != None:
        if condition != "":
            condition += " AND "
        condition  += "category.name LIKE '%" +category+ "%'"
    if brand != None:
        if condition != "":
            condition += " AND "
        condition  += "product.brand LIKE '%" +brand+ "%'"
    if price_greater_equal != None:
        if condition != "":
            condition += " AND "
        condition  += "product.price >= " + str(price_greater_equal)
    if price_smaller_equal != None:
        if condition != "":
            condition += " AND "
        condition  += "product.price <= " + str(price_smaller_equal) 
            
           
    if condition == "":
        command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name
                          FROM {a} 
                          JOIN {b} 
                          ON {a}.category_id = {b}.id
            """.format(a="product", b='category')        
    else:
        command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name
                          FROM {a} 
                          JOIN {b} 
                          ON {a}.category_id = {b}.id
                          WHERE {cond}
            """.format(a="product", b='category', cond = condition)
       
    cursor.execute(command)
    product_data = cursor.fetchall()
    return render_template('products.html', my_list=product_data)





    # --------------------------