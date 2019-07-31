from flask_restful import Resource
from flask import request, make_response
import json


from src.services.bot.controller.event import EventController

event_bot = EventController()

class Event(Resource):
    def post(self):
        slack_event = json.loads(request.data)

        # Verification handshake
        if "challenge" in slack_event:
            return make_response(
                slack_event["challenge"], 200, {
                    "content_type": "application/json"}
            )

        if "event" in slack_event:
            event_type = slack_event["event"]["type"]
            if event_type == "app_mention":
                event_bot.handle_channel_order(slack_event)
                return make_response("", 200)

        return make_response("Invalid event type!", 404, {"X-Slack-No-Retry": 1})
