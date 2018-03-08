from project import db
import datetime
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime
from project.codes.Common import Common


class Teacher(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
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
    activated = Column(Integer, nullable=False, default=1)
    xclass = db.relationship('Class', backref='teacher', lazy=True)
    resources = db.relationship('Resources', backref='teacher', lazy=True)
    assignment = db.relationship('Assignment', backref='teacher', lazy=True)
    announcement = db.relationship('Announcement', backref='teacher', lazy=True)

    def __init__(self):
        self.username = 'ndthanh'
        self.set_password('ndthanh')
        self.firstname = 'Nguyen Duy'
        self.lastname = 'Thanh'
        self.birthdate = '1980/04/16'
        self.gender = 1
        self.email = 'ndthanh.cntt@gmail.com'
        self.website = 'http://lekima.net'
        self.degree = 'Master'
        self.facebook = 'https://www.facebook.com/duythanh.bluestar'
        self.google_plus = 'https://plus.google.com/u/0/114990571875113632427'
        self.mobile = '0918 907 325'
        self.address = 'Da Nang City'
        self.country = 'Viet Nam'
        self.nationality = 'Vietnamese'
        self.avatar = 'https://nguyenduythanh.files.wordpress.com/2007/03/dsc_0081.jpg?w=500&h=333'
        authcode = 'ndthanhndthanh123ndthanh.cntt@gmail.com' # (username + password + email).md5
        self.authcode = Common.md5(authcode)
        self.introduction = 'Programmer'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_password(self, password):
        self.password = md5(password.encode()).hexdigest()

    @staticmethod
    def profile(username):
        teacher = Teacher.query.filter_by(username=username).first()
        if teacher:
            return teacher
        else:
            return None

    @staticmethod
    def insert_teacher(username, password, firstname, lastname, birthdate, gender, email, degree, authcode, introduction, activated):
        obj = Teacher()
        obj.username = username
        obj.set_password(password)
        obj.firstname = firstname
        obj.lastname = lastname
        obj.birthdate = birthdate
        obj.gender = gender
        obj.email = email
        obj.degree = degree
        obj.authcode = authcode # Ham set authen nen duoc de o day
        obj.introduction = introduction
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.activated = activated
        return obj

    # Kiem tra email da ton tai hay chua
    @staticmethod
    def exists_email(email):
        user = Teacher.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def get_teacher(username):
        user = Teacher.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def get_all_teachers():
        return Teacher.query.filter().order_by(Teacher.username.asc()).all()