from project import app, db
from flask import redirect, render_template, request
from flask_login import login_required, current_user
from project.models.UserModel import User
from project.models.CategoryModel import Category
from project.models.EntryModel import Entry


@app.route('/')
@login_required
def admin():
    account = current_user.username
    return render_template('back-end/_index.html', account=account)


@app.route('/create_tables/')
def create_tables():
    db.create_all()
    db.session.add(User())
    db.session.add(Category())
    db.session.add(Entry())
    db.session.commit()

    return redirect('/login/')