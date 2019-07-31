from src.services.tea.controller.channel import ChannelController
from test.base_test import BaseTest

class ChannelTest(BaseTest):
    def test_create_channel(self):
        with self.app_context():
            ChannelController.create_channel(1)
            channel = ChannelController.find_channel(1)
            self.assertIsNotNone(channel)
    