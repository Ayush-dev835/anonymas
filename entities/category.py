from bson.objectid import ObjectId


class Category:
    def __init__(self, category: str):
        self.category = category
        

    def serialize(self):
        
        return {"category": self.category}

    @staticmethod
    def validate(data: dict):
        required_fields = ["category",]

        misssing_fields = [field for field in required_fields if not data.get(field)]
        if misssing_fields:
            return f"Missing required fields: {', '.join(misssing_fields)}", None
        return None, Category(data.get("category"))
