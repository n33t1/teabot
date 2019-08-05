from flask_restful import Resource
from flask import request, make_response
import json


from src.services.bot.controller.action import ActionController

action_bot = ActionController()

class Action(Resource):
    def post(self):
        message_action = json.loads(request.form["payload"])
        user_id = message_action["user"]["id"]
        channel_id = message_action["channel"]["id"]
        if "callback_id" not in message_action:
            channel_id = message_action["channel"]["id"]
            user_id = message_action["user"]["id"]
            item_id = message_action["actions"][0]["value"]
            trigger_id = message_action["trigger_id"]
            print("channel_id, user_id, item_id: ", channel_id, user_id, item_id)
            action_bot.handle_update_item(channel_id, user_id, item_id, trigger_id)
        else:
            callback_id = message_action["callback_id"]

            if message_action["type"] == "interactive_message":
                action_name = message_action["actions"][0]["name"]
                action_value = message_action["actions"][0]["value"]
                ts = message_action["message_ts"]
                trigger_id = message_action["trigger_id"]

                if action_name == "channel_configs":
                    # TODO: refactor this
                    if callback_id == "1_UESL7NLH5_channel_configs_menu":
                        action_bot.handle_view_items(channel_id, trigger_id)
                elif action_name == "user_items":
                    action_bot.handle_edit_items(user_id, channel_id, action_value, trigger_id)

            elif message_action["type"] == "dialog_submission":
                action_bot.handle_submit_items(user_id, channel_id, message_action["submission"])
            
        return make_response("", 200)
