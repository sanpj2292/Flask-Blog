# Initialization of Flask Blog Application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# For management of loginsession(s)
from flask_login import LoginManager

# Initialization of the Flask Class similar to the one used in ExpressJs(NodeJs)
app = Flask(__name__)

# Configuration of Secret Key will protect the site from modifying cookies
# CrossSite Forgery Attacks
app.config['SECRET_KEY'] = '4d5521851675d51736e0b3a05ad9c5f2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# The login is the function-name of the route not the view-name
login_manager.login_view = 'login'

db = SQLAlchemy(app)