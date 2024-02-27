from system import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Add a field to distinguish between voters and admins
    # Relationship to retrieve user's votes (for voters)
    votes = db.relationship('BallotPosition', lazy=True, viewonly=True)

    def __repr__(self):
        return (
            f"User(id={self.id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"email={self.email}, "
            f"password={self.password}, "
            f"is_admin={self.is_admin})"
        )

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(16))
    candidate_img = db.Column(db.String(255), nullable=False, default="default.jpg")
    bio = db.Column(db.Text)

    # Relationships
    votes = db.relationship('BallotPosition', back_populates='candidate', lazy=True)
    position = db.relationship('Position', back_populates='candidates')

    def __repr__(self):
        return (
            f"Candidate("
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"email={self.email}, "
            f"phone={self.phone}, "
            f"candidate_img={self.candidate_img}, "
            f"bio={self.bio}, "
            f"position={self.position.position_name}"
        )

    def __repr__(self):
        return f"[({self.name}), ({self.emai}), ({self.phone}), ({self.candidte_img}), ({self.bio}), ({self.position_id}), ({self.votes}), ({self.position})]"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(40), unique=True)
    # Relationship
    candidates = db.relationship('Candidate', back_populates='position')
    # Change back_populates to 'votes' to match BallotPosition model
    votes = db.relationship('BallotPosition', back_populates='position', lazy=True)

    def __repr__(self):
        return (
            f"{self.id}, {self.position_name}"
        )

class BallotPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    # Relationships
    user = db.relationship('User', back_populates='votes', lazy=True)
    # Add back_populates to the relationships
    candidate = db.relationship('Candidate', back_populates='votes')
    position = db.relationship('Position', back_populates='votes')

    def __repr__(self):
        return (
            f"BallotPosition(id={self.id}, "
            f"candidate_id={self.candidate_id}, "
            f"user_id={self.user_id}, "
            f"position_id={self.position_id}, "
            f"candidate={self.candidate}, "
            f"position={self.position})"
        )
