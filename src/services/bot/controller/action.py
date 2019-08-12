import re

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

    def _add_item(self, channel_id, user_id, item_info, order):
        try:
            item = ItemController.add_order_item(order.id, user_id, item_info)
            return None, item
        except Exception as e:
            logger.error("Unable to add item for user %s in channel %s",
                         user_id, channel_id, exc_info=True)
            return e, None
    
    def _update_item(self, channel_id, user_id, item_id, item_info, order):
        try:
            item = ItemController.update_order_item(order.id, user_id, item_id, item_info)
            return None, item
        except Exception as e:
            logger.error("Unable to add item for user %s in channel %s",
                         user_id, channel_id, exc_info=True)
            return e, None

    def query_items(self, order_id):
        pass

    def handle_edit_order(self, user_id, channel_id, action_value, trigger_id):
        self.slack_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog=Message.get_user_items_edit_dialog(channel_id, user_id))

    def handle_add_items(self, user_id, channel_id, action_value, trigger_id):
        # TODO: check if order is still activate
        self.slack_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog=Message.get_user_items_edit_dialog(channel_id, user_id))

    def handle_update_item(self, channel_id, user_id, item_id, trigger_id):
        order = OrderController.find_active_order(channel_id)
        item = ItemController.query_user_order_item(order.id, user_id, item_id).json()
        self.slack_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog=Message.get_user_items_edit_dialog(channel_id, user_id, item=item))

    def handle_submit_item(self, user_id, channel_id, item_info, order, dialog_submission_type, item_id=None):
        # TODO: Update the message to show that we're in the process of taking their order
        if dialog_submission_type == "add":
            error, added_item = self._add_item(channel_id, user_id, item_info, order)
            print("error, added_item: ", error, added_item)
            self.slack_client.api_call("chat.postEphemeral",
                                    channel=channel_id,
                                    text="has been added to your order!")
        elif dialog_submission_type == "update":
            error, added_item = self._update_item(channel_id, user_id, item_id, item_info, order)
            self.slack_client.api_call("chat.postEphemeral",
                                    channel=channel_id,
                                    text="has been updated to")

        # order = OrderController.find_active_order(channel_id)
        # items = OrderController.find_order_items(order.id)

        # self.slack_client.api_call("chat.postMessage",
        #                            channel=channel_id,
        #                            text="hi",
        #                            blocks=Message.get_channel_order_result(order.json(), items))

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

    def handle_view_items(self, channel_id, user_id, trigger_id, order):
        items = OrderController.find_order_items(order.id)
        # TODO: refactor this into chat.update
        self.slack_client.api_call("chat.postEphemeral",
                                   channel=channel_id,
                                   user=user_id,
                                   text="hi",
                                   blocks=Message.get_channel_order_result(order.json(), items))

    def handle_cancel_items(self, user_id, channel_id, order):
        ItemController.delete_items(order.id, user_id)
        self.slack_client.api_call("chat.postEphemeral",
                                   channel=channel_id,
                                   user=user_id,
                                   text="Your items has been deleted!")

    def handle_cancel_order(self, channel_id):
        OrderController.deactivate_order(channel_id)
        self.slack_client.api_call("chat.postMessage",
                                   channel=channel_id,
                                   text="This order has been canceled and is no longer activated :(")

    def handle_order_submit(self, slack_event):
        pass
    
    def handle_actions(self, message_action, user_id, channel_id):
        order = OrderController.find_active_order(channel_id)
        if order:
            if "callback_id" not in message_action:
                channel_id = message_action["channel"]["id"]
                user_id = message_action["user"]["id"]
                item_id = message_action["actions"][0]["value"]
                trigger_id = message_action["trigger_id"]

                if message_action["type"] == "block_actions":
                    self.handle_update_item(channel_id, user_id, item_id, trigger_id)
            else:
                if message_action["type"] == "interactive_message":
                    action_name = message_action["actions"][0]["name"]
                    action_value = message_action["actions"][0]["value"]
                    ts = message_action["message_ts"]
                    trigger_id = message_action["trigger_id"]

                    if action_name == "channel_configs":
                        if action_value == "view":
                            # self.handle_view_items(channel_id, user_id, trigger_id, order)
                            pass
                        elif action_value == "cancel":
                            self.handle_cancel_order(channel_id)
                    elif action_name == "user_items":
                        if action_value == "view":
                            self.handle_view_items(channel_id, user_id, trigger_id, order)
                        elif action_value == "add":
                            self.handle_add_items(user_id, channel_id, action_value, trigger_id)
                        elif action_value == "cancel":
                            self.handle_cancel_items(user_id, channel_id, order)

                elif message_action["type"] == "dialog_submission":
                    callback_id = message_action["callback_id"]
                    if callback_id.endswith("add"):
                        self.handle_submit_item(user_id, channel_id, message_action["submission"], order, "add")

                    res = re.match("^(.*?)_(.*?)_user_items_(\w+)_(\d+)$", callback_id)
                    if res:
                        order_id, user_id, dialog_submission_type, item_id = res.groups()
                        self.handle_submit_item(user_id, channel_id, message_action["submission"], order, dialog_submission_type, item_id)
                    else:
                        pass
        else:
            self.slack_client.api_call("chat.postEphemeral",
                                   channel=channel_id,
                                   user=user_id,
                                   text="This order is no longer active! Please start a new one!")
