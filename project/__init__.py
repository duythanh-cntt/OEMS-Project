__version__ = '1.0'

from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config.from_pyfile('config.cfg')
app.secret_key = 'blogful-secretkey'
app.debug = True
db = SQLAlchemy(app)

from project.controllers import *
from project.models import *


# 401 Unauthorized
@app.errorhandler(401)
def page_not_found(e):
    return redirect('/login/')


# 404 Not Found
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404