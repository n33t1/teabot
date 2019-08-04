from datetime import datetime

from src.services.tea.model.order import OrderModel
from src.services.tea.model.order_user_items import OrderUserItemsModel 

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)

class OrderController:
    __instance = None

    def __init__(self):
        pass
    
    def __new__(cls):
        if OrderController.__instance is None:
            OrderController.__instance = object.__new__(cls)
        return OrderController.__instance
    
    @classmethod
    def find_order_items(cls, channel_id):
        try:
            items = OrderUserItemsModel.find_order_items(channel_id)
            return [item.json() for item in items] if items else []
        except Exception as e:
            logger.error("Unable to find items for channel %s.", channel_id)
            raise

    @classmethod
    def find_active_order(cls, channel_id):
        try:
            active_order = OrderModel.find_active_order(channel_id)
            return active_order
        except Exception as e:
            logger.error("Unable to find active order for channel %s.", channel_id)
            raise
    
    @classmethod
    def create_order(cls, channel_id, user_id, resturant, timeout_at):
        try:
            order = OrderModel(channel_id, user_id, resturant, timeout_at)
            order.save_to_db()
            return order.json()
        except Exception as e:
            logger.error("Unable to create new order for channel %s.", channel_id, exc_info=True)
            raise
    
    @classmethod
    def deactivate_order(cls, channel_id):
        try:
            active_order = cls.find_active_order(channel_id)
            active_order.is_active = False
            active_order.save_to_db()
            return None, True
        except Exception as e:
            logger.error("Unable to deactivate order for channel %s.", channel_id, exc_info=True)
            return e, None
    
    @classmethod
    def finish_order(cls, channel_id):
        try:
            order = cls.find_active_order(channel_id)
            order.is_active = False
            order.is_finished = True
            order.finished_at = datetime.utcnow
            order.save_to_db()

            return None, order.json()
        except Exception as e:
            logger.error("Unable to finish order for channel %s.", channel_id, exc_info=True)
            return e, None
