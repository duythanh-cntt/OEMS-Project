from project import app, db
from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user
from project.models.CategoryModel import Category
from project.models.EntryModel import Entry
from project.models.UploadModel import Upload


@app.route('/admin/entry/')
@app.route('/admin/entry/<id>')
@login_required
def admin_entry(id=None):
    if id is not None and id != '' and int(id) > 0:
        if Entry.get_entry(id) is not None:
            entry = Entry.get_entry(id)
            page_title = 'Update entry'
        else:
            return redirect('/admin/list_entry/')
    else:
        entry = None
        page_title = 'Add new entry'
    cat_list = Category.get_category_list()
    return render_template('back-end/_entry-form.html', page_title=page_title, cat_list=cat_list, entry=entry, account=current_user.username)


@app.route('/admin/add_entry/', methods=['POST'])
@app.route('/admin/add_entry/<id>', methods=['POST'])
@login_required
def add_entry(id=None):
    category_id = int(request.form['category_id'])
    if category_id == 0:
        category_id = 1
    user_id = int(current_user.id)
    title = request.form['title']
    slug = request.form['slug']
    summary = request.form['summary']
    content = request.form['content']
    thumbnail = ''
    tags = request.form['tags']
    published = int(request.form['published'])
    image = Upload.upload_image()

    if id is not None and id != '' and int(id) > 0:
        entry = Entry.query.filter(Entry.id != id, Entry.slug == slug).first()
        if entry:
            flash('This slug has already taken.', 'error')
            return redirect('%s%s' % ('/admin/entry/', id))
        else:
            Entry.update_entry(id, category_id, user_id, title, slug, summary, content, thumbnail, image, tags, published)
            flash('Entry has been updated successfully.', 'success')
    else:
        db.session.add(Entry.insert_entry(category_id, user_id, title, slug, summary, content, thumbnail, image, tags, published))
        flash('Entry has been created successfully.', 'success')
    db.session.commit()
    return redirect('/admin/list_entry/')


@app.route('/admin/delete_entry/', methods=['GET'])
@login_required
def delete_entry():
    id = request.args.get('id')
    if id is not None and id != '' and int(id) > 0:
        if Entry.get_entry(id) is not None and Entry.get_entry(id).user_id == current_user.id:
            db.session.delete(Entry.get_entry(id))
            db.session.commit()
    return redirect('/admin/list_entry/')


@app.route('/admin/list_entry/')
@login_required
def list_entry():
    page_title = 'List of entries'
    entry_list = Entry.get_entry_by_user()
    return render_template('back-end/_entry-table.html', page_title=page_title, entry_list=entry_list, account=current_user.username)