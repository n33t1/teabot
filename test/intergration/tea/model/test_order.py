from model.order import OrderModel
from test.base_test import BaseTest
import sqlite3

class OrderTest(BaseTest):
    def test_crud_create_read_delete_one(self):
        with self.app_context():
            query_res = OrderModel.find_by_channel_id("")
            self.assertIsNone(query_res)
            ord = OrderModel("", "")
            ord.save_to_db()
            query_res = OrderModel.find_by_channel_id("")
            self.assertEqual(query_res.channel_uuid, "")
            self.assertEqual(query_res.channel_id, "")
            self.assertEqual(query_res.id, 1)
            self.assertEqual(ord.id, 1)
            ord.delete_from_db()
            query_res = OrderModel.find_by_channel_id("")
            self.assertIsNone(query_res)
            self.assertEqual(ord.id, 1)

    def test_crud_create_read_multi(self):
        with self.app_context():
            ord1 = OrderModel(10, "C00000001")
            ord2 = OrderModel(20, "C00000002")
            self.assertIsNone(ord1.id)
            self.assertIsNone(ord2.id)
            ord1.save_to_db()
            self.assertEqual(ord1.id, 1)
            ord2.save_to_db()
            self.assertEqual(ord2.id, 2)
            query_res1 = OrderModel.find_by_channel_id("C00000001")
            query_res2 = OrderModel.find_by_channel_id("C00000002")
            self.assertEqual(query_res1.id, 1)
            self.assertEqual(query_res2.id, 2)

    def test_crud_create_query_by_latest(self):
        with self.app_context():
            # assuming channel_uuid~channel_id is one-to-one
            # querying for latest order, so result should be ord2 and ord3
            ord1 = OrderModel(10, "C00000001") # id 1
            ord2 = OrderModel(20, "C00000002") # id 4
            ord1.save_to_db()
            ord2.save_to_db()
            query_res1 = OrderModel.find_latest_order_uuid("C00000001")
            query_res2 = OrderModel.find_latest_order_uuid("C00000002")
            query_res_none = OrderModel.find_latest_order_uuid("C00000003")
            self.assertEqual(query_res1.id, 1)
            self.assertEqual(query_res2.id, 2)
            self.assertIsNone(query_res_none)

    def test_crud_cross_collision(self):
        # expecting an one-to-one relationship between channel_uuid 
        #   and channel_id
        with self.app_context():
            with self.assertRaises(Exception):
                ord12 = OrderModel(10, "C00000002")
                ord21 = OrderModel(20, "C00000001")
                ord11 = OrderModel(10, "C00000001")
                ord22 = OrderModel(20, "C00000002")
                ord12.save_to_db()
                ord21.save_to_db()
                ord11.save_to_db()
                ord22.save_to_db()

    def text_crud_none(self):
        with self.app_context():
            ord_none_1 = OrderModel(None, None)
            ord_none_2 = OrderModel(20, None)
            ord_none_3 = OrderModel(None, "C00000001")
            with self.assertRaises(Exception):
                ord_none_1.save_to_db()
            with self.assertRaises(Exception):
                ord_none_2.save_to_db()
            with self.assertRaises(Exception):
                ord_none_3.save_to_db()

    def test_json_content_basic(self):
        with self.app_context():
            ord1 = OrderModel(10, "C00000001")
            expected_json_id_none = {"id": None, "channel_id": "C00000001", "channel_uuid": 10} 
            self.assertDictEqual(ord1.json(), expected_json_id_none)
            ord1.save_to_db()
            expected_json = {"id": 1, "channel_id": "C00000001", "channel_uuid": 10}
            self.assertDictEqual(ord1.json(), expected_json)

