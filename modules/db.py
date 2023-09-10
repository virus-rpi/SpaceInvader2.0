import pymongo


class DB:
    def __init__(self, db_name, collection_name, url, port, user, password):
        self.client = pymongo.MongoClient(
            f"mongodb://{user}:{password}@{url}:{port}/")
        self.db = self.client[db_name]
        self.collection_name = collection_name  # Store collection name as an instance attribute

    @property
    def collection(self):
        return self.db[self.collection_name]

    def insert(self, data):
        self.collection.insert_one(data)

    def multi_insert(self, data):
        self.collection.insert_many(data)

    def find(self, query):
        return self.collection.find(query)

    def update(self, query, data):
        self.collection.update_one(query, {"$set": data})

    def delete(self, query):
        self.collection.delete_one(query)

    def delete_all(self):
        self.collection.delete_many({})

    def close(self):
        self.client.close()
