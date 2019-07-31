from model.channel import ChannelModel
from test.base_test import BaseTest

class ChannelTest(BaseTest):
    def test_crud_create_read_delete_basic(self):
        with self.app_context():
            ch1 = ChannelModel("C00000001")
            self.assertIsNone(ChannelModel.find_channel_by_id("C00000001"))
            ch1.save_to_db()
            foundItem = ChannelModel.find_channel_by_id("C00000001")
            self.assertEqual(foundItem.channel_id, "C00000001")
            self.assertFalse(foundItem.order_activated)
            ch1.delete_from_db()
            self.assertIsNone(ChannelModel.find_channel_by_id("C00000001"))

    def test_json_before_db(self):
        with self.app_context():
            ch2 = ChannelModel("C00000002")
            json_before_db = ch2.json()
            self.assertEqual(json_before_db['channel_id'], "C00000002")
            self.assertFalse(json_before_db['order_activated'])


    def test_json_after_db(self):
        with self.app_context():
            ch2 = ChannelModel("C00000002")
            ch2.save_to_db()
            json_after_db = ch2.json()
            expected_json = {'id': 1, 'channel_id': "C00000002", 'order_activated': False}
            self.assertDictEqual(json_after_db, expected_json)

    def test_json_id_persistence_after_db_removal(self):
        with self.app_context():
            ch2 = ChannelModel("C00000002")
            ch2.save_to_db()
            found_channel = ChannelModel.find_channel_by_id("C00000002")
            self.assertEqual(found_channel.channel_id, "C00000002")
            ch2.delete_from_db()
            json_after_removal = ch2.json()
            expected_json = {'id': 1, 'channel_id': "C00000002", 'order_activated': False}
            self.assertDictEqual(json_after_removal, expected_json)