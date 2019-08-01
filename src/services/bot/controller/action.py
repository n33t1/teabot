
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
            return None, item
        except Exception as e:
            logger.error("Unable to add item for user %s in channel %s", user_id, channel_id, exc_info=True)
            return e, None
        
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

    def handle_view_items(self, slack_event):
        pass
        #     open_dialog = slack_client.api_call(
        #         "dialog.open",
        #         trigger_id=message_action["trigger_id"],
        #         dialog=UserEditDialog(user_id).get_formatted_message())

    def handle_order_submit(self, slack_event):
        pass 

