from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
import json


def insert_data():
    with open(os.path.join('flaskblog/data.json'),'r') as json_f:
        posts = json.load(json_f)
        for post in posts:
            author = User.query.get(post['user_id'])
            p = Post(title=post['title'],content=post['content'],author=author)
            db.session.add(p)
        db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    # insert_data()
    posts = Post.query.order_by(Post.date_poster.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, active_page=page)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created: {user}'.format(user=form.username.data), 'success')
        return redirect(url_for('login'))     
    return render_template('register.html',title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('home')) if not next_page else redirect(url_for(next_page[1:]))
        else:
            flash('Login Unsuccessful, please check Username/Password', 'danger')
    return render_template('login.html',title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_pic):
    rand_hex = secrets.token_hex(8)
    _, fext = os.path.splitext(form_pic.filename)
    pic_fnm = rand_hex + fext
    pic_path = os.path.join(app.root_path, 'static/profile_pix', pic_fnm)
    out_sz = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(out_sz)
    img.save(pic_path)
    # Deleting the old image
    os.remove(os.path.join(app.root_path, 'static/profile_pix', current_user.image_file))
    return pic_fnm


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Validation & setting the picture-path
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated!', 'info')
        # Due to post-get-redirect pattern
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file=url_for('static',filename='profile_pix/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file, 
                            form=form)

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
             form=form, legend='Create Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author !=  current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # since only an update on existing data is being done
        # The line db.session.add(post) -> can be ignored!!
        db.session.commit()
        flash('Post has been updated!', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',
                form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your message has been deleted!!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def posts_by_user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_poster.desc())\
        .paginate(page=page,per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, active_page=page)