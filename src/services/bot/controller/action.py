
from config import slack_client

from src.services.tea.controller.order import OrderController
from src.services.tea.controller.item import ItemController

from ..view.message import Message
from ...util.error import OrderExistedError

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


class ActionController:
    def __init__(self):
        self.slack_client = slack_client

    def _add_item(self, channel_id, user_id, item_info):
        try:
            order = OrderController.find_active_order(channel_id)
            item = ItemController.add_item(order.id, user_id, item_info)
            print("new item:", item)
            return None, item
        except Exception as e:
            logger.error("Unable to add item for user %s in channel %s",
                         user_id, channel_id, exc_info=True)
            print("E: ", e)
            return e, None

    def query_items(self, order_id):
        pass

    def handle_edit_order(self, user_id, channel_id, action_value, trigger_id):
        self.slack_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog=Message.get_user_items_edit_dialog(channel_id, user_id))

    def handle_edit_items(self, user_id, channel_id, action_value, trigger_id):
        # TODO: check if order is still activate
        self.slack_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog=Message.get_user_items_edit_dialog(channel_id, user_id))

    def handle_submit_items(self, user_id, channel_id, item_info):
        # TODO: Update the message to show that we're in the process of taking their order
        error, added_item = self._add_item(channel_id, user_id, item_info)
        # TODO: fix issue if flavor same, cannot add element now
        print("error: ", error)
        print("added_item: ", added_item)
        # if error:
        #     slack_client.api_call(
        #         "chat.postEphemeral",
        #         channel=channel_id,
        #         user=user_id,
        #         ts=ts,
        #         text="Item existed already! Do you want to add more?",
        #         attachments=[])
        # else:
        #     slack_client.api_call("chat.postEphemeral",
        #                             channel=channel_id,
        #                             user=user_id,
        #                             ts=ts,
        #                             text=":pencil: Taking your order...",
        #                             attachments=[])

    def handle_view_items(self, channel_id, trigger_id):
        order = OrderController.find_active_order(channel_id)
        items = OrderController.find_order_items(order.id)
        # TODO: refactor this into chat.update
        self.slack_client.api_call("chat.postMessage",
                                   channel=channel_id,
                                   text="hi",
                                   blocks=Message.get_channel_order_result(order.json(), items))

    def handle_order_submit(self, slack_event):
        pass
