from flask import render_template, request, redirect, url_for, flash
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

    command = """SELECT {a}.id, {a}.brand, {a}.name, {a}.price, {b}.name, {a}.image
                      FROM {a} join {b} ON {a}.category_id = {b}.id
                      WHERE {a}.category_id = {p1}
        """.format(a="product", b='category', p1=key)
    cursor.execute(command)
    product_data = cursor.fetchall()  
   
    return render_template('category.html', category_id=key, category_name=category_name, 
                            my_list=product_data)



# ------------------ Contact Us Phone Numbers -------------------
def contact_us():
    command = """ SELECT name, deptPhone, deptLine, deptMang
                  FROM category """
    cursor.execute(command)
    phone_numbers = cursor.fetchall()

    return render_template('contact.html', categories=phone_numbers)

# ----------------------------------------------------------------
    