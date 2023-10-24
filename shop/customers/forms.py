from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, BooleanField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from flask_wtf import FlaskForm
from .model import Register



class CustomerRegisterForm(FlaskForm ):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    phone = StringField('Phone: ', [validators.DataRequired(), validators.Length(min=10, max=10), validators.Regexp('^\d+$', message='Phone number must contain exactly 10 digits!')])
    password = PasswordField('Password ', [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match!')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    
    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already in use')
    
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already in use')
        
    submit = SubmitField('Register')
    
        
class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password ', [validators.DataRequired()])
    
    submit = SubmitField("Login")
