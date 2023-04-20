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
    
    def __init__(self, emp_id, email_id, password):
        self.emp_id = emp_id
        self.email_id = email_id
        self.password = password
        
    def get_id(self):
        return (self.emp_id)
        
    def __repr__(self):
        return f"User('{self.emp_number}', '{self.first_name}', '{self.last_name}', '{self.gender}', '{self.date_of_birth}', '{self.email}', '{self.password}', '{self.phone_number}', '{self.encoded_photo}')"