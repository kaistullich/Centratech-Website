from flask import render_template, request, redirect, url_for, flash
from my_app.source.models import ProductForm
from my_app.source.models import cursor, conn

#------------ THIS WILL SHOW ALL PRODUCTS TABLE -------------------
def products():
	command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name
	             FROM {a} 
                 JOIN {b} 
                 ON {a}.category_id = {b}.id
	    """.format(a="product", b='category')
	cursor.execute(command)
	product_data = cursor.fetchall()  
	
	return render_template('products.html', my_list=product_data)

# ---------- THIS WILL SHOW A SINGLE PRODUCT ---------------------
def product(key):    
    command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.image, {a}.stock
                      FROM {a} 
                      JOIN {b} 
                      ON {a}.category_id = {b}.id
                      WHERE {a}.id = {p1}
        """.format(a="product", b='category', p1=key)
    cursor.execute(command)
    product_data = cursor.fetchall()  
      
    if len(product_data) == 0:
        return "The key "+ key + " was not found" 
    item = product_data[0]    

    return render_template('product.html', single_product=item)


# ---------------------- CREATE A NEW PRODUCT -------------------
def product_create():
    command = """ SELECT MAX(id)
                    FROM product
            """
    cursor.execute(command)
    next_id = cursor.fetchone()   
    product_id = next_id[0]+1
        
    form = ProductForm(request.form, csrf_enabled=False)

    command = """ SELECT * FROM category """
    cursor.execute(command)
    categories = cursor.fetchall()

    form.category.choices = categories
    
    if request.method == 'POST' and form.validate():
        name = form.name.data
        price = form.price.data
        category = form.category.data
        url = form.url.data
        stock = form.stock.data
        
        command = """
            INSERT INTO product 
            (id,name,price,category_id,image,stock) 
            VALUES 
            ({i},'{n}',{p},{c},'{im}',{s})
            """.format(i=product_id, n=name, p=price, c=category, im=image, s=stock)
        
        cursor.execute(command)
        conn.commit()
        
        flash('"{}" was successfully created!'.format(name))
        return redirect(url_for('my_view.product', key=product_id))

    if form.errors:
        flash(form.errors, 'Something went wrong! Retry!')

    return render_template('product-create.html', form=form, product_id=product_id)



















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