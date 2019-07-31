from src.services.bot.view.common.confirm import Confirm

class Button:
    def __init__(self, name, text, value, **kwargs):
        self.type = "button"
        self.name = name
        self.text = text
        self.value = value
        if "style" in kwargs:
            self.style = kwargs.get("style")
        if "confirm" in kwargs:
            self.confirm = kwargs.get("confirm")
