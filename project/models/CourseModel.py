from project import db
from sqlalchemy import Column, Integer, String
from flask_login import current_user


class Course(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    created_by = Column(String(50), nullable=False)
    # xclass = db.relationship('Class', backref='course', lazy=True)

    def __init__(self):
        self.code = 'python'
        self.name = 'Python course'
        self.created_by = 'admin'

    @staticmethod
    def get_course(course_id):
        course = Course.query.filter_by(id=course_id).first()
        if course:
            return course
        else:
            return None

    @staticmethod
    def insert_course(code, name):
        obj = Course()
        obj.code = code
        obj.name = name
        obj.created_by = current_user.username
        return obj

    @staticmethod
    def update_course(course_id, code, name):
        obj = Course.get_course(course_id)
        obj.code = code
        obj.name = name

    @staticmethod
    def get_all_course():
        return Course.query.filter().order_by(Course.code.asc()).all()
