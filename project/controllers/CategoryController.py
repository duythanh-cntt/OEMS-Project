from project import app, db
from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user
from project.models.CategoryModel import Category


@app.route('/admin/category/')
@app.route('/admin/category/<cat_id>')
@login_required
def admin_category(cat_id=None):
    account = current_user.username
    page_title = 'Category'
    cat_list = Category.get_category_list()

    # Get category to edit
    if cat_id is not None and cat_id != '' and int(cat_id) > 0:
        if Category.get_cat(cat_id) is not None:
            cat = Category.get_cat(cat_id)
        else:
            cat = ''
    else:
        cat = ''
    return render_template('back-end/_category.html', page_title=page_title, cat_list=cat_list, cat=cat, account=account)


#
# @app.route('/admin/add_category1', methods=['POST'])
# @login_required
# def add_category1():
#     parent_id = request.form['parent_id']
#     code = request.form['code']
#     name = request.form['name']
#     order = request.form['order']
#     cat = Category(parent_id, code, name, order)
#     db.session.add(cat)
#     db.session.commit()
#     return redirect('/admin/category')


@app.route('/admin/add_category/', methods=['POST'])
@app.route('/admin/add_category/<cat_id>', methods=['POST'])
@login_required
def add_category(cat_id=None):
    parent_id = request.form['parent_id']
    code = request.form['code']
    name = request.form['name']
    order = request.form['order']

    if cat_id is not None and cat_id != '' and int(cat_id) > 0:
        cat = Category.query.filter(Category.id != cat_id, Category.code == code).first()
        if cat:
            flash('This category code has already taken.', 'error')
            return redirect('%s%s' % ('/admin/category/', cat_id))
        else:
            Category.update_cat(cat_id, parent_id, code, name, order)
            flash('Category has been updated successfully.', 'success')
    else:
        db.session.add(Category.insert_cat(parent_id, code, name, order))
        flash('Category has been created successfully.', 'success')
    db.session.commit()
    return redirect('/admin/category/')


@app.route('/admin/delete_category/', methods=['GET'])
@login_required
def delete_category():
    cat_id = request.args.get('cat_id')
    if cat_id is not None and cat_id != '' and int(cat_id) > 1:
        if Category.get_cat(cat_id) is not None:
            db.session.delete(Category.get_cat(cat_id))
            db.session.commit()
    return redirect('/admin/category/')


@app.route('/test')
def testing():
    # return Category.get_cat(1).name
    return str(current_user.id)
