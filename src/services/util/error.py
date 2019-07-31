class Error(Exception):
    pass


class CommandError(Error):
    def __init__(self, message):
        self.message = message

class ItemExistedError(Error):
    def __init__(self):
        self.message = "Item already exists!"

class OrderExistedError(Error):
    def __init__(self):
        self.message = "Previous active order exists!"

class OrderNotExistedError(Error):
    def __init__(self):
        self.message = "No active order exist yet!"

class BadRequestError(Error):
    def __init__(self):
        self.message = "Invalid command type!" 