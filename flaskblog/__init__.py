# Initialization of Flask Blog Application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialization of the Flask Class similar to the one used in ExpressJs(NodeJs)
app = Flask(__name__)

# Configuration of Secret Key will protect the site from modifying cookies
# CrossSite Forgery Attacks
app.config['SECRET_KEY'] = '4d5521851675d51736e0b3a05ad9c5f2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)