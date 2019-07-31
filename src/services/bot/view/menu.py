import json

class Menu:
    def __init__(self, color, text, callback_id, actions, **kwargs):
        self.fallback = kwargs.get("value", "Upgrade your Slack client to use messages like these.")
        self.color = color
        self.text = text
        self.callback_id = callback_id
        self.actions = actions
    
    def json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))