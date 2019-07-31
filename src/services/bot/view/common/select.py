class Select:
    def __init__(self, label, name, placeholder, options):
        self.type = "select"
        self.label = label 
        self.name = name
        self.placeholder = placeholder
        self.options = self.get_options(options)
    
    def get_options(self, options):
        result = []
        for label, value in options:
            result.append({
                            "label": label,
                            "value": value
                        })
        return result
