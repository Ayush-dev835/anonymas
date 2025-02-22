from bson.objectid import ObjectId

class RefreshToken:
    def __init__(self, refresh_token: str, user_id: ObjectId):
        self.refresh_token = refresh_token
        self.user_id = user_id
    
    def serialize(self):
        return {
            "refresh_token": self.refresh_token,
            "user_id": self.user_id
        }
