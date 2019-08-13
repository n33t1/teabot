from collections import defaultdict
from datetime import datetime

from .menu import Menu
from .dialog import Dialog

from .common.button import Button
from .common.confirm import Confirm
from .common.text import Text
from .common.select import Select
from .block import Markdown, Image, Context, Context, Section, Accessory

from .color import MILK_TEA, BOBA


class Message:
    def __init__(self):
        pass

    @classmethod
    def get_previous_order_message(cls, previous_order):
        return "Previous order exist!"

    @classmethod
    def get_new_order_message(cls, new_order):
        order_info = new_order.json()
        return "*Ordering from {}! Place your order before {}* Started by <@{}>".format(order_info["from_resturant"], order_info["timeout_at"].strftime('%H:%M'), order_info["by_user"])

    @classmethod
    def get_user_items_menu(cls, order_id, user_id):
        menu = Menu(
            MILK_TEA,
            "Edit, view or delete your items for current order",
            "{}_{}_user_items_menu".format(order_id, user_id),
            [
                Button("user_items", "Add Item", "add"),
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
                Button("channel_configs", "Finish Order", "finish"),
                Button("channel_configs", "Cancel Order", "cancel",
                       style="danger",
                       confirm=Confirm(
                           "Are you sure?", "The order will be cancelled. Everyone's items will be gone :(")
                       )
            ]
        )
        return [menu.json()]


# @classmethod
    # def get_drink_details(cls, item_name, item_to_users_info, count, order_id):
    #     result = ["*{}*".format(item_name)]

    #     for (ice, sugar, topping), users_info in item_to_users_info.items():
    #         item_count = 0
    #         notes = []
    #         for (uid, note, item_id, count) in users_info:
    #             item_count += count
    #             notes.append("<@{}>: \"{}\"\n".format(uid, note))
    #             delete_button_value = "delete_{}_{}_{}".format(order_id, uid, item_id)
    #         a = "{}% ice, {}% sugar with {} ({})".format(ice, sugar, topping, item_count)
            
    #     # for (i, ((ice, sugar, topping), (uid, note, button_msg, count))) in enumerate(user_items):
    #     #     total_count =
    #     #     a = "{}% ice, {}% sugar with {} ({})".format(ice, sugar, topping)
    #     #     # if not note:
    #     #     #     plain_users.append(Markdown("<@{}>".format(uid)).json())
    #     #     # else:
    #     #     elements = "<@{}>: \"{}\"".format(uid, note)
    #     # # result.append(Context(plain_users).json())
    #     # return result

    @classmethod
    def get_drink_details(cls, item_name, item_to_user_info, count, order_id):
        user_items = list(item_to_user_info.items())
        result = []
        for (i, ((ice, sugar, topping), users_info)) in enumerate(user_items):
            
            item_count = 0
            notes = []
            for (uid, note, item_id, count) in users_info:
                item_count += count
                notes.append(Markdown("<@{}>: \"{}\"".format(uid, note)).json())
            
            if i == 0:
                item_detail = "*{}* ({})\n{}% ice, {}% sugar with {} ({})".format(item_name, count, ice, sugar, topping, item_count) 
            else:
                item_detail = "{}% ice, {}% sugar with {} ({})".format(ice, sugar, topping, item_count)
            
            result.append(Section(Markdown(item_detail).json(), accessory=Accessory(str(item_id)).json()).json())
            

            result.append(Context(notes).json())
        return result

    @classmethod
    def get_channel_order_result(cls, order_info, items, is_user_summary):
        if is_user_summary:
            result = [
                Section(Markdown("*Here is your order summary!*").json()).json()]
        else:
            result = [Section(Markdown("*Ordering from {}! Place your order before {}* Started by <@{}>".format(order_info["from_resturant"], order_info["timeout_at"].strftime('%H:%M'), order_info["by_user"])).json()).json()]
        item_name_to_details = defaultdict(lambda: defaultdict(list))
        item_name_to_count = defaultdict(lambda: 0)
        for item in items:
            item_name_to_count[item["item_name"]] += item["count"]
            item_name_to_details[item["item_name"]][(
                item["ice_percentage"], item["sugar_percentage"], item["topping"])].append([item["user_id"], item["note"], item["id"], item["count"]])

        for item_name, item_to_users_info in item_name_to_details.items():
            result += cls.get_drink_details(item_name,
                                            item_to_users_info, item_name_to_count[item_name], order_info["id"])
        return result

    @classmethod
    def get_user_items_edit_dialog(cls, order_id, user_id, item=None):
        if item:
            dialog = Dialog(
                "Edit your items",
                "{}_{}_user_items_update_{}".format(order_id, user_id, item["id"]),
                [
                    Text("Flavor", "flavor", value = item["item_name"]),
                    Text("Topping", "topping", value = item["topping"]),
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
                        ],
                        value = item["ice_percentage"]
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
                        ],
                        value = item["sugar_percentage"]
                    ),
                    Text("Count", "count", subtype="number",
                        placeholder="How many do you want?", value=item["count"]),
                    Text("Note", "note", value=item["note"]),
                ]
            )
        else:
            dialog = Dialog(
                "Edit your items",
                "{}_{}_user_items_add".format(order_id, user_id),
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
                    Text("Count", "count", subtype="number",
                        placeholder="How many do you want?"),
                    Text("Note", "note"),
                ]
            )
        return dialog.json()
