import secrets, os
from PIL import Image
from church_web.models import User, Post
from flask import Flask, render_template, flash, redirect, abort
from church_web.forms import RegisterationForm, LoginForm, UpdateAccountForm, PostForm
from church_web import app, db, bcrypt
from flask import url_for, request
from flask_login import login_user,current_user, logout_user, login_required

@app.route("/") # root page or home page.
@app.route("/home") # also need thie route.

def home():
    page = request.args.get('page',1,type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', posts=post)


@app.route("/about") # About page.

def about():
    return render_template('about.html',title='about')

@app.route("/register",methods=['GET', 'POST'])

def register():
    
    if current_user.is_authenticated:
        return redireect(url_for('home'))
    
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_psw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please login','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET', 'POST'])

def login():
    
    if current_user.is_authenticated:
        return redireect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged In to {user.username}!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Failed to login. please retry again', 'danger')
    return render_template('login.html',title='Login',form=form)


@app.route("/logout")

def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, extention = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + extention
    picture_path = os.path.join(app.root_path, 'static/', picture_fn)
    
    # resizing the image
    output_size = (125,125)
    images = Image.open(form_picture)
    images.thumbnail(output_size)
    images.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
           picture_file =  save_picture(form.picture.data)           
           current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET' :
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='./' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been Updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_post(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_post.html', posts=post, user=user)





















