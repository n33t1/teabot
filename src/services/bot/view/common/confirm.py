class Confirm:
    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text
        if "ok_text" in kwargs:
            self.ok_text = kwargs.get("ok_text")
        if "dismiss_text" in kwargs:
            self.dismiss_text = kwargs.get("dismiss_text")
