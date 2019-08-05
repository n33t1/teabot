class Text:
    def __init__(self, label, name, **kwargs):
        self.type = "text"
        self.label = label 
        self.name = name
        if "value" in kwargs:
            self.value = kwargs.get("value")
        if "subtype" in kwargs:
            self.subtype = kwargs.get("subtype")
        if "placeholder" in kwargs:
            self.placeholder = kwargs.get("placeholder")
