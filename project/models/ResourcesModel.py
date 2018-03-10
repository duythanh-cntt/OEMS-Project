from project import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from project.models.UserModel import User
from project.models.CategoryModel import Category


class Resources(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    description = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    download = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=1)

    def __init__(self):
        self.user_id = 1
        self.category_id = 1
        self.name = 'Install Windows from a USB Flash Drive'
        self.link = 'https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/install-windows-from-a-usb-flash-drive'
        self.description = 'This topic covers how to create a bootable Windows installation USB drive from a Windows 10 install .iso or DVD.'
        self.tags = 'Install Windows, USB Flash'
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = 1

    @staticmethod
    def insert_resources(user_id, cat_id, name, link, description, tags, status):
        obj = Resources()
        obj.user_id = user_id
        obj.category_id = cat_id
        obj.name = name
        obj.link = link
        obj.description = description
        obj.tags = tags
        obj.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.status = status
        return obj

    @staticmethod
    def update_resources(id, user_id, cat_id, name, link, description, tags, status):
        obj = Resources.get_resources(id)
        obj.user_id = user_id
        obj.category_id = cat_id
        obj.name = name
        obj.link = link
        obj.description = description
        obj.tags = tags
        obj.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.status = status

    @staticmethod
    def get_resources(id, status=None):
        if status is None:
            result = Resources.query.filter(Resources.id == id).first()
        else:
            result = Resources.query.filter(Resources.id == id, Resources.status == status).first()
        if result:
            return result
        else:
            return None

    @staticmethod
    def get_resources_by_teacher(username, status=None):
        user = User.query.filter(username=username, role_id=2).first()
        if user:
            if status is None:
                return Resources.query.filter(Resources.user_id == user.id).order_by(Resources.id.desc()).all()
            else:
                return Resources.query.filter(Resources.user_id == user.id, Resources.status == status).order_by(Resources.id.desc()).all()
        else:
            return None

    @staticmethod
    def get_related_resources(id, cat_id):
        return Resources.query.filter(Resources.id != id, Resources.category_id == cat_id, Resources.status == 1).order_by(Resources.id.desc()).all()

    @staticmethod
    def get_resources_by_cat(cat_code, status=None):
        cat = Category.query.filter_by(code=cat_code).first()
        if cat:
            if status is None:
                return Resources.query.filter(Resources.category_id == cat.id).order_by(Resources.id.desc()).all()
            else:
                return Resources.query.filter(Resources.category_id == cat.id, Resources.status == status).order_by(Resources.id.desc()).all()
        else:
            return None

    @staticmethod
    def download_resources(id):
        result = Resources.get_resources(id)
        if result:
            result.download = result.download + 1
            db.session.commit()
