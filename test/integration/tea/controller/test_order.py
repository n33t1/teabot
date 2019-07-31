from src.services.tea.controller.item import ItemController
from test.base_test import BaseTest

class ItemTest(BaseTest):
    def test_create_channel(self):
        ItemController.create_channel(1)
        channel = ItemController.find_channel(1)
        self.assertIsNotNone(channel)
    