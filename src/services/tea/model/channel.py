from sqlalchemy import exc

from db import db
from src.services.util.error import OrderExistedError

class ChannelModel(db.Model):
    __tablename__ = "channel"

    channel_id = db.Column(db.String(80), primary_key=True)
    orders = db.relationship('OrderModel', back_populates="channel", lazy='dynamic')

    def __init__(self, channel_id):
        self.channel_id = channel_id

    def __repr__(self):
        return "<Channel ('{}')>".format(self.__dict__)

    def json(self):
        return {
            "id": self.channel_id,
            "orders": [order.json()for order in self.orders]
        }

    @classmethod
    def find_channel(cls, channel_id):
        return cls.query.filter_by(channel_id=channel_id).first()

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