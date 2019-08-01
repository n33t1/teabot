from .menu import Menu
from .dialog import Dialog

from .common.button import Button
from .common.confirm import Confirm
from .common.text import Text
from .common.select import Select

from .color import MILK_TEA, BOBA


class Message:
    def __init__(self):
        pass

    @classmethod
    def get_previous_order_message(cls, previous_order):
        print("previous_order: ", previous_order)
        return "Previous order exist!"

    @classmethod
    def get_new_order_message(cls, new_order):
        print("new_order: ", new_order)
        return "//TODO: some message here"

    @classmethod
    def get_user_items_menu(cls, order_id, user_id):
        menu = Menu(
            MILK_TEA,
            "Edit, view or delete your items for current order",
            "{}_{}_user_items_menu".format(order_id, user_id),
            [
                Button("user_items", "Edit Item", "edit"),
                Button("user_items", "View Items", "view"),
                Button("user_items", "Cancel Items", "cancel",
                       style="danger",
                       confirm=Confirm(
                           "Are you sure?", "All your items for this order will be removed :(")
                       )
            ]
        )
        return [menu.json()]

    @classmethod
    def get_channel_configs_menu(cls, order_id, user_id):
        menu = Menu(
            BOBA,
            "Edit order configuration for everyone in the channel. Add order description, location, last call time and more!",
            "{}_{}_channel_configs_menu".format(order_id, user_id),
            [
                Button("channel_configs", "Edit Order", "edit"),
                Button("channel_configs", "View Summary", "view"),
                Button("channel_configs", "Cancel Order", "cancel",
                       style="danger",
                       confirm=Confirm(
                           "Are you sure?", "The order will be cancelled. Everyone's items will be gone :(")
                       )
            ]
        )
        return [menu.json()]

    @classmethod
    def get_user_items_edit_dialog(cls, order_id, user_id):
        dialog = Dialog(
            "Edit your items",
            "{}_{}_user_items_edit".format(order_id, user_id),
            [
                Text("Flavor", "flavor"),
                Text("Topping", "topping"),
                Select(
                    "Ice Amount",
                    "ice",
                    "How much ice do you want?",
                    [
                        ("0%", "0"),
                        ("30%", "30"),
                        ("50%", "50"),
                        ("70%", "70"),
                        ("100%", "100")
                    ]
                ),
                Select(
                    "Sugar Amount",
                    "sugar",
                    "How much sugar do you want?",
                    [
                        ("0%", "0"),
                        ("30%", "30"),
                        ("50%", "50"),
                        ("70%", "70"),
                        ("100%", "100")
                    ]
                ),
                Text("Count", "count", subtype="number", placeholder="How many do you want?"),
                Text("Note", "note"),
            ]
        )
        return dialog.json()
