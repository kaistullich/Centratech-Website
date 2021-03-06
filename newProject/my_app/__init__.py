import os
from flask import Flask
import my_app.source.views
from my_app.source.views import my_view
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from wtforms import fields, widgets
import flask_restless

# Create the app
app = Flask(__name__)
# Creates random generated key, so we can use session
app.secret_key = os.urandom(24)
# Register all the routes as my_view insead of app.route
app.register_blueprint(my_view)

# Configure the name of the DB
app.config['DATABASE_FILE'] = 'Centratech.sqlite'
# Show full path to where DB is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Kai/Github_Projects/centratech-web/newProject/Centratech.sqlite'
# SQAlchemy Debug Purpose   
app.config['SQLALCHEMY_ECHO'] = True
# Supress warning when running app (SQLAlchemy uses significant overhead)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Pass Flask App into SQLAlchemy
db = SQLAlchemy(app)
# Creating the admin navabar with Boostrap
admin = Admin(app, template_mode='bootstrap3')

# Create the WYSIWYG editor 
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()
# Create models (the Product 'page' in Admin view)
class Product(db.Model):
    brand = db.Column(db.String(120))
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)
    category_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    image = db.Column(db.String(300))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.UnicodeText())

# Create models (the Category 'page' in Admin view)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    deptPhone = db.Column(db.Integer)
    deptLine = db.Column(db.Integer)
    deptMang = db.Column(db.String(50))

# Create class to be able to use the WYSIWYG editor
class ProductEdit(ModelView):
    form_overrides = dict(description=CKTextAreaField)
    create_template = 'create.html'
    edit_template = 'edit.html'
    # Formats the description columns since it will be very long
    def _description_formatter(view, context, model, name):
        # If the description column is empty it will place an empty string for formatting purposes
        if model.description is None:
            return ""
        # If description column is not empty, it will only show up to 19 characters
        return model.description[:20]
        
    column_formatters = {
        'description': _description_formatter,
    }     
# Add views
admin.add_view(ProductEdit(Product, db.session))
admin.add_view(ModelView(Category, db.session))

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by default
manager.create_api(Product,
                    methods=['GET', 'POST'],
                    url_prefix='/api/v1/json', # product API now at /api/v1/json/product
                    results_per_page= -1, # < 0 to disable pagination
                    max_results_per_page= -1 # < 0 to disable pagination
                    )
manager.create_api(Category,
                    methods=['GET', 'POST'],
                    url_prefix='/api/v2/json',# category API now at /api/v2/json/category
                    results_per_page= -1, # < 0 to disable pagination
                    max_results_per_page= -1 # < 0 to disable pagination
                    )