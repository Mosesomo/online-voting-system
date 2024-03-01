from system import app, db, bcrypt
from system.model import User, Candidate, Position, BallotPosition

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
            email='admin@example.com',
            is_admin=True,
            password=hashed_password
            )
        db.session.add(user)""" # Use db.session.add() instead of db.add_all()
    """user = User(
        first_name='Anne',
        last_name='Njeri',
        email='njeri@example.com',
        is_admin=False,
        password='password'
    )
    db.session.add(user)"""
        
    """position1 = Position(position_name='President')
    db.session.add(position1)
    position2 = Position(position_name='Academic sec')
    db.session.add(position2)
    position3 = Position(position_name='Accounts')
    db.session.add(position3)
    position4 = Position(position_name='Games and sports')
    db.session.add(position4)"""
    
    """candidate1 = Candidate(
        first_name='Moses',
        last_name='Omondi',
        email="moses4@gmail.com",
        phone='+2547838387',
        bio="Have a growth mindset",
        candidate_img='img/userplaceholder.png',
        position_id=1
    )"""
    
    """candidate2 = Candidate(
        first_name='Elvis',
        last_name='Onyango',
        email="onyango4@gmail.com",
        phone='+2547838387',
        bio="Have a growth mindset",
        candidate_img='img/userplaceholder.png',
        position_id=2
    )
    
    db.session.add(candidate2)"""
    
    """candidate4 = Candidate(
        first_name='Owuor',
        last_name='Nicholus',
        email="owuor@gmail.com",
        phone='+25487654',
        bio="Leader for all",
        candidate_img='img/userplaceholder.png',
        position_id=4
    )
    
    db.session.add(candidate4)
    
    candidate5 = Candidate(
        first_name='Jasmin',
        last_name='Cheptum',
        email="cheptum@gmail.com",
        phone='+2546567',
        bio="Have a growth mindset",
        candidate_img='img/userplaceholder.png',
        position_id=3
    )
    
    db.session.add(candidate5)
    
    candidate6 = Candidate(
        first_name='Cynthia',
        last_name='Njoroge',
        email='cynthia@gmail.com',
        phone='+4545653',
        bio="Leader for all",
        candidate_img='img/userplaceholder.png',
        position_id=4
    )
    
    db.session.add(candidate6)
    
    candidate7 = Candidate(
        first_name='George',
        last_name='Wangombe',
        email="george@gmail.com",
        phone='+254455387',
        bio="Have a growth mindset",
        candidate_img='img/userplaceholder.png',
        position_id=3
    )
    
    db.session.add(candidate7)
    
    candidate8 = Candidate(
        first_name='Nyagut',
        last_name='Kiptum',
        email="kiptum@gmail.com",
        phone='+25476654',
        bio="Intelligent and ready to deliver",
        candidate_img='img/userplaceholder.png',
        position_id=1
    )
    
    db.session.add(candidate8)
    
    candidate9 = Candidate(
        first_name='Joan',
        last_name='Nyamboka',
        email="joan@gmail.com",
        phone='+2547665544',
        bio="Together we can",
        candidate_img='img/userplaceholder.png',
        position_id=2
    )
    
    db.session.add(candidate9)"""
    
    """ballot = BallotPosition(
        user_id=2,
        position_id = 1,
        candidate_id = 1
    )
    db.session.add(ballot)"""
    
    # candidate1 = Candidate.query.get(9)
    # candidate1.candidate_img = 'img/boy6.jpeg'
    
    
    db.session.commit() # Use db.session.commit() instead of db.commit()
    
    users = User.query.all()
    for user in users:
        print(user)
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
        print(ballot)
        
