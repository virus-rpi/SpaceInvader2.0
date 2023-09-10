import unittest
from unittest.mock import patch
import pymongo
from modules.db import DB


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client = pymongo.MongoClient("mongodb://localhost:27017/")
        cls.mock_db = cls.mock_client["test_db"]
        cls.mock_collection = cls.mock_db["test_collection"]
        cls.db = DB("test_db", "test_collection", "localhost", 27017, "user", "password")

    @classmethod
    def tearDownClass(cls):
        # Close the mongomock client
        cls.mock_client.close()

    @patch.object(DB, 'collection', new_callable=unittest.mock.PropertyMock)
    def test_insert(self, mock_collection):
        data = {"key1": "value1", "key2": "value2"}
        mock_collection.insert_one.return_value = None
        self.db.insert(data)
        mock_collection.insert_one.assert_called_once_with(data)

    @patch.object(DB, 'collection', new_callable=unittest.mock.PropertyMock)
    def test_find(self, mock_collection):
        query = {"key1": "value1"}
        mock_collection.find.return_value = [{'key1': 'value1', 'key2': 'value2'}]
        result = list(self.db.find(query))
        mock_collection.find.assert_called_once_with(query)
        self.assertEqual(result, [{'key1': 'value1', 'key2': 'value2'}])

    @patch.object(DB, 'collection', new_callable=unittest.mock.PropertyMock)
    def test_update(self, mock_collection):
        query = {"key1": "value1"}
        data = {"key2": "new_value"}
        mock_collection.update_one.return_value = None
        self.db.update(query, data)
        mock_collection.update_one.assert_called_once_with(query, {"$set": data})

    @patch.object(DB, 'collection', new_callable=unittest.mock.PropertyMock)
    def test_delete(self, mock_collection):
        query = {"key1": "value1"}
        mock_collection.delete_one.return_value = None
        self.db.delete(query)
        mock_collection.delete_one.assert_called_once_with(query)

    @patch.object(DB, 'collection', new_callable=unittest.mock.PropertyMock)
    def test_delete_all(self, mock_collection):
        mock_collection.delete_many.return_value = None
        self.db.delete_all()
        mock_collection.delete_many.assert_called_once_with({})


if __name__ == '__main__':
    unittest.main()
