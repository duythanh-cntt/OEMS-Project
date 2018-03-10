from project import app, db
from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user
from project.models.CategoryModel import Category
from project.models.AnnouncementModel import Announcement
from project.models.UploadModel import Upload


@app.route('/announcement/')
@app.route('/announcement/<id>')
@login_required
def form_announcement(id=None):
    if id is not None and id != '' and int(id) > 0:
        if Announcement.get_announcement(id) is not None:
            announcement = Announcement.get_announcement(id)
            page_title = 'Update announcement'
        else:
            return redirect('/list_announcement/')
    else:
        announcement = None
        page_title = 'Add new announcement'
    cat_list = Category.get_category_list()
    return render_template('back-end/_announcement-form.html', page_title=page_title, cat_list=cat_list, announcement=announcement, account=current_user.username)


@app.route('/add_announcement/', methods=['POST'])
@app.route('/add_announcement/<id>', methods=['POST'])
@login_required
def add_announcement(id=None):
    user_id = int(current_user.id)
    category_id = int(request.form['category_id'])
    if category_id == 0:
        category_id = 1
    title = request.form['title']
    slug = request.form['slug']
    summary = request.form['summary']
    content = request.form['content']
    thumbnail = ''
    tags = request.form['tags']
    published = int(request.form['published'])
    image = Upload.upload_image()

    if id is not None and id != '' and int(id) > 0:
        announcement = Announcement.query.filter(Announcement.id != id, Announcement.slug == slug).first()
        if announcement:
            flash('This slug has already taken.', 'error')
            return redirect('%s%s' % ('/announcement/', id))
        else:
            Announcement.update_announcement(id, user_id, category_id, title, slug, summary, content, thumbnail, image, tags, published)
            flash('Entry has been updated successfully.', 'success')
    else:
        db.session.add(Announcement.insert_announcement(user_id, category_id, title, slug, summary, content, thumbnail, image, tags, published))
        flash('Entry has been created successfully.', 'success')
    db.session.commit()
    return redirect('/list_announcement/')


@app.route('/delete_announcement/', methods=['GET'])
@login_required
def delete_announcement():
    id = request.args.get('id')
    if id is not None and id != '' and int(id) > 0:
        if Announcement.get_announcement(id) is not None and Announcement.get_announcement(id).user_id == current_user.id:
            db.session.delete(Announcement.get_announcement(id))
            db.session.commit()
    return redirect('/list_announcement/')


@app.route('/list_announcement/')
@login_required
def list_announcement():
    page_title = 'List of announcements'
    announcement_list = Announcement.get_announcement_by_user_logged_in()
    return render_template('back-end/_announcement-table.html', page_title=page_title, announcement_list=announcement_list, account=current_user.username)