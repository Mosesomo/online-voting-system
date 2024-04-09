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
    reg_no = StringField('Reg No.',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                           validators=[DataRequired()])
    submit = SubmitField('login')


# List of department codes
departments = ['bscit', 'bbit', 'bbam', 'bird', 'staff', 'admin', 'dit', 'dbit']

# Create the regex pattern
department_pattern = '|'.join(departments)

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    reg_no = StringField('Reg No.', validators=[DataRequired(),
                                                Regexp(rf'^{department_pattern}-[0-9]{2}-[0-9]{4}/[0-9]{4}$',
                                                       message='Invalid Registration Number')],
                         render_kw={"placeholder": "bscit-00-000/year", "style": "color: gray;font-weight: 400;"})
    student_id = FileField('Upload your Id', validators=[FileAllowed(photos, 'Only Images are allowed')])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)],
                             render_kw={"Password": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists!')
        
    def validate_reg_no(self, reg_no_field):
        reg_no = User.query.filter_by(reg_no=reg_no_field.data).first()
        if reg_no:
            raise ValidationError('Reg No. already exists!')
        
    def validate_password(self, password_field):
        password = password_field.data
        # Check if password contains at least one uppercase letter, one lowercase letter, and one digit
        if (not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
            or not any(c.isdigit() for c in password)):
            raise ValidationError('Password must contain at least one uppercase letter,\
                one lowercase letter, and one digit.')

class BallotForm(FlaskForm):
    submit_vote = SubmitField('Vote')


class CandidateForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField('Phone no.', validators=[DataRequired(),
                                                 Regexp(r'^\+?\d+$', message='Invalid phone number')])
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
    
