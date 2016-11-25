from flask import Blueprint, render_template, request, redirect, url_for

my_view = Blueprint('my_view' , __name__)

import my_app.source.views_products as product_view
import my_app.source.views_categories as category_view

# ========================================================
# ----------------- HOME PAGE LAYOUT ---------------------
# ========================================================

@my_view.route('/')
@my_view.route('/home')
def home():
    return render_template('home.html')

# ========================================================
# ----------------- SHOW ALL PRODUCTS --------------------
# ========================================================

@my_view.route('/products')
def products():
    return (product_view.products())

# ========================================================
# ----------------- SHOW ONE PRODUCT ---------------------
# ========================================================

@my_view.route('/product/<key>')
def product(key):
	return (product_view.product(key))

# ========================================================
# ----------------- CREATE A PRODUCT ---------------------
# ========================================================

@my_view.route('/product_create', methods=['GET', 'POST'])
def product_create():
	return (product_view.product_create())

# ========================================================
# ----------------- EDIT A PRODUCT -----------------------
# ========================================================

@my_view.route('/product_edit<key>', methods=['GET', 'POST'])
def product_edit(key):
	return None

# ========================================================
# ----------------- DELETE A PRODUCT ---------------------
# ========================================================

@my_view.route('/product_delete/<key>', methods=['GET', 'POST'])
def product_delete(key):
	return None

# ========================================================
# ----------------- SHOW ALL CATEGORIES-------------------
# ========================================================

@my_view.route('/categories')
def categories():
	return (category_view.categories())

# ========================================================
# ----------------- SHOW ONE CATEGORY --------------------
# ========================================================

@my_view.route('/category/<key>')
def category(key):
    return (category_view.category(key))

# ========================================================
# ----------------- CREATE A CATEGORY --------------------
# ========================================================

@my_view.route('/category_create', methods=['GET', 'POST'] )
def category_create():
    return None

# ========================================================
# ----------------- EDIT A CATEGORY ----------------------
# ========================================================

@my_view.route('/category_edit/<key>', methods=['GET', 'POST'] )
def category_edit(key):
    return None

# ========================================================
# ----------------- DELETE A CATEGORY --------------------
# ========================================================

@my_view.route('/category_delete/<key>', methods=['GET', 'POST'] )
def category_delete(key):
    return None

# ========================================================
# ----------------- SEARCH FUNCTION ----------------------
# ========================================================

@my_view.route('/search')
def product_search():
	return (product_view.product_search())

# ========================================================
# ----------------- USER LOGIN PAGE ----------------------
# ========================================================

@my_view.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Username or Password is incorrect. Please try again'
		else:
			return redirect(url_for('@my_view.home'))
	return render_template('login.html', error=error)