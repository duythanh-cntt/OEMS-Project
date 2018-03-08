from project import db
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
import datetime
from flask_login import current_user
from project.models.TeacherModel import Teacher
from project.models.CategoryModel import Category


class Assignment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    name = Column(String, nullable=False)
    link = Column(String, nullable=True)
    description = Column(String, nullable=True)
    deadline = Column(Date, nullable=True)
    tags = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False, default=1)
    trainee_assignment = db.relationship('Trainee_Assignment', backref='assignment', lazy=True)

    def __init__(self):
        self.teacher_id = 1
        self.category_id = 1
        self.name = 'Bartender'
        self.link = 'https://classroom.google.com/u/0/c/OTM2MzY2NDMwM1pa/a/OTM4MjA2MzE0MVpa/details'
        self.description = 'Given two above dictionaries, construct the Python program (using functions) to ask users entering their tastes and then match randomly with the ingredients (print out outputs for user).'
        self.deadline = '2018-03-20'
        self.tags = 'Bartender, dictionaries, construct'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = 1

    @staticmethod
    def insert_assignment(teacher_id, cat_id, name, link, description, deadline, tags, status):
        obj = Assignment()
        obj.teacher_id = teacher_id
        obj.category_id = cat_id
        obj.name = name
        obj.link = link
        obj.description = description
        obj.deadline = deadline
        obj.tags = tags
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.status = status
        return obj

    @staticmethod
    def update_assignment(id, teacher_id, cat_id, name, link, description, deadline, tags, status):
        obj = Assignment.get_assignment(id)
        obj.teacher_id = teacher_id
        obj.category_id = cat_id
        obj.name = name
        obj.link = link
        obj.description = description
        obj.deadline = deadline
        obj.tags = tags
        obj.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.status = status

    @staticmethod
    def get_assignment(id, status=None):
        if status is None:
            result = Assignment.query.filter(Assignment.id == id).first()
        else:
            result = Assignment.query.filter(Assignment.id == id, Assignment.status == status).first()
        if result:
            return result
        else:
            return None

    @staticmethod
    def get_assignment_by_teacher(username, status=None):
        user = Teacher.query.filter_by(username=username).first()
        if user:
            if status is None:
                return Assignment.query.filter(Assignment.teacher_id == user.id).order_by(Assignment.id.desc()).all()
            else:
                return Assignment.query.filter(Assignment.teacher_id == user.id, Assignment.status == status).order_by(Assignment.id.desc()).all()
        else:
            return None

    @staticmethod
    def get_related_assignment(id, cat_id):
        return Assignment.query.filter(Assignment.id != id, Assignment.category_id == cat_id, Assignment.status == 1).order_by(Assignment.id.desc()).all()

    @staticmethod
    def get_assignment_by_cat(cat_code, status=None):
        cat = Category.query.filter_by(code=cat_code).first()
        if cat:
            if status is None:
                return Assignment.query.filter(Assignment.category_id == cat.id).order_by(Assignment.id.desc()).all()
            else:
                return Assignment.query.filter(Assignment.category_id == cat.id, Assignment.status == status).order_by(Assignment.id.desc()).all()
        else:
            return None