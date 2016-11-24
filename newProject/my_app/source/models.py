from wtforms import Form, TextField, DecimalField, SelectField
from wtforms.validators import InputRequired, NumberRange
from decimal import Decimal

import sqlite3
sqlite_file = 'Centratech.sqlite'

conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor() 

class CategoryForm(Form):
    name = TextField(
            label='Category Name',
            validators=[InputRequired()])  
      
class ProductForm(Form):
    name = TextField(
            label='Product Name',
            validators=[InputRequired()])  
    price = DecimalField(
            label='Price', 
            validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    category = SelectField(
            label='Category', 
            validators=[InputRequired()], coerce=int)
    url = TextField(
            label='Image URL',
            validators=[InputRequired()]) 