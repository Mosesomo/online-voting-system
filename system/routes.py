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