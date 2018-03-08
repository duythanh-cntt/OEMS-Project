from project import db
import datetime
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, DateTime
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
    facebook = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    google_plus = Column(String, nullable=True)
    phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    address = Column(String, nullable=True)
    country = Column(String(100), nullable=True)
    nationality = Column(String(100), nullable=True)
    avatar = Column(String, nullable=True)
    role = Column(String(50), nullable=True)
    authcode = Column(String, nullable=True)
    introduction = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    login = Column(DateTime, nullable=True)
    activated = Column(Integer, nullable=False, default=1)
    announcement = db.relationship('Announcement', backref='user', lazy=True)

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
        self.role = 'Admin'
        authcode = 'adminAdmin@2018ndthanh.cntt@gmail.com'
        self.authcode = Common.md5(authcode) # (username + password + email).md5
        self.introduction = 'Administrator of OEMS.'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_password(self, password):
        self.password = md5(password.encode()).hexdigest()

    @staticmethod
    def profile(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def insert_user(username, password, email, role, authcode, introduction, activated):
        obj = User()
        obj.username = username
        obj.set_password(password)
        obj.firstname = None
        obj.lastname = None
        obj.birthdate = None
        obj.gender = None
        obj.email = email
        obj.website = None
        obj.mobile = None
        obj.address = None
        obj.country = None
        obj.nationality = None
        obj.role = role
        obj.authcode = authcode # Ham set authen nen duoc de o day
        obj.introduction = introduction
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.activated = activated
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