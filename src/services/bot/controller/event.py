from datetime import datetime

from config import slack_client

from src.services.tea.controller.channel import ChannelController
from src.services.tea.controller.order import OrderController

from ..view.message import Message
from ...util.error import OrderExistedError
from ...util.ordertime import Ordertime

import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


class EventController:
    def __init__(self):
        self.slack_client = slack_client

    def handle_channel_order(self, slack_event):
        team_id, channel_id, user_id, text = slack_event["event"][
            "team"], slack_event["event"]["channel"], slack_event["event"][
            "user"], slack_event["event"]["text"]

        error, previous_order = self.find_previous_order(channel_id)

        # TODO: for test purpose only
        order_id = previous_order.id
        # error, new_order = self.start_order(channel_id, user_id, resturant, timeout_at)
        # print("new order: ", new_order)

        # order_id = new_order.id
        self.slack_client.api_call("chat.postEphemeral",
                                    channel=channel_id,
                                    user=user_id,
                                    text=Message.get_new_order_message(
                                        previous_order),
                                    attachments=Message.get_channel_configs_menu(order_id, user_id))
        
        self.slack_client.api_call("chat.postMessage",
                                    channel=channel_id,
                                    text=Message.get_new_order_message(
                                        previous_order),
                                    attachments=Message.get_user_items_menu(order_id, user_id))
        # if previous_order:
        #     # previous order did not finish
        #     # ask user if they want to continue with previous one
        #     self.slack_client.api_call("chat.postMessage",
        #                                channel=channel_id,
        #                                text=Message.get_previous_order_message(previous_order))
        # else:
        #     # start a new order
        #     # TODO: remove hardcoded value here
        #     user_id, resturant, timeout_at = user_id, "Yifang", datetime.now()
        #     new_order = self.start_order(channel_id, user_id, resturant, timeout_at)
        #     order_id = new_order.id

        #     self.slack_client.api_call("chat.postEphemeral",
        #                                channel=channel_id,
        #                                user=user_id,
        #                                text=Message.get_new_order_message(
        #                                    new_order),
        #                                attachments=Message.get_channel_configs_menu(order_id, user_id))
            
        #     self.slack_client.api_call("chat.postMessage",
        #                                channel=channel_id,
        #                                text=Message.get_new_order_message(
        #                                    new_order),
        #                                attachments=Message.get_channel_configs_menu(order_id, user_id))

    def __find_or_create_channel(self, channel_id):
        try:
            channel = ChannelController.find_channel(channel_id)
            if not channel:
                ChannelController.create_channel(channel_id)
            return True
        except Exception as e:
            logger.error("Cannot find channel id for channel %s.",
                         channel_id, exc_info=True)
            raise

    def _parse_order_info(self, msg):
        # parse
        # "@teabot start a new order from Yifang. Close order in 3 hours."
        # "@teabot start a new order from Yifang. Close order @ 4:30."

        # You might need to use users.info(https://api.slack.com/methods/users.info) in order to get user timezone
        """Parse Order strings to a location name and a due time (as datetime object)
        Location name is matched by "*FROM_[Alphanumeric Location Name]." where underscore is a space.

        This method will attempt to parse order due time through two ways, interval and time, with the help
            of util.Ordertime class.

        Interval ("in 3 hours", "in 45 mins") is matched by "CLOSE_ORDER_IN_[num]_[unit]"
            Unit is one of '[h]our(s), [m]inute(s), [s]econd(s)', 'min(s)' and'sec(s)' are also matched.

        Time ("@ 2:45pm", "at 15:00") is matched by "CLOSE_ORDER_['@' or 'at']_[h:mm (am/pm)]".
            Current implementation will interpret "...at 3:00" as 3am. 24-hour time will be parsed correctly.
            Current implementation does not allow "...at 3".

        Timezone information is obtained by calling slack API client on the user ID. Since the parameter format
            is yet to be determined, an extra field might be needed if @msg is just the order string.
        Timezone information defaults to Eastern Time of United States ('America/New_York').

        :param msg: Order string to pass in; OR IN CASE OF Event object Extra Preprocessing is required.
        :return: location String, due_dttm datetime object
        """
        raw_location, raw_time = [s.strip() for s in msg.split(".") if s]
        location_pattern = re.compile(r".*from\s(?P<loc>[a-zA-Z0-9]+)\..*", re.I)
        location = location_pattern.match(raw_location)['loc']

        interval_pattern = re.compile(r".*Close\sorder\sin\s(?P<amt>[0-9]+)\s(?P<unit>[a-zA-Z]+s?)", re.I)
        time_pattern = re.compile(r".*Close\sorder\s((at)|@)\s(?P<time>[0-9:]+\s+([a|p]m)?)", re.I)
        interval_match = interval_pattern.match(raw_time)
        time_match = time_pattern.match(raw_time)

        # Where will the user_id come from?
        user_id = None
        user_info = self.slack_client.api_call('users.info', user=user_id).get('user', None)
        user_tz = user_info.get('tz', 'America/New_York') if user_info else 'America/New_York'

        due_dttm = None
        if interval_match:
            due_dttm = Ordertime.parse_interval(interval_match['amt'], interval_match['unit'], user_tz)
        elif time_match:
            due_dttm = Ordertime.parse_time(time_match['time'], user_tz)

        return location, due_dttm


    def find_previous_order(self, channel_id):
        try:
            _ = self.__find_or_create_channel(channel_id)
            return None, OrderController.find_active_order(channel_id)
        except Exception as e:
            logger.error("Cannot find previous order for channel %s.",
                         channel_id, exc_info=True)
            return e, None

    def start_order(self, channel_id, user_id, resturant, timeout_at):
        try:
            active_order = OrderController.find_active_order(channel_id)
            if active_order:
                raise OrderExistedError
            else:
                order = OrderController.create_order(channel_id, user_id, resturant, timeout_at)
                return None, order
        except Exception as e:
            return e, None
