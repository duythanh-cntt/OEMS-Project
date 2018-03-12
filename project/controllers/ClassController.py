from project import app, db
from flask import render_template, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from project.models.ClassModel import Class
from project.models.CourseModel import Course
from project.models.UserModel import User
from project.codes.Common import Common

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/class/')
@login_required
def get_all_class():
    account = current_user.username
    page_title = 'List of classes'
    class_list = Class.get_all_class()
    return render_template('back-end/class.html', page_title=page_title, class_list=class_list, account=account, current_user=current_user)


@app.route('/class/create-class/')
@app.route('/class/create-class/<class_id>')
@login_required
def create_class(class_id=None):
    account = current_user.username
    page_title = 'Create class'
    teachers = User.get_all_teacher()
    courses = Course.get_all_course()

    if class_id is not None and class_id != '' and int(class_id) > 0:
        if Class.get_class(class_id) is not None:
            xclass = Class.get_class(class_id)
        else:
            xclass = ''
            # redirect('/user/')
    else:
        xclass = ''
    return render_template('back-end/class-create-update.html', page_title=page_title, teachers=teachers, courses=courses, roles=current_user.role_id, account=account, xclass=xclass, current_user=current_user)


@app.route('/class/add-class/', methods=['POST'])
@app.route('/class/add-class/<class_id>', methods=['POST'])
@login_required
def add_class(class_id=None):
    name = Common.get_value_from_request_form_by_key(request, 'name')
    code = Common.get_value_from_request_form_by_key(request, 'code')
    course_id = Common.get_value_from_request_form_by_key(request, 'course_id')
    user_id = Common.get_value_from_request_form_by_key(request, 'user_id')
    status = Common.get_value_from_request_form_by_key(request, 'status')

    if class_id is not None and class_id != '' and int(class_id) > 0:
        xclass = Class.query.filter(Class.id == class_id).first()
        if xclass:
            Class.update_class(class_id, course_id, user_id, code, name, status)
            flash('Class has been updated successfully.', 'success')
    else:
        db.session.add(Class.insert_class(course_id, user_id, code, name, status))
        flash('Class has been created successfully.', 'success')
    db.session.commit()
    return redirect('/class/')


@app.route('/class/detail-class/<class_id>', methods=['GET'])
@login_required
def detail_class(class_id=None):
    xclass = ''
    page_title = 'Detail class'
    if class_id is not None and class_id != '' and int(class_id) > 0:
        xclass = Class.query.filter(Class.id == class_id).first()
    return render_template('back-end/class-detail.html', page_title=page_title, xclass=xclass, current_user=current_user)


@app.route('/delete_class/', methods=['GET'])
@login_required
def delete_class():
    class_id = request.args.get('id')
    print("DELETE class: " + class_id)
    if class_id is not None and class_id != '' and int(class_id) > 0:
        xclass = Class.get_class(class_id)
        print("DELETE Class FULL: " + str(xclass.id))
        if xclass is not None:
            # Nên kiểm tra quan hệ 1 - n trước khi xóa
            db.session.delete(xclass)
            db.session.commit()
    return redirect('/class/')

