from ISMS import db, login_manager
from datetime import datetime, timezone, timedelta
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    emp_id = db.Column(db.String(8), db.ForeignKey('employees.emp_id'), primary_key=True, nullable=False)
    email_id = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    acc_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(10),  nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    employee = db.relationship("Employee", back_populates="user", uselist=False)
    
    def __init__(self, emp_id: str, email_id: str, password: str, status: str, is_admin: bool) -> None:
        self.emp_id = emp_id
        self.email_id = email_id
        self.password = password
        self.status = status
        self.is_admin = is_admin
        
    def get_id(self):
        return (self.emp_id)
        
    def __repr__(self):
        return f"User('{self.emp_id}', '{self.email_id}', '{self.password}', '{self.status}', '{self.is_admin}')"
    
    def as_dict(self, values):
        values = values or self.__table__.columns.keys()
        try:
            values.remove("password")
        except ValueError:
            pass
        user_data = {attr : getattr(self, attr) for attr in values}
        user_data.update({"first_name":self.employee.first_name ,"last_name": self.employee.last_name, "position": self.employee.position})
        return user_data

    
class Employee(db.Model):
    __tablename__ = "employees"
    emp_id = db.Column(db.String(8), primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    enc_photo = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)
    address = db.Column(db.Text, nullable=True)
    position = db.Column(db.String(10), nullable=False)
    user = db.relationship('User', back_populates='employee', uselist=False)
    
    def __init__(self, emp_id: str, first_name: str, last_name: str, gender: str, date_of_birth: str, enc_photo: str, phone_number: str, address: str, position:str):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.enc_photo = enc_photo
        self.phone_number = phone_number
        self.address = address
        self.position = position
        
    def __repr__(self):
        return f"Employee('{self.emp_id}', '{self.first_name}', '{self.last_name}', '{self.gender}', '{self.date_of_birth}', '{self.enc_photo}', '{self.phone_number}', '{self.address}', '{self.position}')"
    
    def as_dict(self, values):
        values = values or self.__table__.columns.keys()
        employee_data = {attr : getattr(self, attr) for attr in values}
        if self.user:
            employee_data.update({"email" : self.user.email_id, "acc_created": self.user.acc_created, "status":self.user.status})
        return employee_data

class Cluster(db.Model):
    __tablename__ = "clusters"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    location = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    camera = db.Column(db.String(20), nullable=True)
    camera_status = db.Column(db.String(10), nullable=True)
    sensors = db.relationship('Sensor', backref='cluster')
    
    def __init__(self, name: str, location: str, status: str, camera: str = None , camera_status: str = None):
        self.name = name
        self.location = location
        self.status = status
        self.camera = camera
        self.camera_status = camera_status
        
    def __repr__(self) -> str:
        return f"Cluster('{self.id}, {self.name}', '{self.location}', '{self.status}', '{self.camera}', '{self.camera_status}')"
    
    def as_dict(self, values):
        values = values or self.__table__.columns.keys()
        cluster_data = {attr: getattr(self, attr) for attr in values}
        return cluster_data
    
class Sensor(db.Model):
    __tablename__ = "clusters_data"
    free_heap = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, primary_key=True, default=db.func.current_timestamp())
    cluster_id = db.Column(db.Integer, db.ForeignKey("clusters.id"), nullable=False)
    temperature = db.Column(db.Numeric(10,2), nullable=False)
    humidity = db.Column(db.Numeric(10,2), nullable=False)
    pressure = db.Column(db.Numeric(10,2), nullable=False)
    lpg = db.Column(db.Numeric(10,2), nullable=False)
    methane = db.Column(db.Numeric(10,2), nullable=False)
    smoke = db.Column(db.Numeric(10,2), nullable=False)
    hydrogen = db.Column(db.Numeric(10,2), nullable=False)
    ppm = db.Column(db.Numeric(10,2), nullable=False)
    
    def __init__(self, cluster_id: int, temperature: float, humidity: float, pressure: float, lpg: float, methane: float, smoke: float, hydrogen: float, ppm: float, free_heap:str, date_time) -> None:
        self.date_time = datetime(*date_time[:-1], timezone(timedelta(hours=5, minutes=30)))
        self.cluster_id = cluster_id
        self.free_heap = free_heap
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.lpg = lpg
        self.methane = methane
        self.smoke = smoke
        self.hydrogen = hydrogen
        self.ppm = ppm
        
    def __repr__(self) -> str:
        return f"Sensor('{self.date_time}', '{self.cluster_id}', '{self.temperature}', '{self.humidity}', '{self.pressure}', '{self.lpg}', '{self.methane}', '{self.smoke}', '{self.hydrogen}', '{self.ppm}')"

    def as_dict(self):
        sensor_data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        sensor_data.update({'status': self.cluster.status})
        return sensor_data
    
class Entry(db.Model):
    __tablename__ = "entries"
    entry_id = db.Column(db.Integer, primary_key=True, nullable=False, default=db.func.next_val('entries_entry_id_seq'))
    date_time = db.Column(db.DateTime, nullable=False)
    emp_id = db.Column(db.String(8), db.ForeignKey("employees.emp_id"), nullable=False)
    photo = db.Column(db.Text, nullable=False)
    
    def __init__(self, date_time, emp_id, photo):
        self.date_time = date_time
        self.emp_id = emp_id
        self.photo = photo