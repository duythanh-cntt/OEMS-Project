from project import db
from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
import datetime
from flask_login import current_user
from project.models.TraineeModel import Trainee
from project.models.AssignmentModel import Assignment


class Trainee_Assignment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    trainee_id = Column(Integer, ForeignKey('trainee.id'), nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignment.id'), nullable=False)
    submission_date = Column(Date, nullable=True)
    link = Column(String, nullable=True)
    note = Column(String, nullable=True)
    score = Column(Float, nullable=True)

    def __init__(self):
        self.trainee_id = 1
        self.assignment_id = 1
        self.submission_date = '2018-03-20'
        self.link = 'https://gist.github.com/duythanh-cntt/149ab6382cf1b17427c30589f3ea23a6'
        self.note = ''
        self.score = 7.5