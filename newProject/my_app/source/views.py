from __future__ import print_function
from flask import Flask, flash, redirect, render_template, request, session, abort, Blueprint, url_for, flash
import my_app.source.views_products as product_view
import my_app.source.views_categories as category_view
from my_app.source.models import cursor, conn

my_view = Blueprint('my_view' , __name__)

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

@my_view.route('/product_edit/<key>', methods=['GET', 'POST'])
def product_edit(key):
	return (product_view.product_edit(key))

# ========================================================
# ----------------- DELETE A PRODUCT ---------------------
# ========================================================

@my_view.route('/product_delete', methods=['GET', 'POST'])
def product_delete():
	return (product_view.product_delete())

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
    return (category_view.category_create())

# ========================================================
# ----------------- EDIT A CATEGORY ----------------------
# ========================================================

@my_view.route('/category_edit/<key>', methods=['GET', 'POST'] )
def category_edit(key):
    return (category_view.category_edit(key))

# ========================================================
# ----------------- DELETE A CATEGORY --------------------
# ========================================================

@my_view.route('/category_delete', methods=['GET', 'POST'] )
def category_delete():
    return (category_view.category_delete())

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
            flash('Username or Password is incorrect! Please try again')
        else:
            return redirect(url_for('admin.index'))
    return render_template('login.html', error=error)

# ========================================================
# ----------------- NAVBAR DROPDOWN SEARCH BOX -----------
# ========================================================
def dropdown_search():
	command = """ SELECT name
				  FROM category"""
	cursor.execute(command)
	dropdown_category = cursor.fetchall()

	return (dropdown_category)

#==============================================================
#================TERMS AND CONDITIONS PAGE=====================
#==============================================================

@my_view.route('/terms')
def terms():
    return render_template('terms.html')

#==============================================================
#=====================PRIVACY PAGE=============================
#==============================================================

@my_view.route('/privacy')
def privacy():
    return render_template('privacy.html')

#==============================================================
#==================== SHIPPING ================================
#==============================================================

@my_view.route('/shipping')
def shipping():
    return render_template('shipping.html')

# ========================================================
# ----------------- ABOUT US -----------------------------
# ========================================================

@my_view.route('/about_us')
def about_us():
    return render_template('about-us.html')

# ========================================================
# ----------------- CONTACT US ---------------------------
# ========================================================

@my_view.route('/contact')
def contact():
    return (category_view.contact_us())

# ========================================================
# ----------------- RETURNS ------------------------------
# ========================================================

@my_view.route('/returns')
def returns():
    return render_template('returns.html')

# ========================================================
# ----------------- SHOPPING CART ------------------------
# ========================================================

# Links to cart 
@my_view.route('/cart/')
def cart():
    # Verifies if the cart is empty or not
    if 'cart_data' in session and 'quantityList' in session:
        # Grabbing the cart data from the session (its a list)
        cart_data = session['cart_data']
        # Grabbing quantityList from the session (its a list)
        quantityList = session['quantityList']
        # renders cart template, and passes in cart_data & quantityList as parameter
        return render_template('cart.html', cart_data=cart_data, quantityList=quantityList)
    # If cart is empty it will render this template
    return render_template('empty_cart.html')

# Checks to see if product ID is in session list 
def findItemInCart(items, key):
    for item in items:
        if item['id'] == key:
            return item
    # if item isnt found, returns nothing
    return None

# Passes product ID into add-to-cart
@my_view.route('/add-to-cart/<key>', methods=['POST'])
def addToCart(key):

    if 'cart-items' in session:
        items = session['cart-items']
        item = findItemInCart(items, key)
        if item is not None:
            item['quantity'] = item['quantity'] + 1
        else:
            items.append({'id':key, 'quantity':1})
        
        session['cart-items'] = items
        return product_view.addToCart(session['cart-items'])
    else:
        items = []
        items.append({'id':key, 'quantity':1})
        session['cart-items'] = items
        return product_view.addToCart(session['cart-items'])

# ========================================================
# ----------------- DROP SESSION  ------------------------
# ========================================================
@my_view.route('/drop-session', methods=['POST'])
def dropSession():
    session.pop('cart-items', None)
    session.pop('quantityList', None)
    return redirect(url_for('my_view.cart'))