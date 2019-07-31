from sqlalchemy import exc

from db import db, make_session_scope
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
        with make_session_scope(db.session) as session:
            db.session.add(self)

    def delete_from_db(self):
        with make_session_scope(db.session) as session:
            session.delete(self)