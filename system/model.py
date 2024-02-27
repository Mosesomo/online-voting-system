from system import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True,  nullable=False)

    def __repr__(self):
        return f"[({self.first_name}), ({self.last_name}), ({self.last_email}), ({self.password})]"


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(16))
    candidate_img = db.Column(db.String(255), nullable=False, default="default.jpg")
    bio = db.Column(db.Text)
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))

    def __repr__(self):
        return f"[({self.name}), ({self.emai}), ({self.phone}), ({self.candidte_img}), ({self.bio}), ({self.position_id})]"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(40), unique=True)

    def __repr__(self):
        return f"[({self.position_name})]"


class BallotPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    def __repr__(self):
        return f"[({self.candidate_id}), ({self.user_id}), ({self.position_id})]"
