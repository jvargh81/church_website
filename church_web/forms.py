from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # email helps to validate the email address.
from church_web.models import User
from flask_login import current_user

class RegisterationForm(FlaskForm):
    
    username = StringField('Username',validators=[DataRequired(),
                                                  Length(min=2,max=20)])
    
    email = StringField('Email',validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password', 
                                        validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Sign Up')

    # this will be call each time.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken.')


class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign Up')

class UpdateAccountForm(FlaskForm):

    username = StringField('Username',validators=[DataRequired(),
                                                  Length(min=2,max=20)])

    email = StringField('Email',validators=[DataRequired(), Email()])

    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    # this will be call each time.
    def validate_username(self, username):

        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken.')

    def validate_email(self, email):
        
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already taken.')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')






























