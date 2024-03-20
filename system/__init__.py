import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer



app = Flask(__name__)
app.config['SECRET_KEY'] = 'c4e8441a9ebafce522e2730f7ba526df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.root_path, 'uploads')
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '1c2bd454f2ab00d3042ab99d86492999'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
mail = Mail(app)

serial = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager(app)
login_manager.login_view = 'login_home'
login_manager.login_message_category = 'info'

from system import routes
