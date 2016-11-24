from flask import render_template, request, redirect, url_for, flash
from my_app.source.models import ProductForm
from my_app.source.models import cursor, conn

#-------------------- Product Handler --------------------
def products():   
    command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name
                      FROM {a} join {b} ON {a}.category_id = {b}.id
        """.format(a="product", b='category')
    cursor.execute(command)
    astro_data = cursor.fetchall()  


    return render_template('products.html', my_list=astro_data)
    

#-------------------- Product Key Handler --------------------
#Parameters: Key, integer
def product(key):    
    command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.url
                      FROM {a} join {b} ON {a}.category_id = {b}.id
                      WHERE {a}.id = {p1}
        """.format(a="product", b='category', p1=key)
    cursor.execute(command)
    astro_data = cursor.fetchall()  
      
    if len(astro_data) == 0:
        return "The key "+ key + " was not found" 
    item = astro_data[0]    

    return render_template('product.html', single_product=item)


# Product Create -----------------
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
        
        command = """
            INSERT INTO product 
            (id,name,price,category_id,url) VALUES 
            ({i},'{n}',{p},{c},'{u}')
            """.format(i=product_id, n=name, p=price, c=category, u=url)
        
        cursor.execute(command)
        conn.commit()
        
        flash('The product %s, with id %d has been created with the price %2.2f' % (name, product_id, price), 'success')
        return redirect(url_for('my_view.product', key=product_id))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('product-create.html', form=form, product_id=product_id)

# 2) Product Edit -----------------
def product_edit(key):
    command = """ SELECT *
                    FROM product
                    WHERE id = {p1}
            """.format(p1=key)    
    cursor.execute(command)
    single_product = cursor.fetchall()[0]

    
    form = ProductForm(request.form, csrf_enabled=False, name=single_product[1], price = single_product[2], 
                       url = single_product[4], category = single_product[3])

    command = """ SELECT *
                    FROM category
            """
    cursor.execute(command)
    categories = cursor.fetchall()

    form.category.choices = categories

    if request.method == 'POST' and form.validate():
        name = form.name.data
        price = form.price.data
        category = form.category.data
        
        command = """
            UPDATE product SET name = '{n}', price = '{p}', category_id = '{c}'
            WHERE  id = {i}
            """.format(n=name, i=key, p=price, c=category)
        cursor.execute(command)
        conn.commit()
        
        flash('The product %s has been edited with the price %2.2f' % (name, price), 'success')
        return redirect(url_for('my_view.product', key=key))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('product-edit.html', form=form, product_id = key)

# 3) Product Delete -----------------
def product_delete(key):
    command = """ SELECT *
                    FROM product
                    WHERE product.id = {p1}
            """.format(p1=key)
    cursor.execute(command)
    single_category = cursor.fetchall()   
    name = single_category[0][1] 
    
    command = """ DELETE FROM product
                    WHERE product.id = {p1}
            """.format(p1=key)
    cursor.execute(command) 
    conn.commit()   
    
    flash('The product %s has been deleted' % (name), 'success')
    return redirect(url_for('my_view.home'))

# ----------------- Search -----------------
def product_search():
    name = request.args.get('name')
    price = request.args.get('price')
    category = request.args.get('category')
    price_greater_equal = request.args.get('price_ge')
    price_smaller_equal = request.args.get('price_se')
    
    condition = ""
    if name != None:
        condition += "product.name LIKE '%"+name+"%'"
    if price != None:
        if condition !="":
            condition += " AND "
        condition += "product.price = "+str(price)
    if category != None:
        if condition != "":
            condition += " AND "
        condition  += "category.name LIKE '%" + category +"%'"
    if price_greater_equal != None:
        if condition != "":
            condition += " AND "
        condition  += "product.price >= " + str(price_greater_equal)
    if price_smaller_equal != None:
        if condition != "":
            condition += " AND "
        condition  += "product.price <= " + str(price_smaller_equal)            
           
    if condition == "":
        command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.url
                          FROM {a} join {b} ON {a}.category_id = {b}.id
            """.format(a="product", b='category')        
    else:
        command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.url
                          FROM {a} join {b} ON {a}.category_id = {b}.id
                          WHERE {cond}
            """.format(a="product", b='category', cond = condition)
       
    cursor.execute(command)
    astro_data = cursor.fetchall()      
    return render_template('products.html', my_list=astro_data)
