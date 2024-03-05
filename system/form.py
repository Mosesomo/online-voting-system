from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField, EmailField,
    PasswordField, BooleanField,
    RadioField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
from system.model import User
from system import photos


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
    submit_vote = SubmitField('Vote')
    

class CandidateForm(FlaskForm):
    first_name = StringField('First name',
                         validators=[DataRequired()])
    last_name = StringField('Last name',
                         validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired()])
    phone = StringField('Phone no.', validators=[DataRequired(), Regexp('^\+?\d+$', message='Invalid phone number')])
    bio = StringField('Biography')
    position = SelectField('Position', choices=[
        ('President', 'President'),
        ('Academic sec', 'Academic sec'),
        ('Accounts', 'Accounts'),
        ('Games and sports', 'Games and sports')
    ], validators=[DataRequired()])
    candidate_img = FileField('Img URL',
                              validators=[FileAllowed(photos, 'Only Images are allowed')]
                              )
    submit = SubmitField('Add')
    
    
class AddPosition(FlaskForm):
    position_name = StringField("Position name:", validators=[DataRequired()])
    submit = SubmitField('Add')
    
