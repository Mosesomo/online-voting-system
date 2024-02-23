from flask import render_template, url_for
from system import app
from system.form import LoginForm, RegistrationForm

@app.route('/')
@app.route('/account/')
@app.route('/account/login')
def login_home():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/account/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route('/ballot')
def ballot():
    return render_template('ballot.html')

@app.route('/dashboard/positions')
def positions():
    return render_template('admin/positions.html')


@app.route('/dashboard/candidates')
def candidates():
    return render_template('admin/candidates.html')

@app.route('/dashboard/voters')
def voters():
    return render_template('admin/voters.html')

@app.route('/ballot_positions')
def ballot_positions():
    return render_template('admin/ballot_position.html')

@app.route('/dashboard/votes')
def votes():
    return render_template('admin/votes.html')



@app.route('/dashboard')
def home():
    return render_template('admin/home.html')
