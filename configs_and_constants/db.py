from pymongo import MongoClient
from configs_and_constants.env import env
from configs_and_constants.constants import CollectionNames

class DB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        self.client = MongoClient(env.get("db_uri"))
        print("Connected with db", self.client)
        self.db = self.client[env.get("db_name")]
        print("Connected with db", self.db)

    def get_collection(self, collection_name: CollectionNames):
        try:
            return self.db.get_collection(collection_name), None
        except Exception as e:
            return e, None

    def close(self):
        self.client.close()
        print("Connection with database has been closed.")
