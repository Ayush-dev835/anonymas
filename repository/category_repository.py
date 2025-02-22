from bson import ObjectId
from pymongo import MongoClient


from configs_and_constants.constants import CollectionNames


class CategoryRepository:
    def __init__(self, db: MongoClient):
        self.db = db
        self.collection_name_for_category = CollectionNames.categories.value

    def create_category(self, category_data: dict):
        try:
            
            category = self.db.get_collection(
                self.collection_name_for_category
            ).insert_one(category_data)
            category_data.update({"_id": str(category.inserted_id)})
            return None, category_data
        except Exception as error:
            return str(error), None

    def get_all_categories(self):
        try:
            query = [
                {
                    "$addFields": {
                        "_id": {"$toString": "$_id"},
                    }
                }
            ]
            categories = self.db.get_collection(
                self.collection_name_for_category
            ).aggregate(query)
            return None, list(categories)
        except Exception as error:
            return str(error), None
    
    
    #
    def delete_category(self, category_id):
        try:
            result = self.db.get_collection(self.collection_name_for_category).delete_one({"_id": ObjectId(category_id)})
            if result.deleted_count == 1:
                return None, "Category deleted successfully"
            else:
                return "Category not found", None
        except Exception as error:
            return str(error), None
