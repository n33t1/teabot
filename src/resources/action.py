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
        response_url = message_action["response_url"]
        
        action_bot.handle_actions(message_action, user_id, channel_id, response_url)
            
        return make_response("", 200)
