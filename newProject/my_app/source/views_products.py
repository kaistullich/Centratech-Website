from flask import render_template, request, redirect, url_for, flash
from my_app.source.models import ProductForm
from my_app.source.models import cursor, conn

#------------------------ SHOW ALL products-------------------
def products():
	command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name
	             FROM {a} 
                 JOIN {b} 
                 ON {a}.category_id = {b}.id
	    """.format(a="product", b='category')
	cursor.execute(command)
	product_data = cursor.fetchall()  
	
	return render_template('products.html', my_list=product_data)

# ------------------------SINGLE product ---------------------
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

    return render_template('product.html', single_product=item, key=key)


# ---------------------- CREATE a new product -------------------
def product_create():
    # this will fetch the max ID from product table, to create a new product
    command = """ SELECT MAX(id)
                    FROM product """
    cursor.execute(command)
    next_id = cursor.fetchone()   
    product_id = next_id[0]+1
    # re-assings the ProductForm class from models.py into variable  
    form = ProductForm(request.form)
    #Selects all from category
    command = """ SELECT * FROM category """
    cursor.execute(command)
    categories = cursor.fetchall()
    # checks if the request method == POST and if the form is validated
    if request.method == 'POST' and form.validate():
        brand = form.brand.data
        name = form.name.data
        price = form.price.data
        rating = form.rating.data
        year = form.year.data
        stock = form.stock.data
        image = form.image.data
        category = request.form['category']
        # will insert the new product into the product table
        command = """
            INSERT INTO product 
            (id,brand,name,price,rating,category_id,year,stock,image)
            VALUES 
            ({i},'{b}','{n}',{p},{r},{c},{y},{s},'{img}')
            """.format(i=product_id,b=brand,n=name,p=price,r=rating,c=category,y=year,s=stock,img=image)#place category_id between rating & year when fixed
        cursor.execute(command)
        conn.commit()
        # when form is submitted it will redirect user to the products page
        return redirect(url_for('my_view.products', key=product_id))
    # if there is an error with the form it will flash the message
    if form.errors:
        flash(form.errors, 'Something went wrong! Retry!')
    # this renders the template
    return render_template('product-create.html', form=form, product_id=product_id, categories=categories)

# --------------------- EDIT a product ----------------------------
def product_edit(key):
    # this will fetch all product names for dropdown menu
    command = """ SELECT id,name
                  FROM product """
    cursor.execute(command)
    product_name = cursor.fetchall()
    # Reassings the ProductForm class from 'models.py' into variable
    form = ProductForm(request.form)
    # this will fetch all categories for dropdown menu
    command = """ SELECT *
                  FROM category """
    cursor.execute(command)
    categories = cursor.fetchall()
    # checks if the request method == POST and if the form is validated
    if request.method == 'POST' and form.validate():
        brand = form.brand.data
        name = request.form['name']
        price = form.price.data
        rating = form.rating.data
        year = form.year.data
        stock = form.stock.data
        image = form.image.data
        category = request.form['category']
        # will update the product chosen inside of the product table
        command = """
            UPDATE product SET brand='{b}', 'name={n}' price={p}, rating={r}, category_id={c}, year={y}, stock={s}, image='{img}'
            WHERE  id = {i}
            """.format(b=brand, n=name, p=price, r=rating, y=year, s=stock, img=image, i=key)
        cursor.execute(command)                                                              
        conn.commit()
        # will redirect user to the edited product
        return redirect(url_for('my_view.products', key=key))
    # if there is an error with the form it will flash the message
    if form.errors:
        flash(form.errors, 'danger')
    # this renders the template
    return render_template('product-edit.html', form=form, categories=categories, product_name=product_name, category_id=key)


# ----------------------- Product Delete -----------------
def product_delete():
    #selects all product names, id from product table
    command = """ SELECT id, name
                  FROM product """
    cursor.execute(command)
    products = cursor.fetchall()
    
    #deletes product selected from product table
    if request.method == 'POST':
        #Command to delete goes here
        product_id = request.form['product']
        command = """ DELETE FROM product
                    WHERE product.id = {p1}
                  """.format(p1=product_id)
        cursor.execute(command)
        conn.commit()
        return redirect(url_for('my_view.products'))
    
    return render_template('product-delete.html', products=products )


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