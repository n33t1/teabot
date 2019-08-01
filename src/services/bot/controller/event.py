
from config import slack_client

from src.services.tea.controller.channel import ChannelController
from src.services.tea.controller.order import OrderController

from ..view.message import Message
from ...util.error import OrderExistedError

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


class EventController:
    def __init__(self):
        self.slack_client = slack_client

    def handle_channel_order(self, slack_event):
        team_id, channel_id, user_id, text = slack_event["event"][
            "team"], slack_event["event"]["channel"], slack_event["event"][
            "user"], slack_event["event"]["text"]

        error, previous_order = self.find_previous_order(channel_id)

        # TODO: for test purpose only
        order_id = previous_order.id
        self.slack_client.api_call("chat.postEphemeral",
                                    channel=channel_id,
                                    user=user_id,
                                    text=Message.get_new_order_message(
                                        previous_order),
                                    attachments=Message.get_channel_configs_menu(order_id, user_id))
        
        self.slack_client.api_call("chat.postMessage",
                                    channel=channel_id,
                                    text=Message.get_new_order_message(
                                        previous_order),
                                    attachments=Message.get_user_items_menu(order_id, user_id))
        # if previous_order:
        #     # previous order did not finish
        #     # ask user if they want to continue with previous one
        #     self.slack_client.api_call("chat.postMessage",
        #                                channel=channel_id,
        #                                text=Message.get_previous_order_message(previous_order))
        # else:
        #     # start a new order
        #     new_order = self.start_order(channel_id)
        #     order_id = new_order.id

        #     self.slack_client.api_call("chat.postEphemeral",
        #                                channel=channel_id,
        #                                user=user_id,
        #                                text=Message.get_new_order_message(
        #                                    new_order),
        #                                attachments=Message.get_channel_configs_menu(order_id, user_id))
            
        #     self.slack_client.api_call("chat.postMessage",
        #                                channel=channel_id,
        #                                text=Message.get_new_order_message(
        #                                    new_order),
        #                                attachments=Message.get_channel_configs_menu(order_id, user_id))

    def __find_or_create_channel(self, channel_id):
        try:
            channel = ChannelController.find_channel(channel_id)
            if not channel:
                ChannelController.create_channel(channel_id)
            return True
        except Exception as e:
            logger.error("Cannot find channel id for channel %s.",
                         channel_id, exc_info=True)
            raise

    def find_previous_order(self, channel_id):
        try:
            _ = self.__find_or_create_channel(channel_id)
            return None, OrderController.find_active_order(channel_id)
        except Exception as e:
            logger.error("Cannot find previous order for channel %s.",
                         channel_id, exc_info=True)
            return e, None

    def start_order(self, channel_id):
        try:
            active_order = OrderController.find_active_order(channel_id)
            if active_order:
                raise OrderExistedError
            else:
                order = OrderController.create_order(channel_id)
                return None, order
        except Exception as e:
            return e, None
