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
#Parameters: Key, integer
def category(key):
    command = """ SELECT *
                    FROM category
                    WHERE category.id = {p1}
            """.format(p1=key)
    cursor.execute(command)
    category_name = cursor.fetchall()[0][1]

    command = """SELECT {a}.id, {a}.name, {a}.price, {b}.name, {a}.url
                      FROM {a} join {b} ON {a}.category_id = {b}.id
                      WHERE {a}.category_id = {p1}
        """.format(a="product", b='category', p1=key)
    cursor.execute(command)
    astro_data = cursor.fetchall()  
   
    return render_template('category.html', category_id = key, 
                           category_name=category_name, my_list=astro_data)

# ----------------- Category Edit -----------------
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
        
        command = """
            INSERT INTO category 
            (id,name) VALUES 
            ({i},'{n}')
            """.format(i=category_id, n=name)
        
        cursor.execute(command)
        conn.commit()
        
        flash('The category %s, ID: %d has been created' % (name,category_id), 'success')
        return redirect(url_for('my_view.categories'))
    
    return render_template('category-create.html', form=form, result=result)

# ----------------- Category Edit -----------------
def category_edit(key):
    command = """ SELECT *
                    FROM category
                    WHERE id = {p1}
            """.format(p1=key)    
    cursor.execute(command)
    single_category = cursor.fetchall()[0]        
    
    form = CategoryForm(request.form, csrf_enabled=False, name=single_category[1])
       
    if request.method == 'POST' and form.validate():
        name = form.name.data
        
        command = """
            UPDATE category SET name = '{n}'
            WHERE  id = {i}
            """.format(n=name, i=key)
        cursor.execute(command)
        conn.commit()
        
        flash('The category has been edited to %s' % (name), 'success')
        return redirect(url_for('my_view.category', key=key))
    
    return render_template('category-edit.html', form=form, category_id=key)

# ----------------- Category Edit -----------------
def category_delete(key):
    command = """ SELECT *
                    FROM category
                    WHERE category.id = {p1}
            """.format(p1=key)
    cursor.execute(command)
    single_category = cursor.fetchall()   
    name = single_category[0][1] 
    
    command = """ DELETE FROM category
                    WHERE category.id = {p1}
            """.format(p1=key)
    cursor.execute(command)
    conn.commit()    
    
    flash('The category %s has been deleted' % (name), 'success')
    return redirect(url_for('my_view.home'))