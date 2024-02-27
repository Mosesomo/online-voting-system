from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, EmailField,  PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from system.model import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                           validators=[DataRequired()])
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name',
                         validators=[DataRequired()])
    last_name = StringField('Last name',
                         validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists!')

class BallotForm(FlaskForm):
    position_1 = RadioField('Position 1', choices=[], validators=[DataRequired()])
    position_2 = RadioField('Position 2', choices=[], validators=[DataRequired()])
    position_3 = RadioField('Position 3', choices=[], validators=[DataRequired()])
    position_4 = RadioField('Position 4', choices=[], validators=[DataRequired()])
    submit_vote = SubmitField('Vote')
