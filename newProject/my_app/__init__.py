from flask import Flask
import my_app.source.views
from my_app.source.views import my_view
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from wtforms import fields, widgets

app = Flask(__name__)
app.secret_key = 'some_random_key'

app.register_blueprint(my_view)

app.config['DATABASE_FILE'] = 'Centratech.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Kai/Github_Projects/centratech-web/newProject/Centratech.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

admin = Admin(app, template_mode='bootstrap3')

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()

class Product(db.Model):
    form_widget_args = {
        'description': {
            'rows': 10,
            'class': 'input-xlarge'
        }
    }
    brand = db.Column(db.String(120))
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)
    category_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    image = db.Column(db.String(300))
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.UnicodeText())
        

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    deptPhone = db.Column(db.Integer)
    deptLine = db.Column(db.Integer)
    deptMang = db.Column(db.String(50))

class ProductEdit(ModelView):
    form_overrides = dict(description=CKTextAreaField)
    create_template = 'create.html'
    edit_template = 'edit.html'

admin.add_view(ProductEdit(Product, db.session))
admin.add_view(ModelView(Category, db.session))