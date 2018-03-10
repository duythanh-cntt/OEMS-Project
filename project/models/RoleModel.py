from project import db
from sqlalchemy import Column, Integer, String


class Role(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user = db.relationship('User', backref='role', lazy=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_role(role_id):
        role = Role.query.filter_by(id=role_id).first()
        if role:
            return role
        else:
            return None

    @staticmethod
    def insert_role(id, name):
        obj = Role()
        obj.id = id
        obj.name = name
        return obj

    @staticmethod
    def update_role(id, name):
        obj = Role.get_role(id)
        obj.name = name

    @staticmethod
    def get_all_role():
        return Role.query.filter().order_by(Role.id.asc()).all()