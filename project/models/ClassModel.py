from project import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from flask_login import current_user
from project.models.CourseModel import Course
from project.models.UserModel import User


class Class(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    created = Column(DateTime, nullable=False)
    created_by = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    teacher = db.relationship('User', backref='class', lazy=True)
    course = db.relationship('Course', backref='class', lazy=True)

    def __init__(self):
        self.course_id = 1
        self.user_id = 1
        self.code = 'class1'
        self.name = 'Class 1'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.created_by = 'admin'
        self.status = 1

    @staticmethod
    def insert_class(course_id, user_id, code, name, status):
        obj = Class()
        obj.course_id = course_id
        obj.user_id = user_id
        obj.code = code
        obj.name = name
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.created_by = current_user.username
        obj.status = status
        return obj

    @staticmethod
    def update_class(id, course_id, user_id, code, name, status):
        obj = Class.get_class(id)
        obj.course_id = course_id
        obj.user_id = user_id
        obj.code = code
        obj.name = name
        obj.status = status

    @staticmethod
    def get_class(id, status=None):
        if status is None:
            obj = Class.query.filter(Class.id == id).first()
        else:
            obj = Class.query.filter(Class.id == id, Class.status == status).first()
        if obj:
            return obj
        else:
            return None

    @staticmethod
    def get_all_class():
        return Class.query.filter().order_by(Class.code.asc()).all()


    @staticmethod
    def get_class_by_teacher(username, status=None):
        user = User.query.filter(username=username, role_id=2).first()
        if user:
            if status is None:
                return Class.query.filter(Class.user_id == user.id).order_by(Class.id.desc()).all()
            else:
                return Class.query.filter(Class.user_id == user.id, Class.status == status).order_by(Class.id.desc()).all()
        else:
            return None

    @staticmethod
    def get_related_class(id, course_id):
        return Class.query.filter(Class.id != id, Class.course_id == course_id, Class.status == 1).order_by(Class.code.asc()).all()

    @staticmethod
    def get_class_by_course(course_code, status=None):
        course = Course.query.filter_by(code=course_code).first()
        if course:
            if status is None:
                return Class.query.filter(Class.course_id == course.id).order_by(Class.code.asc()).all()
            else:
                return Class.query.filter(Class.course_id == course.id, Class.status == status).order_by(Class.id.asc()).all()
        else:
            return None