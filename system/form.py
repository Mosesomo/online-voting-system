from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, EmailField,  PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    email = StringField('email',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                           validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    first_name = StringField('first name',
                         validators=[DataRequired()])
    last_name = StringField('last name',
                         validators=[DataRequired()])
    email = EmailField('email',
                       validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('register')
