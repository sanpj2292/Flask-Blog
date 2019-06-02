from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import User, Post

# Initialization of the Flask Class similar to the one used in ExpressJs(NodeJs)
app = Flask(__name__)

# Configuration of Secret Key will protect the site from modifying cookies
# CrossSite Forgery Attacks
app.config['SECRET_KEY'] = '4d5521851675d51736e0b3a05ad9c5f2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


posts = [
    {
        'author': 'San PJ',
        'title': 'My Title',
        'date_posted': '31st May, 2019',
        'content': 'The first content I wrote'
    },
    {
        'author': 'John Doe',
        'title': 'His Title',
        'date_posted': '25th March, 2019',
        'content': 'The first content I wrote'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    print(form.username.errors)
    if form.validate_on_submit():
        flash('User Successfully create: {user}'.format(user=form.username.data), 'success')
        return redirect(url_for('home'))     
    return render_template('register.html',title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data=='admin@blog.com' and form.password.data=='password':
            flash('You have been Logged In!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, please check Username/Password', 'danger')
    return render_template('login.html',title='Login', form=form)

# To run the server using python command rather than flask command
if __name__ == '__main__':
    # Debug True is set to make sure whenever there is change
    # then we don't need of stopping and restarting the server
    app.run(debug=True)