from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "<SECRET_KEY>"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://<username>:<password>@localhost:5432/ISMS"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from ISMS import routes