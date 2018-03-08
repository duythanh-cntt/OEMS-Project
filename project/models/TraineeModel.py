from project import db
import datetime
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from project.codes.Common import Common


class Trainee(UserMixin, db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
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
    authcode = Column(String, nullable=True)
    introduction = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    login = Column(DateTime, nullable=True)
    attending = Column(Integer, nullable=False, default=1)
    activated = Column(Integer, nullable=False, default=1)
    trainee_assignment = db.relationship('Trainee_Assignment', backref='trainee', lazy=True)

    def __init__(self):
        self.class_id = 1
        self.username = 'truongbao'
        self.set_password('truongbao123')
        self.firstname = 'Truong'
        self.lastname = 'Bao'
        self.birthdate = ''
        self.gender = 1
        self.email = 'truongbao@gmail.com'
        self.website = ''
        self.facebook = ''
        self.google_plus = ''
        self.mobile = ''
        self.address = 'Hue City'
        self.country = 'Viet Nam'
        self.nationality = 'Vietnamese'
        self.avatar = ''
        authcode = 'truongbaotruongbao123truongbao@gmail.com' # (username + password + email).md5
        self.authcode = Common.md5(authcode)
        self.introduction = 'Programmer'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_password(self, password):
        self.password = md5(password.encode()).hexdigest()

    @staticmethod
    def profile(username):
        user = Trainee.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def insert_trainnee(username, password, firstname, lastname, birthdate, gender, email, authcode, introduction, attending, activated):
        obj = Trainee()
        obj.username = username
        obj.set_password(password)
        obj.firstname = firstname
        obj.lastname = lastname
        obj.birthdate = birthdate
        obj.gender = gender
        obj.email = email
        obj.authcode = authcode # Ham set authen nen duoc de o day
        obj.introduction = introduction
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.attending = attending
        obj.activated = activated
        return obj

    # Kiem tra email da ton tai hay chua
    @staticmethod
    def exists_email(email):
        user = Trainee.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def get_trainnee(username):
        user = Trainee.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @staticmethod
    def get_all_trainnees():
        return Trainee.query.filter().order_by(Trainee.username.asc()).all()