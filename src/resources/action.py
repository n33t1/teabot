from flask_restful import Resource
from flask import request, make_response
import json

# from controller.bot import Bot
from config import slack_client
# from view.userEditDialog import UserEditDialog
# from view.config import ChannelConfigDialog

# bot = Bot()

COFFEE_ORDERS = {}


class Action(Resource):
    def post(self):
        return make_response("", 200)
        # message_action = json.loads(request.form["payload"])
        # user_id = message_action["user"]["id"]
        # channel_id = message_action["channel"]["id"]

        # if message_action["type"] == "interactive_message":
        #     action_name = message_action["actions"][0]["name"]
        #     action_value = message_action["actions"][0]["value"]
        #     ts = message_action["message_ts"]

        #     if action_name == "channel_config":
        #         if action_value == "edit_config":
        #             open_dialog = slack_client.api_call(
        #                 "dialog.open",
        #                 trigger_id=message_action["trigger_id"],
        #                 dialog=ChannelConfigDialog(
        #                     channel_id).get_formatted_message())
        #     elif action_name == "user_item":
        #         info = {
        #             "flavor": "a",
        #             "topping": "aaa",
        #             "ice": "30",
        #             "sugar": "30",
        #             "note": "fff",
        #             "count": 1
        #         }

        #         error, added_items = bot.add_item(channel_id, user_id, info)
        #         print("error: ", error)
        #         print("added_items: ", added_items)
        #         if error:
        #             slack_client.api_call(
        #                 "chat.postEphemeral",
        #                 channel=channel_id,
        #                 user=user_id,
        #                 ts=ts,
        #                 text="Item existed already! Do you want to add more?",
        #                 attachments=[])
        #         else:
        #             slack_client.api_call("chat.postEphemeral",
        #                                   channel=channel_id,
        #                                   user=user_id,
        #                                   ts=ts,
        #                                   text=":pencil: Taking your order...",
        #                                   attachments=[])

        #         # if action == "edit":
        #         #     open_dialog = slack_client.api_call(
        #         #         "dialog.open",
        #         #         trigger_id=message_action["trigger_id"],
        #         #         dialog=UserEditDialog(user_id).get_formatted_message())
        #         # elif action == "view":
        #         #     open_dialog = slack_client.api_call(
        #         #         "dialog.open",
        #         #         trigger_id=message_action["trigger_id"],
        #         #         dialog=UserEditDialog(user_id).get_formatted_message())

        #     # # Show the ordering dialog to the user
        #     # open_dialog = slack_client.api_call(
        #     #     "dialog.open",
        #     #     trigger_id=message_action["trigger_id"],
        #     #     dialog=UserEditDialog(user_id).get_formatted_message())

        #     # Update the message to show that we're in the process of taking their order
        #     # TODO: only current user can see it

        # elif message_action["type"] == "dialog_submission":

        #     ts = message_action["action_ts"]
        #     print(message_action["submission"])
        #     # slack_client.api_call(
        #     #     "chat.update",
        #     #     channel=channel_id,
        #     #     ts=ts,
        #     #     text=":white_check_mark: Order received!",
        #     #     attachments=[])

        # return make_response("", 200)
