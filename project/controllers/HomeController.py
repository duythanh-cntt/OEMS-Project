from project import app, db
from flask import redirect, render_template, request
from flask_login import login_required, current_user
from project.models.UserModel import User
from project.models.TeacherModel import Teacher
from project.models.TraineeModel import Trainee
from project.models.CourseModel import Course
from project.models.ClassModel import Class
from project.models.CategoryModel import Category
from project.models.AssignmentModel import Assignment
from project.models.ResourcesModel import Resources
from project.models.AnnouncementModel import Announcement
from project.models.Trainee_AssignmentModel import Trainee_Assignment


@app.route('/')
@login_required
def admin():
    account = current_user.username
    return render_template('back-end/_index.html', account=account)


@app.route('/create_tables/')
def create_tables():
    db.create_all()
    db.session.add(User())
    db.session.add(Teacher())
    db.session.add(Trainee())
    db.session.add(Course())
    db.session.add(Class())
    db.session.add(Category())
    db.session.add(Assignment())
    db.session.add(Resources())
    db.session.add(Announcement())
    db.session.add(Trainee_Assignment())
    db.session.commit()

    return redirect('/login/')