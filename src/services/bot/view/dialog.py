import json

class Dialog:
    def __init__(self, title, callback_id, elements, **kwargs):
        self.title = title
        self.callback_id = callback_id
        self.elements = elements
        self.submit_label = kwargs.get("submit_label", "Submit")
    
    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__)