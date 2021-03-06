from project import db
import datetime
from hashlib import md5
from flask_login import UserMixin, current_user
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from project.codes.Common import Common


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=True)
    firstname = Column(String(50), nullable=True)
    lastname = Column(String(50), nullable=True)
    birthdate = Column(String(10), nullable=True)
    gender = Column(Integer, nullable=True)
    degree = Column(String, nullable=True)
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
    authcode = Column(String, nullable=True) # Mã xác thực để kích hoạt tài khoản (để dự trữ, chưa dùng tới)
    introduction = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    created_by = Column(String(50), nullable=False)
    login = Column(DateTime, nullable=True)
    attending = Column(Integer, nullable=True)
    activated = Column(Integer, nullable=False, default=1)
    xclass = db.relationship('Class', backref='user', lazy=True)
    resources = db.relationship('Resources', backref='user', lazy=True)
    assignment = db.relationship('Assignment', backref='user', lazy=True)
    announcement = db.relationship('Announcement', backref='user', lazy=True)
    trainee_assignment = db.relationship('Trainee_Assignment', backref='user', lazy=True)

    # def __init__(self, role_id, username, password, firstname, lastname, birthdate, gender, email, website, mobile, address, country, nationality, avatar, authcode, introduction):
    #     self.role_id = role_id
    #     self.username = username
    #     self.set_password(password)
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.birthdate = birthdate
    #     self.gender = gender
    #     self.email = email
    #     self.website = website
    #     self.mobile = mobile
    #     self.address = address
    #     self.country = country
    #     self.nationality = nationality
    #     self.avatar = avatar
    #     self.authcode = Common.md5(authcode) # (username + password + email).md5
    #     self.introduction = introduction
    #     self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self):
        self.role_id = 1
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
        authcode = 'adminAdmin@2018ndthanh.cntt@gmail.com'
        self.authcode = Common.md5(authcode) # (username + password + email).md5
        self.introduction = 'Administrator of OEMS.'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.created_by = 'admin'

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
    def insert_user(role_id, username, password, firstname, lastname, email, address, nationality, introduction, authcode, activated):
        obj = User()
        obj.role_id = role_id
        obj.username = username.lower()
        obj.set_password(password)
        obj.firstname = Common.get_str_value(firstname)
        obj.lastname = Common.get_str_value(lastname)
        obj.birthdate = None
        obj.gender = None
        obj.email = Common.get_str_value(email)
        obj.website = None
        obj.mobile = None
        obj.address = Common.get_str_value(address)
        obj.country = None
        obj.nationality = Common.get_str_value(nationality)
        obj.avatar = None
        obj.introduction = Common.get_str_value(introduction)
        obj.attending = 1
        obj.authcode = authcode # Ham set authen nen duoc de o day
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.created_by = current_user.username
        obj.activated = activated
        return obj

    @staticmethod
    def update_user(role_id, user_id, username, password, firstname, lastname, email, address, nationality, introduction, authcode, activated):
        obj = User.get_user(user_id)
        obj.role_id = role_id
        obj.username = username.lower()
        obj.set_password(password)
        obj.firstname = Common.get_str_value(firstname)
        obj.lastname = Common.get_str_value(lastname)
        obj.birthdate = None
        obj.gender = None
        obj.email = Common.get_str_value(email)
        obj.website = None
        obj.mobile = None
        obj.address = Common.get_str_value(address)
        obj.country = None
        obj.nationality = Common.get_str_value(nationality)
        obj.introduction = Common.get_str_value(introduction)
        obj.authcode = authcode
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.activated = activated
        # return obj

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
    def get_user(id):
        user = User.query.filter_by(id=id).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def get_all_teacher():
        teachers = User.query.filter_by(role_id=2).order_by(User.username.asc()).all()
        if teachers:
            return teachers
        else:
            return None


    @staticmethod
    def get_all_users():
        return User.query.filter().order_by(User.username.asc()).all()