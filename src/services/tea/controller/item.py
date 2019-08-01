from src.services.tea.model.order_user_items import OrderUserItemsModel
from src.services.tea.model.item import ItemModel

from ...util.error import ItemExistedError

import logging

logger = logging.getLogger(__name__)


class ItemController:
    __instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if ItemController.__instance is None:
            ItemController.__instance = object.__new__(cls)
        return ItemController.__instance

    @classmethod
    def query_user_items(cls, order_id, user_id):
        try:
            items = OrderUserItemsModel.find_user_items(order_id, user_id)
            return None, items
        except Exception as e:
            logger.error("Unable to query items for user %s with order %s.", user_id, order_id, exc_info=True)
            return e, None
    
    @classmethod
    def query_user_order_item(cls, order_id, user_id, item_name):
        try:
            items = OrderUserItemsModel.find_user_order_item(order_id, user_id, item_name)
            return items
        except Exception as e:
            logger.error("Unable to find item %s for user %s with order %s.", item_name, user_id, order_id, exc_info=True)
            raise
    
    @classmethod
    def _add_item(cls, item_name):
        try:
            item = cls._find_item(item_name)
            if not item:
                item = ItemModel(item_name)
                item.save_to_db()
            return item
        except Exception as e:
            logger.error("Unable to add item %s.", item_name, exc_info=True)
            raise

    @classmethod
    def _find_item(cls, item_name):
        try:
            item = ItemModel.find_item(item_name)
            return item
        except Exception as e:
            logger.error("Unable to find item %s.", item_name, exc_info=True)
            raise

    @classmethod
    def add_item(cls, order_id, user_id, item_info):
        try:
            item_name = item_info["flavor"]
            item = cls.query_user_order_item(order_id, user_id, item_name)
            if item:
                raise ItemExistedError
            else:
                item = cls._add_item(item_name)
                order_user_item = OrderUserItemsModel(order_id, user_id, item_info)
                order_user_item.save_to_db()
                return order_user_item.json()
        except Exception as e:
            logger.error("Unable to add item %s for user %s with order %s.", item_name, user_id, order_id, exc_info=True)
            raise

    @classmethod
    def delete_item(cls, order_id, user_id, item_name):
        try:
            item = cls._find_item(item_name)
            order_user_item = OrderUserItemsModel.find_user_order_item(order_id, user_id, item.name)
            order_user_item.delete_from_db()
            return None, True
        except Exception as e:
            logger.error("Unable to delete item %s for user %s with order %s.", item_name, user_id, order_id, exc_info=True)
            return e, None 
    
    @classmethod
    def update_item(cls, order_id, user_id, item_name, item_info):
        try:
            item = cls._find_item(item_name)
            order_user_item = OrderUserItemsModel.find_user_order_item(order_id, user_id, item.name)
            if not order_user_item:
                cls.add_item(order_id, user_id, item_name)
            else:
                OrderUserItemsModel.update_user_order_item(order_user_item, item_info)
                order_user_item.save_to_db()
            return None, order_user_item.json()
        except Exception as e:
            logger.error("Unable to u itpdateem %s for user %s with order %s.", item_name, user_id, order_id, exc_info=True)
            return e, None 