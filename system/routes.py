from flask import redirect, render_template, url_for, flash
from system import app, login_manager, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from system.form import LoginForm, RegistrationForm
from system.model import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/account/')
@app.route('/account/login')
def login_home():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/account/register' ,methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = (bcrypt.generate_password_hash
                           (form.password.data)
                           .decode('utf-8'))
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
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
