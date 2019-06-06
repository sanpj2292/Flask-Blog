# WT Form is an extension
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from flaskblog.models import User
from flask_login import current_user

# Here classes are defined which will be converted to HTML

# Register Form class - Loads with html tags some-styling needs to be done
class RegistrationForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), InputRequired(), Length(min=2,max=50)])
    email=StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    #  Custom Validation for Username
    def validate_username(self, username):
        # username is a wtforms object
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'User {username.data}: Already Taken. Choose Another one')
    
    #  Custom Validation for Email
    def validate_email(self, email):
        # email is a wtforms object
        emailId = User.query.filter_by(email=email.data).first()
        if emailId:
            raise ValidationError(f'Email {email.data}: Already Taken. Choose Another one')


# Login Form class - Loads with html tags some-styling needs to be done
class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), InputRequired(),])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), InputRequired(), Length(min=2,max=50)])
    email=StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    picture = FileField('Update Profile Pic.', validators=[FileAllowed(['jpeg','png','jpg'])])
    submit = SubmitField('Update')
    
    #  Custom Validation for Username
    def validate_username(self, username):
        if username.data != current_user.username:
            # username is a wtforms object
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(f'User {username.data}: Already Taken. Choose Another one')
    
    #  Custom Validation for Email
    def validate_email(self, email):
        if current_user.email != email.data:
            # email is a wtforms object
            emailId = User.query.filter_by(email=email.data).first()
            if emailId:
                raise ValidationError(f'Email {email.data}: Already Taken. Choose Another one')