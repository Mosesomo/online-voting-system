from flask import render_template, url_for, redirect, flash
from itertools import groupby
from system import app, bcrypt, db
from system.form import LoginForm, RegistrationForm
from system.model import User, Candidate, BallotPosition, Position
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/account/', methods=['GET', 'POST'])
@app.route('/account/login', methods=['GET', 'POST'])
def login_home():
    if current_user.is_authenticated:
        return redirect(url_for('ballot'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            return redirect(url_for('ballot'))
        else:
            flash('Login Unsuccessfull, please check email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/account/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ballot'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = (bcrypt.generate_password_hash
                           (form.password.data)
                           .decode('utf-8'))
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully', 'success')
        return redirect(url_for('login_home'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_home'))

@app.route('/ballot')
def ballot():
    # Query candidates grouped by position
    grouped_candidates = {}
    positions = Position.query.all()

    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates

    return render_template('ballot.html', grouped_candidates=grouped_candidates)

@app.route('/dashboard/positions')
def positions():
    positions = Position.query.all()
    return render_template('admin/positions.html', positions=positions)


@app.route('/dashboard/candidates')
def candidates():
    candidates = Candidate.query.all()
    return render_template('admin/candidates.html', candidates=candidates)

@app.route('/dashboard/voters')
def voters():
    voters = User.query.all()
    return render_template('admin/voters.html', voters=voters)

@app.route('/ballot_positions')
def ballot_positions():
    grouped_candidates = {}
    positions = Position.query.all()

    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates
    

    return render_template('admin/ballot_position.html',
                           grouped_candidates=grouped_candidates)

@app.route('/dashboard/votes')
def votes():
    return render_template('admin/votes.html')


@app.route('/dashboard')
def home():
    positions = Position.query.all()
    candidates = Candidate.query.all()
    voters = User.query.all()
    count_candidates = len(candidates)
    count_voters = len(voters)
    count_position = len(positions)
    return render_template('admin/home.html',
                           count_position=count_position,
                           count_voters=count_voters,
                           count_candidates=count_candidates)
