from project import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from flask_login import current_user
from project.models.CategoryModel import Category


class Entry(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False, default=1)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    summary = Column(String, nullable=True)
    content = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)
    image = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    likes = Column(Integer, nullable=False, default=0)
    hits = Column(Integer, nullable=False, default=0)
    published = Column(Integer, nullable=False, default=1)

    def __init__(self):
        self.category_id = 1
        self.user_id = 1
        self.title = 'The first post'
        self.slug = 'the-first-post'
        self.summary = 'Lang Co Resort - Lang Co Town - Thua Thien Hue Province'
        self.content = '<b>The difference between UTF-8 and Unicode?</b><br />If asked the question, “What is the difference between UTF-8 and Unicode?”, would you confidently reply with a short and precise answer? In these days of internationalization all developers should be able to do that. I suspect many of us do not understand these concepts as well as we should. If you feel you belong to this group, you should read this ultra short introduction to character sets and encodings.'
        self.thumbnail = ''
        self.image = 'https://nguyenduythanh.files.wordpress.com/2007/03/dsc_0081.jpg?w=500&h=333'
        self.tags = 'first post, about'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.likes = 1
        self.hits = 1
        self.published = 1

    @staticmethod
    def insert_entry(cat_id, uid, title, slug, summary, content, thumbnail, image, tags, published):
        obj = Entry()
        obj.category_id = cat_id
        obj.user_id = uid
        obj.title = title
        obj.slug = slug
        obj.summary = summary
        obj.content = content
        obj.thumbnail = thumbnail
        obj.image = image
        obj.tags = tags
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.likes = 0
        obj.hits = 0
        obj.published = published
        return obj

    @staticmethod
    def update_entry(id, cat_id, uid, title, slug, summary, content, thumbnail, image, tags, published):
        obj = Entry.get_entry(id)
        obj.category_id = cat_id
        obj.user_id = uid
        obj.title = title
        obj.slug = slug
        obj.summary = summary
        obj.content = content
        obj.thumbnail = thumbnail
        if image is not None:
            obj.image = image
        obj.tags = tags
        obj.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.published = published

    @staticmethod
    def get_entry(id, published=None):
        if published is None:
            entry = Entry.query.filter(Entry.id == id).first()
        else:
            entry = Entry.query.filter(Entry.id == id, Entry.published == published).first()
        if entry:
            return entry
        else:
            return None

    @staticmethod
    def get_entry_by_user():
        return Entry.query.filter_by(user_id=current_user.id).order_by(Entry.id.desc()).all()

    @staticmethod
    def get_related_entry(id, cat_id):
        return Entry.query.filter(Entry.id != id, Entry.category_id == cat_id, Entry.published == 1).order_by(Entry.id.desc()).all()

    @staticmethod
    def get_entry_by_cat(cat_code, published=None):
        cat = Category.query.filter_by(code=cat_code).first()
        if cat:
            if published is None:
                return Entry.query.filter(Entry.category_id == cat.id).order_by(Entry.id.desc()).all()
            else:
                return Entry.query.filter(Entry.category_id == cat.id, Entry.published == published).order_by(Entry.id.desc()).all()
        else:
            return None