from model.item import ItemModel
from test.base_test import BaseTest

class ItemTest(BaseTest):
    def test_crud_create_read_delete(self):
        with self.app_context():
            itm = ItemModel("0001", "U00000000", "Details of an order")
            self.assertListEqual(ItemModel.find_by_order_uuid_and_user_id(order_uuid = "1", user_id = "U00000000"), [])
            itm.save_to_db()
            self.assertEqual(len(ItemModel.find_by_order_uuid_and_user_id(order_uuid = "1", user_id = "U00000000")), 1)
            itm.delete_from_db()
            self.assertListEqual(ItemModel.find_by_order_uuid_and_user_id(order_uuid = "1", user_id = "U00000000"), [])

    def test_crud_create_read_delete_multi(self):
        with self.app_context():
            itm = ItemModel("2", "U00000001", "Details of an order 😂")
            self.assertListEqual(ItemModel.find_by_order_uuid_and_user_id(order_uuid = "2", user_id = "U00000001"), [])
            itm.save_to_db()
            self.assertEqual(len(ItemModel.find_by_order_uuid_and_user_id(order_uuid = "2", user_id = "U00000001")), 1)
            found_item = ItemModel.find_by_order_uuid_and_user_id(order_uuid = "2", user_id = "U00000001")[0]
            self.assertEqual(found_item.order_id, 2)
            self.assertEqual(found_item.user_id, "U00000001")
            self.assertEqual(found_item.details, "Details of an order 😂")
            itm.delete_from_db()
            self.assertListEqual(ItemModel.find_by_order_uuid_and_user_id(order_uuid = "2", user_id = "U00000001"), [])

    def test_crud_create_read_query_uuid_type(self):
        # Check if query method can handel uuid of both types
        with self.app_context():
            itm = ItemModel(3, "U00000002", "Details of an order")
            itm.save_to_db()
            found_item_str = ItemModel.find_by_order_uuid_and_user_id(order_uuid = "3", user_id = "U00000002")[0]
            found_item_int = ItemModel.find_by_order_uuid_and_user_id(order_uuid = 3, user_id = "U00000002")[0]
            self.assertEquals(found_item_int.order_id, found_item_str.order_id)

    def test_crud_create_read_multiple_json(self):
        with self.app_context():
            itm1 = ItemModel("2", "U00000001", "Details of an order 😂")
            itm2 = ItemModel(3, "U00000002", "Details of an order")
            # Field 'id' is assigned at write to the db
            itm1.save_to_db()
            self.assertEqual(itm1.id, 1)
            itm2.save_to_db()
            self.assertEqual(itm2.id, 2)
            found_itm2 = ItemModel.find_all_by_order_uuid(2)
            found_itm3 = ItemModel.find_all_by_order_uuid(3)
            # order_id is not written to json
            expected_json2 = {"id": 1, "user_id": "U00000001", "details": "Details of an order 😂"}
            expected_json3 = {"id": 2, "user_id": "U00000002", "details": "Details of an order"}
            self.assertEqual(len(found_itm2), 1)
            self.assertEqual(len(found_itm3), 1)
            self.assertDictEqual(found_itm2[0].json(), expected_json2)
            self.assertDictEqual(found_itm3[0].json(), expected_json3)


    def test_json_details_empty(self):
        with self.app_context():
            # Details field is empty string
            itm = ItemModel(4, "U00000003", "")
            jsonres = itm.json()
            self.assertEqual(jsonres['user_id'], "U00000003")
            self.assertEqual(jsonres['details'], "")
            self.assertEqual(len(jsonres), 3)

    def test_json_with_id(self):
        with self.app_context():
            itm = ItemModel(4, "U00000004", "Details of an order")
            itm.save_to_db()
            jsonres = itm.json()
            expected_json = {"id": 1, "user_id": "U00000004", "details": "Details of an order"}
            self.assertDictEqual(jsonres, expected_json)