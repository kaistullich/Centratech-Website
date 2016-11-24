from flask import Blueprint
from flask import render_template

my_view = Blueprint('my_view', __name__)

import my_app.source.views_product as pd
import my_app.source.views_category as ct

#-------------------- Home Page Handler --------------------
@my_view.route('/')
@my_view.route('/home')
def home():
    return render_template('home.html')

#-------------------- Product Handler --------------------
@my_view.route('/products')
def products():   
    return (pd.products())    

#-------------------- Product Key Handler --------------------
@my_view.route('/product/<key>')
def product(key):    
    return (pd.product(key))

# ----------------- Product Create -----------------
@my_view.route('/product_create', methods=['GET', 'POST'])
def product_create():
    return (pd.product_create())

# ----------------- Product Edit -----------------
@my_view.route('/product_edit/<key>', methods=['GET', 'POST'])
def product_edit(key):
    return (pd.product_edit(key))

# ----------------- Product Delete -----------------
@my_view.route('/product_delete/<key>', methods=['GET', 'POST'])
def product_delete(key):
    return (pd.product_delete(key))

# ----------------- Search -----------------
@my_view.route('/product_search')
def product_search():
    return (pd.product_search())

#-------------------- Category Handler --------------------
@my_view.route('/categories')
def categories():   
    return (ct.categories())

#-------------------- Category Key Handler --------------------
#Parameters: Key, integer
@my_view.route('/category/<key>')
def category(key):
    return (ct.category(key))

# ----------------- Category Create -----------------
@my_view.route('/category_create', methods=['GET', 'POST'] )
def category_create():
    return (ct.category_create())

# ----------------- Category Edit -----------------
@my_view.route('/category_edit/<key>', methods=['GET', 'POST'] )
def category_edit(key):
    return (ct.category_edit(key))

# ----------------- Category Delete -----------------
@my_view.route('/category_delete/<key>', methods=['GET', 'POST'] )
def category_delete(key):
    return (ct.category_delete(key))


