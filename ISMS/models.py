from ISMS import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    __tablename__ = "employee"
    emp_number = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    encoded_photo = db.Column(db.Text, nullable=False)
    
    
    def __init__(self, emp_number, first_name, last_name, gender, date_of_birth, email, password, phone_number, encoded_photo):
        self.emp_number = emp_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.encoded_photo = encoded_photo
        
    def get_id(self):
        return (self.emp_number)
    
    def __repr__(self):
        return f"User('{self.emp_number}', '{self.first_name}', '{self.last_name}', '{self.gender}', '{self.date_of_birth}', '{self.email}', '{self.password}', '{self.phone_number}', '{self.encoded_photo}')"