from project import db
import datetime
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from project.codes.Common import Common


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=True)
    firstname = Column(String(50), nullable=True)
    lastname = Column(String(50), nullable=True)
    birthdate = Column(String(10), nullable=True)
    gender = Column(Integer, nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    website = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    google_plus = Column(String, nullable=True)
    phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    address = Column(String, nullable=True)
    country = Column(String(100), nullable=True)
    nationality = Column(String(100), nullable=True)
    avatar = Column(String, nullable=True)
    authcode = Column(String, nullable=True)
    introduction = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    login = Column(DateTime, nullable=True)
    attending = Column(Integer, nullable=False, default=1)
    activated = Column(Integer, nullable=False, default=1)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = db.relationship('Role', backref='user', lazy=True)
    #class_id = Column(Integer, ForeignKey('class.id'), nullable=False) #Trainee
    xclass = db.relationship('Class', backref='user', lazy=True)
    resources = db.relationship('Resources', backref='user', lazy=True)
    assignment = db.relationship('Assignment', backref='user', lazy=True)
    announcement = db.relationship('Announcement', backref='user', lazy=True)
    trainee_assignment = db.relationship('Trainee_Assignment', backref='trainee', lazy=True)

    def __init__(self):
        self.username = 'admin'
        self.set_password('Admin@2018')
        self.firstname = 'Administrator'
        self.lastname = 'Thanh'
        self.birthdate = '1980/04/16'
        self.gender = 1
        self.email = 'ndthanh.cntt@gmail.com'
        self.website = 'http://lekima.net'
        self.mobile = '0918 907 325'
        self.address = 'Da Nang City'
        self.country = 'Viet Nam'
        self.nationality = 'Vietnamese'
        self.avatar = 'https://nguyenduythanh.files.wordpress.com/2007/03/dsc_0081.jpg?w=500&h=333'
        self.role_id = 1
        authcode = 'adminAdmin@2018ndthanh.cntt@gmail.com'
        self.authcode = Common.md5(authcode) # (username + password + email).md5
        self.introduction = 'Administrator of OEMS.'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_password(self, password):
        self.password = md5(password.encode()).hexdigest()

    def get_str_value(self, str):
        if str == None:
            return ''
        else:
            return str

    @staticmethod
    def profile(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def insert_user(username, password, email, role_id, introduction, firstname, lastname, address, nationality):
        obj = User()
        obj.username = username.lower()
        obj.set_password(password)
        obj.firstname = obj.get_str_value(firstname)
        obj.lastname = obj.get_str_value(lastname)
        obj.birthdate = None
        obj.gender = None
        obj.email = obj.get_str_value(email)
        obj.website = None
        obj.mobile = None
        obj.address = obj.get_str_value(address)
        obj.country = None
        obj.nationality = obj.get_str_value(nationality)
        obj.role_id = role_id
        #obj.authcode = authcode # Ham set authen nen duoc de o day
        obj.introduction = obj.get_str_value(introduction)
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.activated = 1
        return obj

    @staticmethod
    def update_user(user_id, username, password, email, role_id, introduction, firstname, lastname, address, nationality):
        obj = User.get_user(user_id)
        obj.username = username.lower()
        obj.set_password(password)
        obj.firstname = obj.get_str_value(firstname)
        obj.lastname = obj.get_str_value(lastname)
        obj.birthdate = None
        obj.gender = None
        obj.email = obj.get_str_value(email)
        obj.website = None
        obj.mobile = None
        obj.address = obj.get_str_value(address)
        obj.country = None
        obj.nationality = obj.get_str_value(nationality)
        obj.role_id = role_id
        # obj.authcode = authcode # Ham set authen nen duoc de o day
        obj.introduction = obj.get_str_value(introduction)
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.activated = 1
        return obj

    # Kiem tra username da ton tai hay chua
    @staticmethod
    def exists_username(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return True
        else:
            return False

    # Kiem tra email da ton tai hay chua
    @staticmethod
    def exists_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def get_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def get_all_users():
        return User.query.filter().order_by(User.username.asc()).all()