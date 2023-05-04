from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "7980184255359f0b85941714f0bfbcee"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://starkhan:bmwm3gtr@localhost:5432/ISMS"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

from ISMS.users.routes import users
from ISMS.main.routes import main
from ISMS.api.routes import api

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(api)