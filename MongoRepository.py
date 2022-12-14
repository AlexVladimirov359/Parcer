from pymongo import MongoClient
from Model import Model


class MongoRepository:
    def __init__(self, db, host='localhost', port=27017):
        client = MongoClient(host, port)
        self.db = client[db]

    #def save(self, record: Model):
    #    self.db[record.collection()] \
    #     .update({record.primary_key(): getattr(record, record.primary_key())}, record.__dict__, upsert=True)

    def insert(self, record: Model):
        self.db[record.collection()].insert(record.__dict__)

    def find_one(self, collection_name, params=None):
        return self.db[collection_name].find_one(params)

    def find_all(self, collection_name, params=None):
        return self.db[collection_name].find(params)

    def delete(self, collection_name, params=None):
        return self.db[collection_name].delete_many(params)