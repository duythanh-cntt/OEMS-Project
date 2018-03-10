from project import app, db
from hashlib import md5
import datetime
from flask import render_template, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from project.models.RoleModel import Role
from project.models.UserModel import User
from project.codes.Common import Common

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    if (username):
        return User.query.get(username)
    else:
        return None


@app.route('/login/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username.lower(), password=md5(password.encode()).hexdigest()).first()
        if user:
            login_user(user=user)
            user.login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.session.commit()
        else:
            message = 'Wrong username or password'

    # Kiem tra quyen
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('back-end/login.html', message=message)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/login/')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        authcode = Common.md5(username + password + email)
        activated = 1
        firstname = lastname = address = nationality = introduction = None

        # Kiem tra trung username va email
        if User.exists_username(username):
            message = 'Username "' + username + '" is already taken'
            return render_template('back-end/login.html', message=message)
        elif User.exists_email(email):
            message = 'Email "' + email + '" is already taken'
            return render_template('back-end/login.html', message=message)
        else:
            db.session.add(User.insert_user(role, username, password, firstname, lastname, email, address, nationality, introduction, authcode, activated))
            db.session.commit()
    return redirect('/login/')


@app.route('/user/')
@login_required
def admin_user():
    account = current_user.username
    page_title = 'List of users'
    user_list = User.get_all_users()
    return render_template('back-end/_user.html', page_title=page_title, user_list=user_list, account=account)


@app.route('/profile/')
@login_required
def profile():
    if current_user.firstname is not None and current_user.firstname != '' and current_user.lastname is not None and current_user.lastname != '':
        account = current_user.firstname + ' ' + current_user.lastname
    else: account = current_user.username
    avatar = current_user.avatar
    page_title = 'User profile'
    return render_template('back-end/_profile.html', page_title=page_title, account=account, avatar=avatar, current_user=current_user)


@app.route('/user/create-user/')
@app.route('/user/create-user/<user_id>')
@login_required
def create_user(user_id=None):
    account = current_user.username
    roles = Role.get_all_role()
    page_title = 'Create user'

    if user_id is not None and user_id != '' and int(user_id) > 0:
        if User.get_user(user_id) is not None:
            user = User.get_user(user_id)
            user.password = ''
            page_title = 'Update user'
        else:
            user = ''
            # redirect('/user/')
    else:
        user = ''
    return render_template('back-end/_user-create-update.html', page_title=page_title, roles=roles, account=account, user=user)


@app.route('/user/add-user/', methods=['POST'])
@app.route('/user/add-user/<user_id>', methods=['POST'])
@login_required
def add_user(user_id=None):
    username = Common.get_value_from_request_form_by_key(request, 'username')
    password = Common.get_value_from_request_form_by_key(request, 'password')
    email = Common.get_value_from_request_form_by_key(request, 'email')
    role_id = Common.get_value_from_request_form_by_key(request, 'role_id')
    introduction = Common.get_value_from_request_form_by_key(request, 'introduction')
    firstname = Common.get_value_from_request_form_by_key(request, 'firstname')
    lastname = Common.get_value_from_request_form_by_key(request, 'lastname')
    address = Common.get_value_from_request_form_by_key(request, 'address')
    nationality = Common.get_value_from_request_form_by_key(request, 'nationality')

    authcode = ''
    activated = 1

    if user_id is not None and user_id != '' and int(user_id) > 0:
        user = User.query.filter(User.id == user_id).first()
        if user:
            User.update_user(role_id, user_id, username, password, firstname, lastname, email, address, nationality, introduction, authcode, activated)
            flash('User has been updated successfully.', 'success')
    else:
        db.session.add(User.insert_user(role_id, username, password, firstname, lastname, email, address, nationality, introduction, authcode, activated))
        flash('User has been created successfully.', 'success')
    db.session.commit()
    return redirect('/user/')


@app.route('/delete_user/', methods=['GET'])
@login_required
def delete_user():
    user_id = request.args.get('id')
    if user_id is not None and user_id != '' and int(user_id) > 0:
        if User.get_user(user_id) is not None:
            # Nên kiểm tra quan hệ 1 - n trước khi xóa

            db.session.delete(User.get_user(user_id))
            db.session.commit()
    return redirect('/admin/user/')

