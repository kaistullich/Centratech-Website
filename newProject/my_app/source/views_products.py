from flask import render_template, request, redirect, url_for, flash
from my_app.source.models import cursor, conn

#------------------------ SHOW ALL products-------------------
def products():
    #selects all product.id,name,price and category.name
	command = """SELECT {a}.id, {a}.brand, {a}.name, {a}.price, {b}.name, {a}.image
	             FROM {a} 
                 JOIN {b} 
                 ON {a}.category_id = {b}.id
	    """.format(a="product", b='category')
	cursor.execute(command)
	product_data = cursor.fetchall()  
	# takes 'command' and renders the template products.html
	return render_template('products.html', my_list=product_data)

# ------------------------SINGLE product ---------------------
def product(key):    
    # selects all columns shown
    command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.image, {a}.stock, {a}.description
                      FROM {a} 
                      JOIN {b} 
                      ON {a}.category_id = {b}.id
                      WHERE {a}.id = {p1}
        """.format(a="product", b='category', p1=key)
    cursor.execute(command)
    # fetches all the columns from the command variable
    product_data = cursor.fetchall()  
    # if the len of product_data DB is too long it will show error 
    if len(product_data) == 0:
        flash('Key not found, please try again!')
    item = product_data[0]    
    # renders template to show a single product
    return render_template('product.html', single_product=item, key=key)

# ------------------ PRODUCT SEARCHING ---------------------------
# Product Search Function
def product_search():  
    # All the arguments 
    name = request.args.get('name')
    price = request.args.get('price')
    price_greater_equal = request.args.get('price_ge')
    price_smaller_equal = request.args.get('price_se')
    category = request.args.get('category')
    brand = request.args.get('brand')
    year = request.args.get('year')
    rating = request.args.get('rating')
    stock = request.args.get('stock')
    # Creates the argument for each varibale from above
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
            
    # Creates the query from the DB
    if condition == "":
        command = """SELECT {a}.id, {a}.brand, {a}.name, {a}.price, {b}.name, {a}.image
                          FROM {a} 
                          JOIN {b} 
                          ON {a}.category_id = {b}.id
            """.format(a="product", b='category')        
    else:
        command = """SELECT {a}.id, {a}.brand, {a}.name, {a}.price, {b}.name, {a}.image
                          FROM {a} 
                          JOIN {b} 
                          ON {a}.category_id = {b}.id
                          WHERE {cond}
            """.format(a="product", b='category', cond = condition)
    # Executes either command depending on the search type
    cursor.execute(command)
    product_data = cursor.fetchall()
    # When user hits submit on search it will render template with the returned searches
    return render_template('products.html', my_list=product_data)