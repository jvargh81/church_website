from flask import Flask, render_template, flash, redirect
# finds exact location of our routes.
from flask import url_for
from forms import RegisterationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9798d59e0ca53f5e76215b5905718d5b'
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
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)


@app.route("/login",methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data== 'password':
            flash(f'Logged In to {form.email.data}!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Failed to login. please retry again', 'danger')
    return render_template('login.html',title='Login',form=form)


if __name__ == '__main__':
    app.run(debug=True)

































