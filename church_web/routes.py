from church_web.models import User, Post
from flask import Flask, render_template, flash, redirect
from church_web.forms import RegisterationForm, LoginForm
from church_web import app, db, bcrypt
from flask import url_for, request
from flask_login import login_user,current_user, logout_user, login_required

post = [
        {
            'author': 'Jerrin Joe Varghese',
            'title': 'Convolutional neural network or Logistic regression',
            'content': 'Pending',
            'date_posted' : 'April 7 2019'
        }
        ]

@app.route("/") # root page or home page.
@app.route("/home") # also need thie route.

def home():
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

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
































