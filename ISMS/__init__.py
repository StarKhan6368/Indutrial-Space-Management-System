from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "<SECRET_KEY>"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://<username>:<password>@localhost:5432/ISMS"
db = SQLAlchemy(app)

from ISMS import routes