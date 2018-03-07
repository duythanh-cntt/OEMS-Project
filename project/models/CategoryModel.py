from project import db
from sqlalchemy import Column, Integer, String


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=False, default=0)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False, default=1)
    level = Column(Integer, nullable=False, default=1)
    entry = db.relationship('Entry', backref='category', lazy=True)

    def __init__(self):
        self.parent_id = 0
        self.code = 'general'
        self.name = 'General'
        self.order = 1
        self.level = 1

    # def __init__(self, pid, code, name, order, level):
    #     self.parent_id = pid
    #     self.code = code
    #     self.name = name
    #     self.order = order
    #     self.level = level

    @staticmethod
    def get_cat(cat_id):
        cat = Category.query.filter_by(id=cat_id).first()
        if cat:
            return cat
        else:
            return None

    @staticmethod
    def insert_cat(pid, code, name, order):
        obj = Category()
        obj.parent_id = pid
        obj.code = code
        obj.name = name
        obj.order = order
        obj.level = obj.set_level(pid)
        return obj

    @staticmethod
    def update_cat(cat_id, pid, code, name, order):
        obj = Category.get_cat(cat_id)
        obj.parent_id = pid
        obj.code = code
        obj.name = name
        obj.order = order
        obj.level = obj.set_level(pid)

    # @staticmethod
    def get_all_cat(self):
        return Category.query.filter().order_by(Category.order.asc()).all()

    @staticmethod
    def get_category_list(level=None):
        if level is None:
            return Category.query.filter_by(parent_id=0).order_by(Category.parent_id.asc(), Category.order.asc()).all()
        else:
            return Category.query.filter_by(level <= level).order_by(Category.parent_id.asc(), Category.order.asc()).all()

        # Sử dụng 1 trong 2 cách viết sau
        # return db.session.query(Category).filter_by(parent_id=0).order_by(Category.id.asc()).all()
        # return Category.query.filter_by(parent_id=0).order_by(Category.id.asc()).all()

    # Set level for the category which has parent_id = pid
    @staticmethod
    def set_level(pid):
        if pid is not None and pid != '' and int(pid) > 0:
            if Category.get_cat(pid) is not None:
                return Category.get_cat(pid).level + 1
            else:
                return 1
        else:
            return 1

    # Get children category of current category
    @staticmethod
    def get_one_child_list(cat_id):
        if cat_id is not None and cat_id != '' and int(cat_id) > 0:
            return Category.query.filter_by(parent_id=cat_id).order_by(Category.order.asc()).all()
        else:
            return None