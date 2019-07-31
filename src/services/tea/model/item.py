from sqlalchemy import exc

from db import db, make_session_scope
from src.services.util.error import OrderExistedError

class ItemModel(db.Model):
    __tablename__ = "items"

    name = db.Column(db.String(80), primary_key=True)
    resturant = db.Column(db.String(80), nullable=True)

    orders = db.relationship("OrderModel", secondary="order_user_items")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Item ('{}')>" .format(self.__dict__)

    def json(self):
        return {"name": self.name, "resturant": self.resturant}

    @classmethod
    def find_item(cls, item_name):
        return cls.query.filter_by(name=item_name).first()

    def save_to_db(self):
        with make_session_scope(db.session) as session:
            db.session.add(self)

    def delete_from_db(self):
        with make_session_scope(db.session) as session:
            session.delete(self)