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