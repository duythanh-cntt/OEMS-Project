from project import app, db
from hashlib import md5
import datetime
from flask import render_template, request, redirect
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from project.models.UserModel import User
from project.codes.Common import Common

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    if(username):
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


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = 'User'
        authcode = Common.md5(username + password + email)
        activated = 1

        # Kiem tra trung username va email
        if User.exists_username(username):
            message = 'Username "' + username + '" is already taken'
            return render_template('back-end/login.html', message=message)
        elif User.exists_email(email):
            message = 'Email "' + email + '" is already taken'
            return render_template('back-end/login.html', message=message)
        else:
            db.session.add(User.insert_user(username, password, email, role, authcode, activated))
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


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/login/')