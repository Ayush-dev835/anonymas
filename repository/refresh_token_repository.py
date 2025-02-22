from pymongo import MongoClient
from configs_and_constants.constants import CollectionNames
from entities.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: MongoClient):
        self.db = db
        self.collection_name = CollectionNames.refresh_tokens.value

    def create(self, token_data: RefreshToken):
        try:
            token = self.db.get_collection(self.collection_name).insert_one(
                token_data
            )
            token.update({"_id": str(token_data.inserted_id)})
            return None, token
        except Exception as error:
            return str(error), None
