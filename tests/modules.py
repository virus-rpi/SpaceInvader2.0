import unittest
from unittest.mock import patch, PropertyMock
import pymongo
from modules.db import DB


class TestDB(unittest.TestCase):
    mock_db = None
    mock_client = None

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

    @patch.object(DB, 'collection', new_callable=PropertyMock)
    def test_insert(self, mock_collection):
        data = {"key1": "value1", "key2": "value2"}
        mock_collection.return_value.insert_one.return_value = None
        self.db.insert(data)
        mock_collection.return_value.insert_one.assert_called_once_with(data)

    @patch.object(DB, 'collection', new_callable=PropertyMock)
    def test_find(self, mock_collection):
        query = {"key1": "value1"}
        mock_collection.return_value.find.return_value = [{'key1': 'value1', 'key2': 'value2'}]
        result = list(self.db.find(query))
        mock_collection.return_value.find.assert_called_once_with(query)
        self.assertEqual(result, [{'key1': 'value1', 'key2': 'value2'}])

    @patch.object(DB, 'collection', new_callable=PropertyMock)
    def test_update(self, mock_collection):
        query = {"key1": "value1"}
        data = {"key2": "new_value"}
        mock_collection.return_value.update_one.return_value = None
        self.db.update(query, data)
        mock_collection.return_value.update_one.assert_called_once_with(query, {"$set": data})

    @patch.object(DB, 'collection', new_callable=PropertyMock)
    def test_delete(self, mock_collection):
        query = {"key1": "value1"}
        mock_collection.return_value.delete_one.return_value = None
        self.db.delete(query)
        mock_collection.return_value.delete_one.assert_called_once_with(query)

    @patch.object(DB, 'collection', new_callable=PropertyMock)
    def test_delete_all(self, mock_collection):
        mock_collection.return_value.delete_many.return_value = None
        self.db.delete_all()
        mock_collection.return_value.delete_many.assert_called_once_with({})

    @patch.object(DB, 'collection', new_callable=PropertyMock)
    def test_multi_insert(self, mock_collection):
        data = [{"key1": "value1", "key2": "value2"}, {"key1": "value3", "key2": "value4"}]
        mock_collection.return_value.insert_many.return_value = None
        self.db.multi_insert(data)
        mock_collection.return_value.insert_many.assert_called_once_with(data)


class TestServerReconnaissance(unittest.TestCase):  # TODO: Implement tests for ServerReconnaissance
    pass


if __name__ == '__main__':
    unittest.main()
