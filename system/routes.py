import os
from click import confirm
from flask import render_template, url_for, redirect, flash, request, send_from_directory
from sqlalchemy import func
from system import app, bcrypt, db, photos, serial, mail
from system.form import LoginForm, RegistrationForm, BallotForm, CandidateForm, AddPosition, EditVotingPeriod
from system.model import User, Candidate, BallotPosition, Position, VotingPeriod
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from flask_mail import Message


# This route handles the authenication login
# of voters or admin
@app.route('/', methods=['GET', 'POST'])
@app.route('/account/', methods=['GET', 'POST'])
@app.route('/account/login', methods=['GET', 'POST'])
def login_home():
    if current_user.is_authenticated: 
        return redirect(url_for('ballot'))  # Redirect authenticated users to the ballot page directly

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(reg_no=form.reg_no.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.is_approved:
                flash('Your account is still on the verification process,\
                    please wait for the confirmation email..', 'warning')
                return redirect(url_for('login_home'))
            login_user(user)
            return redirect(url_for('ballot'))
        else:
            flash('Login Unsuccessful, please check reg no. or password', 'danger')
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
        filename = photos.save(form.student_id.data)
        file_url = url_for('server_uploaded_file', filename=filename)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            reg_no=form.reg_no.data,
            student_id=file_url,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {user.first_name}, your voting account has been registered successfully.\
            wait for your account to be verified.', 'success')
        
        return redirect(url_for('login_home'))
    return render_template('register.html', form=form)

@app.route('/dashboard/verify/<int:user_id>', methods=['GET', 'POST'])
def verify(user_id):
    user = User.query.get_or_404(user_id)
    if user:
        user.is_approved = True
        db.session.commit()
        # send_confirmation_message(user.email)
        flash('Verified successfully', 'success')
        return redirect(url_for('home'))

@app.route('/dashboard/cancel_verification/<int:user_id>', methods=['GET', 'POST']) 
def cancel_verification(user_id):
    user = User.query.get_or_404(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Verification cancelled successfully', 'success')
        return redirect(url_for('home'))


def send_confirmation_message(email):
    msg = Message('Approval  Email', sender='noreply@mosesomo.tech', recipients=[email])
    msg.body = f'Your voting account has been verified successfully.'
    mail.send(msg)

# This routes logs out the user from the system
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_home'))


@app.route('/ballot', methods=['GET', 'POST'])
@login_required
def ballot():
    if current_user.is_admin:
        return redirect(url_for('home'))
    
    # Checking for voting period
    voting_period = VotingPeriod.query.first()
    current_time = datetime.now()
    
    print(f"Current Time: {current_time}")
    print(f"Voting Period Start Time: {voting_period.start_time if voting_period else 'No Voting Period Found'}")
    print(f"Current User is Admin: {current_user.is_admin}")
    
    if voting_period:
        if current_time > voting_period.end_time and not current_user.is_admin:
            flash(f'The voting period has ended. Closed at {voting_period.end_time}', 'danger')
            return redirect(url_for('ballot_positions')) # Redirect back to  login page
        elif current_time < voting_period.start_time and not current_user.is_admin:
            flash(f'Voting is not currently open! Please wait until {voting_period.start_time}.\
                  for now you can view the ballot positions', 'danger')
            return redirect(url_for('ballot_positions')) # Redirect back to  login page
    else:
        flash('No voting period found.', 'danger')
        return redirect(url_for('ballot_positions')) # Redirect back to  login page
    
    # Check if the user has already voted
    existing_votes = BallotPosition.query.filter_by(user_id=current_user.id).all()
    if existing_votes:
        flash('You have already voted.', 'warning')
        return redirect(url_for('ballot_positions')) # or redirect to a ballot_position page
        
    # Query candidates grouped by position
    grouped_candidates = {}
    positions = Position.query.all()

    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates
        
    form = BallotForm()
    if form.validate_on_submit():
        # Check if a vote has been cast for each position
        for position in positions:
            if not request.form.get(f'position_{position.id}'):
                flash(f'You have not cast a vote for {position.position_name} position!,\
                    Please make sure to vote for all positions available in the ballot',
                    'danger')
                return render_template('ballot.html',
                                    grouped_candidates=grouped_candidates,
                                    form=form)
        
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


@app.route('/dashboard/elections', methods=['GET', 'POST'])
def elections():
    upcoming_positions = Position.query.all()
    current_time = datetime.now()
    upcoming_elections = []

    for position in upcoming_positions:
        voting_period = VotingPeriod.query.first()

        if voting_period is None:
            # Handle the case where there is no voting period for the position
            # You might want to skip this position or set a default status
            continue

        if current_time < voting_period.start_time:
            status = 'Pending'
            status_class = 'text-warning'
        elif current_time >= voting_period.start_time and current_time <= voting_period.end_time:
            status = 'Active'
            status_class = 'text-success'
        else:
            status = 'Expired'
            status_class = 'text-danger'

        upcoming_elections.append({
            'id': position.id,
            'position_name': position.position_name,
            'num_candidates': len(position.candidates),
            'start_time': voting_period.start_time,
            'end_time': voting_period.end_time,
            'status': status,
            'status_class': status_class
        })
    return render_template('admin/period.html', upcoming_elections=upcoming_elections)

# This route queries and list the voters(users)
@app.route('/dashboard/voters')
@login_required
def voters():
    voters = User.query.all()
    return render_template('admin/voters.html', voters=voters)


@app.route('/dashboard/positions')
def positions():
    positions = Position.query.all()
    return render_template('admin/positions.html', positions=positions)

@app.route('/dashboard/candidates')
def candidates():
    candidates = Candidate.query.all()
    return render_template('admin/candidates.html', candidates=candidates)


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
    voting_period = VotingPeriod.query.first()
    current_time = datetime.now()
    grouped_candidates = {}
    positions = Position.query.all()
    
    if current_time < voting_period.start_time and not current_user.is_admin:
        flash('Can not acces this page, voting period not opened!', 'warning')
        return redirect(url_for('ballot_positions'))
    
    for position in positions:
        candidates = Candidate.query.filter_by(position=position).all()
        grouped_candidates[position] = candidates
        
    return render_template('admin/votes.html',
                           grouped_candidates=grouped_candidates)
    

@app.route('/my_votes/<int:user_id>', methods=['GET', 'POST'])
def my_votes(user_id):
    voting_period = VotingPeriod.query.first()
    current_time = datetime.now()
    if current_time < voting_period.start_time and not current_user.is_admin:
        flash('Can not acces this page, voting period not opened!', 'warning')
        return redirect(url_for('ballot_positions'))
    
    user = User.query.get_or_404(user_id)
    if user:
        ballots = BallotPosition.query.filter_by(user_id=current_user.id).all()
    return render_template('user_votes.html', ballots=ballots)

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
                           total_votes=total_votes,
                           voters=voters)


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
        # Get the position ID from the form data
        position_id = form.position.data
        # Query the Position object based on the position ID
        position = Position.query.get(position_id)
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
            flash("Invalid position, please make sure to add a position available in\
                the ballot, check on spellings and extra spaces", 'danger')
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
        position_id = form.position.data
        position = Position.query.get(position_id)
        
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

@app.route('/dashboard/elections/edit_time', methods=['GET', 'POST'])
def editVotingPeriod():
    election = VotingPeriod.query.get_or_404(1)
    form = EditVotingPeriod()
    if form.validate_on_submit():
        election.start_time = form.start_time.data
        election.end_time = form.end_time.data
        db.session.commit()
        flash('Voting period updated successfully', 'success')
        return redirect(url_for('elections'))
    elif request.method == 'GET':
        form.start_time.data = election.start_time
        form.end_time.data = election.end_time
        
    return render_template('admin/edit_period.html', form=form)

@app.route('/results')
def results():
    voting_period = VotingPeriod.query.first()
    current_time = datetime.now()
    if current_time < voting_period.start_time and not current_user.is_admin:
        flash('Can not acces this page, voting period not opened!', 'warning')
        return redirect(url_for('ballot_positions'))
    
    candidates_with_max_votes, total_votes = get_candidates_with_highest_votes()
    return render_template('admin/results.html',
                           candidates_with_max_votes=candidates_with_max_votes,
                           total_votes=total_votes)
