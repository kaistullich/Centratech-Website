from wtforms import Form, TextField, DecimalField, SelectField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from decimal import Decimal

import sqlite3
sqlite_file = 'Centratech.sqlite'

conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor() 

class CategoryForm(Form):
	name = TextField('Category Name', validators=[InputRequired()])
	deptPhone = IntegerField('Department Phone Number', validators=[InputRequired(), NumberRange(min=10)])
	deptLine = IntegerField('Department Extension', validators=[InputRequired(), NumberRange(min=3)])
	deptManager = TextField('Department Manager', validators=[InputRequired()])
	
class ProductForm(Form):
	brand = TextField('Product Brand', validators=[InputRequired()])
	name = TextField('Product Name', validators=[InputRequired()])
	price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
	rating = DecimalField('Product Rating', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
	# CATEGORY WOULD GO HERE
	year = IntegerField('Production Year', validators=[InputRequired(), NumberRange(min=0)])
	stock = IntegerField('Available Stock', validators=[InputRequired(), NumberRange(min=0)])
	image = TextField('Image URL', validators=[InputRequired()])
