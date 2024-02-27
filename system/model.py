from system import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    password = db.Column(db.String(20), unique=True,  nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add a field to distinguish between voters and admins
    # Relationship to retrieve user's votes (for voters)
    votes = db.relationship('BallotPosition', backref='voter', lazy=True)
    
    def __repr__(self):
        return f"[({self.first_name}), ({self.last_name}), ({self.last_email}), ({self.password}), ({self.is_admin}), ({self.votes})]"


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(16))
    candidate_img = db.Column(db.String(255), nullable=False, default="default.jpg")
    bio = db.Column(db.Text)

    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))
     # Relationships
    votes = db.relationship('BallotPosition', backref='candidate', lazy=True)
    position = db.relationship('Position', backref='candidates', lazy=True)

    def __repr__(self):
        return f"[({self.name}), ({self.emai}), ({self.phone}), ({self.candidte_img}), ({self.bio}), ({self.position_id}), ({self.votes}), ({self.position})]"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(40), unique=True)
    # Relationship
    candidates = db.relationship('Candidate', backref='position', lazy=True)


    def __repr__(self):
        return f"[({self.position_name}), ({self.candidates})]"


class BallotPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    
    # Relationships
    user = db.relationship('User', backref='votes', lazy=True)
    candidate = db.relationship('Candidate', backref='votes', lazy=True)
    position = db.relationship('Position', backref='votes', lazy=True)


    def __repr__(self):
        return f"[({self.candidate_id}), ({self.user_id}), ({self.position_id}), ({self.user}), ({self.candidate}), ({self.position})]"

