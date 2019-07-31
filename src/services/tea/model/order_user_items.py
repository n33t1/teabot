from datetime import datetime

from sqlalchemy import exc

from db import db
from src.services.util.error import OrderExistedError

class OrderUserItemsModel(db.Model):
    '''
         =========================
        |          Items          |
         -------------------------    
        |       <PK> id: int      |
        |       user_id: str      |
        |       details: str      |
        |     <FK>order: Order    |
         =========================
    '''
    __tablename__ = 'order_user_items'
    __table_args__ = (
        db.UniqueConstraint('order_id', 'user_id', 'item_name', 'topping', 'ice_percentage', 'sugar_percentage', 'note'),
    )

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False, default=1)
    is_valid = db.Column(db.Boolean, unique=False, default=True)

    user_id = db.Column(db.String(80), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_name = db.Column(db.String(80), db.ForeignKey('items.name'), nullable=False)

    order = db.relationship('OrderModel', backref=db.backref("order_user_items", cascade="all, delete-orphan"))
    items = db.relationship('ItemModel', backref=db.backref("order_user_items", cascade="all, delete-orphan"))

    topping = db.Column(db.String(80), nullable=False)
    ice_percentage = db.Column(db.Integer, nullable=False)
    sugar_percentage = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, order_id, user_id, item_info):
        print("item_info: ", item_info)
        self.order_id = order_id
        self.user_id = user_id
        self.item_name = item_info["flavor"]
        self.topping = item_info["topping"]
        self.ice_percentage = item_info["ice"]
        self.sugar_percentage = item_info["sugar"]
        self.count = item_info["count"]
        self.note = item_info["note"]

    def __repr__(self):
        return "<OrderUserItems ({})>".format(self.__dict__)

    def json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "item_name": self.item_name,
            "topping": self.topping,
            "ice_percentage": self.ice_percentage,
            "sugar_percentage": self.sugar_percentage,
            "note": self.note,
            "created_at": self.created_at
        }

    @classmethod
    def find_user_order_item(cls, order_id, user_id, item_name):
        return cls.query.filter_by(order_id=order_id).filter_by(user_id=user_id).filter_by(item_name=item_name).first()

    @classmethod
    def update_user_order_item(cls, item, item_info):
        self.topping = item_info["topping"]
        self.ice_percentage = item_info["ice"]
        self.sugar_percentage = item_info["sugar"]
        self.count = item_info["count"]
        self.note = item_info["note"]

    @classmethod
    def find_user_items(cls, order_id, user_id):
        return cls.query.filter_by(order_id=order_id).filter_by(user_id=user_id).all()

    @classmethod
    def find_order_items(cls, channel_id):
        return cls.query.filter_by(order_id=order_id).all()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
            raise OrderExistedError()
        except Exception as e:
            db.session().rollback()
            raise
        finally:
            db.session.close()

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session().rollback()
            raise
        finally:
            db.session.close()
