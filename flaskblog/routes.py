from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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