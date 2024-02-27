from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_home"
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_home"
login_manager.login_message_category = 'info'


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from system.model import User, Candidate, Position, BallotPosition

with app.app_context():
    db.create_all()

from system import routes
