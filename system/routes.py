import os
from flask import render_template, url_for, redirect, flash, request, send_from_directory
from itertools import groupby
from sqlalchemy.sql import label
from sqlalchemy import func
from system import app, bcrypt, db, photos
from system.form import LoginForm, RegistrationForm, BallotForm, CandidateForm, AddPosition
from system.model import User, Candidate, BallotPosition, Position
from flask_login import login_user, logout_user, current_user, login_required


# This route handles the authenication login
# of voters or admin
@app.route('/', methods=['GET', 'POST'])
@app.route('/account/', methods=['GET', 'POST'])
@app.route('/account/login', methods=['GET', 'POST'])
def login_home():
    if current_user.is_authenticated: # checks if the current user is authenicated
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

# This route handles the registration of voters
# And stored the registered voters in our database
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


# This routes logs out the user from the system
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_home'))


# This route handles voting process
@app.route('/ballot', methods=['GET', 'POST'])
@login_required
def ballot():
    # Check if the user has already voted
    existing_votes = BallotPosition.query.filter_by(user_id=current_user.id).all()
    if existing_votes:
        flash('You have already voted!', 'warning')
        return redirect(url_for('ballot_positions')) # or redirect to a ballot_position page
    
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

# This route queries and list the position from the database
@app.route('/dashboard/positions')
@login_required
def positions():
    positions = Position.query.all() # Quering positions from database
    return render_template('admin/positions.html', positions=positions)

# This route queries and list available candidates
@app.route('/dashboard/candidates')
@login_required
def candidates():
    candidates = Candidate.query.all()
    return render_template('admin/candidates.html', candidates=candidates)


# This route queries and list the voters(users)
@app.route('/dashboard/voters')
@login_required
def voters():
    voters = User.query.all()
    return render_template('admin/voters.html', voters=voters)


# This routes list candidates with their positions
@app.route('/ballot_positions')
@login_required
def ballot_positions():
    grouped_candidates = {} # Empty dictionary
    positions = Position.query.all() # Quering positions

    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all() # Quering candidates
        grouped_candidates[position] = candidates


    return render_template('admin/ballot_position.html',
                           grouped_candidates=grouped_candidates)

# This routes queries and list number of numbers for each candidates
@app.route('/dashboard/votes')
@login_required
def votes():
    grouped_candidates = {}
    positions = Position.query.all()
    
    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates
        
    return render_template('admin/votes.html',
                           grouped_candidates=grouped_candidates)

# This routes contains the dashbord and results
@app.route('/dashboard')
@login_required
def home():
    positions = Position.query.all()
    candidates = Candidate.query.all()
    voters = User.query.all()
    count_candidates = len(candidates)
    count_voters = len(voters)
    count_position = len(positions)
    candidates_with_max_votes, total_votes = get_candidates_with_highest_votes()
    return render_template('admin/home.html',
                           count_position=count_position,
                           count_voters=count_voters,
                           count_candidates=count_candidates,
                           candidates_with_max_votes=candidates_with_max_votes,
                           total_votes=total_votes)


def get_candidates_with_highest_votes():
    # Subquery to calculate the count of votes for each candidate in each position
    votes_subquery = (
        db.session.query(
            BallotPosition.candidate_id,
            BallotPosition.position_id,
            func.count().label('vote_count')
        )
        .group_by(BallotPosition.candidate_id, BallotPosition.position_id)
        .subquery()
    )

    # Subquery to find the maximum vote count for each position
    max_votes_subquery = (
        db.session.query(
            votes_subquery.c.position_id,
            func.max(votes_subquery.c.vote_count).label('max_votes')
        )
        .group_by(votes_subquery.c.position_id)
        .subquery()
    )

    # Query to get candidates with the highest votes in each position
    candidates_with_max_votes = (
        db.session.query(
            Candidate,
            max_votes_subquery.c.max_votes
        )
        .join(votes_subquery, Candidate.id == votes_subquery.c.candidate_id)
        .join(max_votes_subquery, votes_subquery.c.position_id == max_votes_subquery.c.position_id)
        .filter(votes_subquery.c.vote_count == max_votes_subquery.c.max_votes)
        .all()
    )

    # Query to calculate total votes across all positions
    total_votes = (
        db.session.query(func.count())
        .select_from(BallotPosition)
        .scalar()
    )

    return candidates_with_max_votes, total_votes


