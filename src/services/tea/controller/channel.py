from datetime import datetime

from src.services.tea.model.channel import ChannelModel

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


class ChannelController:
    __instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if ChannelController.__instance is None:
            ChannelController.__instance = object.__new__(cls)
        return ChannelController.__instance

    @classmethod
    def create_channel(cls, channel_id):
        try:
            channel = ChannelModel(channel_id)
            channel.save_to_db()
            return None, channel
        except Exception as e:
            logger.error("Unable to create order for channel  %s.",
                         channel_id, exc_info=True)
            return e, None

    @classmethod
    def find_channel(cls, channel_id):
        try:
            return ChannelModel.find_channel(channel_id)
        except Exception as e:
            logger.error("Unable to channel %s.", channel_id, exc_info=True)
            raise

    @classmethod
    def find_orders(cls, channel_id):
        try:
            channel = cls.find_channel(channel_id)
            if not channel:
                channel = cls.create_channel(channel_id)
            return None, channel.json()
        except Exception as e:
            logger.error("Unable to find orders for channel %s.",
                         channel_id, exc_info=True)
            return e, None
