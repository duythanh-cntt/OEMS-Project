from project import app, db
from flask import render_template, request, redirect, flash
from flask_login import current_user, login_required, LoginManager
from project.models.CourseModel import Course
from project.codes.Common import Common

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/course/')
@login_required
def get_all_course():
    account = current_user.username
    page_title = 'List of courses'
    course_list = Course.get_all_course()
    return render_template('back-end/course.html', page_title=page_title, course_list=course_list, account=account, current_user=current_user)


@app.route('/course/create-course/')
@app.route('/course/create-course/<course_id>')
@login_required
def create_course(course_id=None):
    account = current_user.username
    page_title = 'Create course'

    if course_id is not None and course_id != '' and int(course_id) > 0:
        if Course.get_course(course_id) is not None:
            course = Course.get_course(course_id)
        else:
            course = ''
            # redirect('/user/')
    else:
        course = ''
    return render_template('back-end/course-create-update.html', page_title=page_title, roles=current_user.role_id, account=account, course=course, current_user=current_user)


@app.route('/course/add-course/', methods=['POST'])
@app.route('/course/add-course/<course_id>', methods=['POST'])
@login_required
def add_course(course_id=None):
    name = Common.get_value_from_request_form_by_key(request, 'name')
    code = Common.get_value_from_request_form_by_key(request, 'code')

    print("add_course" + code)
    print("add_course" + name)

    if course_id is not None and course_id != '' and int(course_id) > 0:
        course = Course.query.filter(Course.id == course_id).first()
        if course:
            Course.update_course(course_id, code, name)
            flash('Course has been updated successfully.', 'success')
    else:
        db.session.add(Course.insert_course(code, name))
        flash('Course has been created successfully.', 'success')
    db.session.commit()
    return redirect('/course/')


@app.route('/delete_course/', methods=['GET'])
@login_required
def delete_course():
    course_id = request.args.get('id')
    print("DELETE Course: " + course_id)
    if course_id is not None and course_id != '' and int(course_id) > 0:
        course = Course.get_course(course_id)
        print("DELETE Course FULL: " + str(course.id))
        if course is not None:
            # Nên kiểm tra quan hệ 1 - n trước khi xóa
            db.session.delete(course)
            db.session.commit()
    return redirect('/course/')