@app.route('/dashboard/candidates/add_candidate', methods=['GET', 'POST'])
@login_required
def add_candidate():
    form = CandidateForm()
    if form.validate_on_submit():
        position = Position.query.filter_by(position_name=form.position.data).first()
        if position:
            # Check if a candidate with the same details already exists
            existing_candidate = Candidate.query.filter_by(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                bio=form.bio.data,
                position=position
            ).first()

            if existing_candidate:
                flash("Candidate with the same details already exists", 'danger')
            else:
                filename = photos.save(form.candidate_img.data)
                file_url = url_for('server_uploaded_file', filename=filename)

                candidate = Candidate(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    bio=form.bio.data,
                    position=position,
                    candidate_img=file_url
                )
                db.session.add(candidate)
                db.session.commit()
                flash("Candidate added successfully", 'success')
                return redirect(url_for('candidates'))
        else:
            flash("Invalid position, Please try again", 'danger')
    return render_template('admin/add_candidate.html', form=form)

@app.route('/uploads/<filename>')
def server_uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/dashboard/candidates/<int:candidate_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    form = CandidateForm()

    if form.validate_on_submit():
        position = Position.query.filter_by(position_name=form.position.data).first()
        
        if position:
            # Handle file upload
            if form.candidate_img.data:
                filename = photos.save(form.candidate_img.data)
                file_url = url_for('server_uploaded_file', filename=filename)
                candidate.candidate_img = file_url

            # Update candidate details
            candidate.first_name = form.first_name.data
            candidate.last_name = form.last_name.data
            candidate.email = form.email.data
            candidate.phone = form.phone.data
            candidate.bio = form.bio.data
            candidate.position = position

            db.session.commit()
            flash("Candidate updated successfully", 'success')
            return redirect(url_for('candidates'))
        else:
            flash("Invalid position", 'danger')

    elif request.method == 'GET':
        # Populate the form with existing data
        form.first_name.data = candidate.first_name
        form.last_name.data = candidate.last_name
        form.email.data = candidate.email
        form.phone.data = candidate.phone
        form.bio.data = candidate.bio
        form.position.data = candidate.position.position_name  # Assuming your form has a 'position' field

    return render_template('admin/update_candidate.html', form=form, candidate=candidate)


@app.route('/dashboard/candidates/<int:candidate_id>/delete', methods=['POST'] )
@login_required
def delete_candidate(candidate_id):
    candidates = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidates)
    db.session.commit()
    flash("Candidate deleted successfull", 'success')
    return redirect(url_for('candidates'))

@app.route('/dashboard/positions/add_new', methods=['GET', 'POST'])
@login_required
def add_new_position():
    form = AddPosition()
    if form.validate_on_submit():
        existing_position = Position.query.filter_by(
            position_name=form.position_name.data
            ).first()
        
        if existing_position:
            flash("Position already exists, please try again!", 'warning')
            return redirect(url_for('add_new_position'))
        else:
            new_position = Position(
                position_name = form.position_name.data
            )
            db.session.add(new_position)
            db.session.commit()
            flash("Position added successfully", 'success')
            return redirect(url_for('positions'))
    return render_template('admin/add_position.html', form=form)

@app.route('/dashboard/positions/<int:position_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_position(position_id):
    position = Position.query.get_or_404(position_id)
    db.session.delete(position)
    db.session.commit()
    flash("Position has been deleted successfully", 'warning')
    return redirect(url_for('positions'))

@app.route('/dashboard/positions/<int:position_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_position(position_id):
    position = Position.query.get_or_404(position_id)
    form = AddPosition()
    if form.validate_on_submit():
        position.position_name = form.position_name.data
        db.session.commit()
        flash("Position edited successfully", 'success')
        return redirect(url_for('positions'))
    elif request.method == 'GET':
        form.position_name.data = position.position_name
        
    return render_template('admin/edit_position.html', form=form)
        