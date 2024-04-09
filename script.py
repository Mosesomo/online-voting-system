from system import app, db, bcrypt
from system.model import User, Candidate, Position, BallotPosition, VotingPeriod
from datetime import datetime

with app.app_context():
    db.create_all()
    
    """hashed_password = (bcrypt.generate_password_hash
                           ('password')
                           .decode('utf-8'))
    admin_user = User.query.filter_by(first_name='admin').first()
    if not admin_user:
        user = User(
            first_name='admin',
            last_name='user',
            reg_no='admin-05-0236/2017',
            email='admin@example.com',
            is_admin=True,
            password=hashed_password,
            is_approved=True,
            student_id='default.jpg'
            )
        db.session.add(user)""" # Use db.session.add() instead of db.add_all()
    """user = User(
        first_name='Anne',
        last_name='Njeri',
        email='njeri@example.com',
        is_admin=False,
        password='password',
        email_confirmed=True
    )
    db.session.add(user)
        
    position1 = Position(position_name='President')
    db.session.add(position1)
    position2 = Position(position_name='Academic sec')
    db.session.add(position2)
    position3 = Position(position_name='Accounts')
    db.session.add(position3)
    position4 = Position(position_name='Games and sports')
    db.session.add(position4)
    
    candidate1 = Candidate(
        first_name='Moses',
        last_name='Omondi',
        email="moses4@gmail.com",
        phone='+2547838387',
        bio="Have a growth mindset",
        candidate_img='img/boy1.webp',
        position_id=1
    )
    
    candidate2 = Candidate(
        first_name='Elvis',
        last_name='Onyango',
        email="onyango4@gmail.com",
        phone='+2547838387',
        bio="Have a growth mindset",
        candidate_img='img/boy2.webp',
        position_id=2
    )
    
    db.session.add(candidate2)
    
    candidate4 = Candidate(
        first_name='Owuor',
        last_name='Nicholus',
        email="owuor@gmail.com",
        phone='+25487654',
        bio="Leader for all",
        candidate_img='img/boy5.jpeg',
        position_id=4
    )
    
    db.session.add(candidate4)
    
    candidate5 = Candidate(
        first_name='Jasmin',
        last_name='Cheptum',
        email="cheptum@gmail.com",
        phone='+2546567',
        bio="Have a growth mindset",
        candidate_img='img/lady3.jpeg',
        position_id=3
    )
    
    db.session.add(candidate5)
    
    candidate6 = Candidate(
        first_name='Cynthia',
        last_name='Njoroge',
        email='cynthia@gmail.com',
        phone='+4545653',
        bio="Leader for all",
        candidate_img='img/lady5.jpeg',
        position_id=4
    )
    
    db.session.add(candidate6)
    
    candidate7 = Candidate(
        first_name='George',
        last_name='Wangombe',
        email="george@gmail.com",
        phone='+254455387',
        bio="Have a growth mindset",
        candidate_img='img/boy6.jpeg',
        position_id=3
    )
    
    db.session.add(candidate7)
    
    candidate8 = Candidate(
        first_name='Nyagut',
        last_name='Kiptum',
        email="kiptum@gmail.com",
        phone='+25476654',
        bio="Intelligent and ready to deliver",
        candidate_img='img/boy3.webp',
        position_id=1
    )
    
    db.session.add(candidate8)
    
    candidate9 = Candidate(
        first_name='Joan',
        last_name='Nyamboka',
        email="joan@gmail.com",
        phone='+2547665544',
        bio="Together we can",
        candidate_img='img/lady4.webp',
        position_id=2
    )
    
    db.session.add(candidate9)
    
    ballot = BallotPosition(
        user_id=2,
        position_id = 1,
        candidate_id = 1
    )
    db.session.add(ballot)
    
    # candidate1 = Candidate.query.get(9)
    # candidate1.candidate_img = 'img/boy6.jpeg'
    
    start_time = datetime(2024, 4, 7, 13, 0, 0) # March 15, 2024, 9:00 AM
    end_time = datetime(2024, 3, 8, 17, 0, 0) # March 16, 2024, 5:00 PM
    position_id = 1

    # Create a new voting period entry
    new_voting_period = VotingPeriod(start_time=start_time, end_time=end_time, position_id=position_id)"""

    # Add the new entry to the session
    # db.session.add(new_voting_period)
    
    
    # period = VotingPeriod.query.get(1)
    # period.end_time = datetime(2024, 4, 8, 17, 35, 0)
    # db.session.delete(VotingPeriod.query.get(1))
    #users = User.query.all()
    # db.session.delete(users)
    
    # db.session.delete(User.query.get(3))
    
    db.session.commit() # Use db.session.commit()
    
    users = User.query.all()
    for user in users:
        print(user.votes)
    print('\n')  
    positions = Position.query.all()
    for position in positions:
        print(position)
    print("\n")
    candidates = Candidate.query.all()
    for candidate in candidates:
        print(candidate)
    print("\n")   
    ballots = BallotPosition.query.all()
    for ballot in ballots:
        print("Voter Name: {}\nVoted for: {}\nPosition: {}\n"
              .format(ballot.user.first_name, ballot.candidate.first_name, ballot.position.position_name))
    print("\n")
        
    voting_period = VotingPeriod.query.all()
    for period in voting_period:
        print(period)
        
