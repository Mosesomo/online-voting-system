from flask import render_template, url_for
from itertools import groupby
from system import app
from system.form import LoginForm, RegistrationForm
from system.model import User, Candidate, BallotPosition, Position
from collections import defaultdict

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
