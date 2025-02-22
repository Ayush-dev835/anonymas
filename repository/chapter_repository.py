from pymongo import MongoClient

from configs_and_constants.constants import CollectionNames
from bson.objectid import ObjectId


class ChapterRepository:
    def __init__(self, db: MongoClient):
        self.db = db
        self.collection_name = CollectionNames.chapters.value

    def create_chapter(self, chapter_data: dict):
        try:
            chapter = self.db.get_collection(self.collection_name).insert_one(
                chapter_data
            )
            chapter_data.update({"_id": str(chapter.inserted_id)})
            return None, chapter_data
        except Exception as error:
            return str(error), None

    def get_chapter(self, course_id: str):
        try:
            query = [
                {"$match": {"course_id": ObjectId(course_id)}},
                {"$addFields": {"_id": {"$toString": "$_id"}}},
            ]

            chapter = self.db.get_collection(self.collection_name).aggregate(query)
            return None, chapter
        except Exception as error:
            return str(error), None

    #
    def delete_chapter(self, chapter_id):
        try:
            result = self.db.get_collection(self.collection_name).delete_one({"_id": ObjectId(chapter_id)})
            if result.deleted_count == 1:
                return None, "chapter deleted successfully"
            else:
                return "chapter not found", None
        except Exception as error:
            return str(error), None

