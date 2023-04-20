from ISMS import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    emp_id = db.Column(db.String(16), primary_key=True, nullable=False)
    email_id = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    acc_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    def __init__(self, emp_id: str, email_id: str, password: str) -> None:
        self.emp_id = emp_id
        self.email_id = email_id
        self.password = password
        
    def get_id(self):
        return (self.emp_id)
        
    def __repr__(self):
        return f"User('{self.emp_number}', '{self.first_name}', '{self.last_name}', '{self.gender}', '{self.date_of_birth}', '{self.email}', '{self.password}', '{self.phone_number}', '{self.encoded_photo}')"
    
class Employees(db.Model):
    __tablename__ = "employees"
    emp_id = db.Column(db.String(16), primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    enc_photo = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)
    address = db.Column(db.Text, nullable=True)
    
    def __init__(self, emp_id: str, first_name: str, last_name: str, gender: str, date_of_birth: str, end_photo: str, phone_number: str, address: str):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.enc_photo = enc_photo
        self.phone_number = phone_number
        self.address = address
        
    def __repr__(self):
        return f"Employee('{self.emp_id}', '{self.first_name}', '{self.last_name}', '{self.gender}', '{self.date_of_birth}', '{self.enc_photo}', '{self.phone_number}', '{self.address}')"