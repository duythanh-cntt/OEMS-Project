from project import app, db
from flask import redirect, render_template, request
from flask_login import login_required, current_user
from project.models.RoleModel import Role
from project.models.UserModel import User
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
    return render_template('back-end/_index.html', account=account, current_user=current_user)


@app.route('/create_tables/')
def create_tables():
    db.create_all()

    db.session.add(Role(1, 'Admin'))
    db.session.add(Role(2, 'Teacher'))
    db.session.add(Role(3, 'Trainee'))

    # Add admin
    db.session.add(User())
    db.session.commit()

    # Add teacher
    user = User()
    teacher = user.insert_user(2, 'ducdan', 'ducdan123', 'dan', 'duc', 'ho.ducdan@gmail.com', 'binh dinh', 'Viet Nam', 'RCBD', 'ducdanducdan123ho.ducdan@gmail.com', 1)
    db.session.add(teacher)
    db.session.commit()

    # Add trainee
    user = User()
    trainee = user.insert_user(3, 'baotruong', 'baotruong123', 'bao', 'truong' , 'baotruong@gmail.com', 'hue', 'Viet Nam', 'softworld', 'truongbaotruongbao123truongbao@gmail.com', 1)
    db.session.add(trainee)
    db.session.commit()

    db.session.add(Course())
    db.session.add(Class())
    db.session.add(Category())
    db.session.add(Assignment())
    db.session.add(Resources())
    db.session.add(Announcement())
    db.session.add(Trainee_Assignment())
    db.session.commit()

    return redirect('/login/')