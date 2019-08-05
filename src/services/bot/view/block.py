import json


class Base:
    def json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Markdown(Base):
    def __init__(self, text):
        self.type = "mrkdwn"
        self.text = text


class Image(Base):
    def __init__(self, image_url, alt_text):
        self.type = "image"
        self.image_url = image_url
        self.alt_text = alt_text


class Context(Base):
    def __init__(self, elements):
        self.type = "context"
        self.elements = elements


class Accessory(Base):
    def __init__(self, value):
        self.type = "button"
        self.text = {
            "type": "plain_text",
            "text": "Update"
        }
        self.value = value


class Section(Base):
    def __init__(self, text, **kwargs):
        self.type = "section"
        self.text = text
        if "accessory" in kwargs:
            self.accessory = kwargs.get("accessory")
