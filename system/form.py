from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField, EmailField,
    PasswordField, BooleanField,
    RadioField, DateTimeField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
from system.model import User, Position
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
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField('Phone no.', validators=[DataRequired(), Regexp('^\+?\d+$', message='Invalid phone number')])
    bio = StringField('Biography')
    
    # Dynamically populate choices for the position field from the database
    position = SelectField('Position', coerce=int, validators=[DataRequired()])
    # position = StringField('Position', validators=[DataRequired()],
                           # render_kw={'Chairperson': 'Chairperson'})

    candidate_img = FileField('Img URL', validators=[FileAllowed(photos, 'Only Images are allowed')])
    submit = SubmitField('Add')

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        # Query positions from the database and set choices for the position field
        self.position.choices = [(position.id, position.position_name) for position in Position.query.all()]
    

class AddPosition(FlaskForm):
    position_name = StringField("Position name:", validators=[DataRequired()])
    submit = SubmitField('Add')
    
class EditVotingPeriod(FlaskForm):
    start_time = DateTimeField('Start Time', validators=[DataRequired()],
                               format='%Y-%m-%d %H:%M:%S', render_kw={"placeholder": "YY-MM-DD H:M:S"})
    end_time = DateTimeField('End Time', validators=[DataRequired()],
                             format='%Y-%m-%d %H:%M:%S', render_kw={"placeholder": "YY-MM-DD H:M:S"})
    submit = SubmitField('Update')
    
