from system import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.string(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullabe=False)
    
class Candidate(db.Model):
    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(16))
    candidate_img = db.Column(db.String(255), nullable=False, default="default.jpg")
    bio = db.Column(db.Text)
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))
    
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(40), unique=True)
    
class BallotPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    