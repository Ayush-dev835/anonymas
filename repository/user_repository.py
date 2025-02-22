from pymongo import MongoClient
from configs_and_constants.constants import CollectionNames
from entities.user import User


class UserRepository:
    def __init__(self, db: MongoClient):
        self.db = db

        self.collection_name = CollectionNames.users.value

    def create(self, user_data: User):
        try:
            user = self.db.get_collection(self.collection_name).insert_one(user_data)
            user_data.update({"_id": str(user.inserted_id)})
            return None, user_data
        except Exception as error:
            print("___db_error___", error)
            return str(error), None

    def find_by_fields(self, filters: dict):
        try:
            user = self.db.get_collection(self.collection_name).find_one(filters)
            if user:
                user["_id"] = str(user["_id"])
            return None, user
        except Exception as error:
            return str(error), None

    def save_refresh_token(self, refresh_token_entity):
        pass

    def find_all(self):
        try:
            query = [{"$addFields": {"_id": {"$toString": "$_id"}}}]
            users = self.db.get_collection(self.collection_name).aggregate(query)
            return None, list(users)

        except Exception as error:
            return str(error), None
