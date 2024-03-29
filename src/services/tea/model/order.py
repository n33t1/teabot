from datetime import datetime
from sqlalchemy import exc

from db import db, make_session_scope
from src.services.util.error import OrderExistedError


class OrderModel(db.Model):
    """
         =========================
        |       Orders            |
         -------------------------    
        |     <PK> id: int        |
        |    channel_id: str      |
        |    is_active: bool      |
        |  <FK>items: List<Item>  |
         =========================
    """

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, unique=False, default=True)
    is_finished = db.Column(db.Boolean, unique=False, default=False)

    by_user = db.Column(db.String(80), nullable=False)
    from_resturant = db.Column(db.String(80), nullable=False)
    timeout_at = db.Column(db.DateTime, nullable=False)


    channel_id = db.Column(db.String(80), db.ForeignKey('channel.channel_id'))
    channel = db.relationship('ChannelModel', back_populates="orders")

    items = db.relationship("ItemModel", secondary="order_user_items")

    def __init__(self, channel_id, user_id, resturant, timeout_at):
        self.channel_id = channel_id
        self.by_user = user_id
        self.from_resturant = resturant
        self.timeout_at = timeout_at

    def __repr__(self):
        return "<Order ('{}', channel_id: '{}')>" .format(self.id, self.channel_id)

    def json(self):
        return {
            "id": self.id,
            "is_active": self.is_active,
            "is_finished": self.is_finished,
            "created_at": self.created_at,
            "finished_at": self.finished_at,
            "channel_id": self.channel_id,
            "by_user": self.by_user,
            "from_resturant": self.from_resturant,
            "timeout_at": self.timeout_at
        }

    @classmethod
    def find_active_order(cls, channel_id):
        return cls.query.filter_by(channel_id=channel_id).filter_by(is_active=True).first()
    
    def save_to_db(self):
        with make_session_scope(db.session) as session:
            db.session.add(self)

    def delete_from_db(self):
        with make_session_scope(db.session) as session:
            session.delete(self)
