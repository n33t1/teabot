from sqlalchemy import exc

from db import db
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
