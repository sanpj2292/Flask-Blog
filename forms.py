# WT Form is an extension
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired

# Here classes are defined which will be converted to HTML

# Register Form class - Loads with html tags some-styling needs to be done
class RegistrationForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired(), InputRequired(),
            Length(min=2,max=50)])
    email=StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), InputRequired(),])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), InputRequired(),
            EqualTo('password')])
    submit = SubmitField('Sign Up')

# Login Form class - Loads with html tags some-styling needs to be done
class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), InputRequired(),])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')