from flask import Flask
import my_app.source.views
from my_app.source.views import my_view
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = 'some_random_key'

app.register_blueprint(my_view)

app.config['DATABASE_FILE'] = 'Centratech.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Kai/Github_Projects/centratech-web/newProject/Centratech.sqlite'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

admin = Admin(app)
class Product(db.Model):
    brand = db.Column(db.String(120))
    name = db.Column(db.String(120))
    price = db.Column(db.Float)
    rating = db.Column(db.Float)
    category_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    image = db.Column(db.String(300))
    id = db.Column(db.Integer, primary_key=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    deptPhone = db.Column(db.Integer)
    deptLine = db.Column(db.Integer)
    deptMang = db.Column(db.String(50))

admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Category, db.session))