from flask import render_template, url_for, redirect, flash, request
from itertools import groupby
from wtforms import RadioField
from wtforms.validators import DataRequired
from system import app, bcrypt, db
from system.form import LoginForm, RegistrationForm, BallotForm
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

@app.route('/ballot', methods=['GET', 'POST'])
@login_required
def ballot():
    # Check if the user has already voted
    existing_votes = BallotPosition.query.filter_by(user_id=current_user.id).all()
    if existing_votes:
        flash('You have already voted')
        return redirect(url_for('ballot_positions')) # or redirect to a different page
    # Query candidates grouped by position
    grouped_candidates = {}
    positions = Position.query.all()

    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates
    
    form = BallotForm()
    if form.validate_on_submit():
        # Extract selected candidate IDs for each position
        for position, candidates in grouped_candidates.items():
            selected_candidate_id = request.form.get(f'position_{position.id}')
            if selected_candidate_id:
                # Create a new BallotPosition instance for the selected candidate
                ballot_position = BallotPosition(
                    user_id=current_user.id,
                    position_id=position.id,
                    candidate_id=selected_candidate_id
                )
                db.session.add(ballot_position)
        db.session.commit()
        flash('Vote submitted successfully', 'success')
        return redirect(url_for('ballot_positions')) # or redirect to a confirmation page
    return render_template('ballot.html',
                           grouped_candidates=grouped_candidates,
                           form=form)

@app.route('/dashboard/positions')
@login_required
def positions():
    positions = Position.query.all()
    return render_template('admin/positions.html', positions=positions)

@app.route('/dashboard/candidates')
@login_required
def candidates():
    candidates = Candidate.query.all()
    return render_template('admin/candidates.html', candidates=candidates)

@app.route('/dashboard/voters')
@login_required
def voters():
    voters = User.query.all()
    return render_template('admin/voters.html', voters=voters)

@app.route('/ballot_positions')
@login_required
def ballot_positions():
    grouped_candidates = {}
    positions = Position.query.all()

    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates
    

    return render_template('admin/ballot_position.html',
                           grouped_candidates=grouped_candidates)

@app.route('/dashboard/votes')
@login_required
def votes():
    return render_template('admin/votes.html')


@app.route('/dashboard')
@login_required
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
