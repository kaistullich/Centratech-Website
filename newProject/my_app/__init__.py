from flask import Flask

app = Flask(__name__)
app.secret_key = 'some_random_key'

import my_app.source.views

from my_app.source.views import my_view
app.register_blueprint(my_view)