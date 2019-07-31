from .menu import Menu
from .common.button import Button
from .common.confirm import Confirm

from .color import MILK_TEA


class Message:
    def __init__(self):
        pass

    @classmethod
    def get_previous_order_message(self, previous_order):
        print("previous_order: ", previous_order)
        return "Previous order exist!"

    @classmethod
    def get_new_order_message(self, new_order):
        print("new_order: ", new_order)
        return "Starting Order"

    @classmethod
    def get_new_order_menu(self):
        menu = Menu(
            MILK_TEA,
            "Edit, view or delete your items for current order",
            "user_items",
            [
                Button("user_item", "Edit Item", "edit"),
                Button("user_item", "View Items", "view"),
                Button("user_item", "Cancel Items", "cancel",
                       style="danger",
                       confirm=Confirm(
                           "Are you sure?", "All your items for this order will be removed :(")
                       )
            ]
        )
        return [menu.json()]
