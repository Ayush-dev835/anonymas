from bson import ObjectId
from configs_and_constants.constants import CollectionNames
from pymongo import MongoClient


class CourseRepository:
    def __init__(self, db: MongoClient):
        self.db = db
        self.collection_name = CollectionNames.courses.value

        self.collection_name_for_learner = CollectionNames.purchased_courses.value

    def create(self, course_data: dict):
        print(course_data, "course_data")

        try:

            course = self.db.get_collection(self.collection_name).insert_one(
                course_data
            )
            course_data.update({"_id": str(course.inserted_id)})
            return None, course_data
        except Exception as error:
            return str(error), None

    def get_admin_courses(self, skip: int, limit: int):
        query = [
            {
                "$addFields": {
                    "_id": {"$toString": "$_id"},
                    "author_id": {"$toString": "$author_id"},
                    "category_id": {"$toString": "$category_id"},
                }
            },
            {"$skip": skip},
            {"$limit": limit},
        ]

        try:
            courses = list(
                self.db.get_collection(self.collection_name).aggregate(query)
            )
            return None, courses
        except Exception as error:
            return str(error), None

    def get_mentor_courses(self, author_id: str, skip: int, limit: int):
        query = [
            {"$match": {"author_id": ObjectId(author_id)}},
            {
                "$addFields": {
                    "_id": {"$toString": "$_id"},
                    "author_id": {"$toString": "$author_id"},
                    "category_id": {"$toString": "$category_id"},
                }
            },
            {"$skip": skip},
            {"$limit": limit},
        ]
        try:
            courses = list(
                self.db.get_collection(self.collection_name).aggregate(query)
            )
            return None, courses
        except Exception as error:
            return str(error), None

    def get_learner_courses(self, user_id: str, skip: int, limit: int):
        query = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {
                "$lookup": {
                    "from": self.collection_name,
                    "localField": "course_id",
                    "foreignField": "_id",
                    "as": "course_detail",
                    "pipeline": [
                        {
                            "$addFields": {
                                "_id": {"$toString": "$_id"},
                                "author_id": {"$toString": "$author_id"},
                                "category_id": {"$toString": "$category_id"},
                            }
                        }
                    ],
                }
            },
            {"$replaceRoot": {"newRoot": "$courseDetail"}},
            {"$skip": skip},
            {"$limit": limit},
        ]
        try:
            courses = list(
                self.db.get_collection(self.collection_name_for_learner).aggregate(
                    query
                )
            )
            return None, courses
        except Exception as error:
            return str(error), None

    def get_all_courses(self, skip, limit):
        query = [
            {
                "$match":{
                    "is_published":True
                }
            },
            {
                "$addFields": {
                    "_id": {"$toString": "$_id"},
                    "author_id": {"$toString": "$author_id"},
                    "category_id": {"$toString": "$category_id"},
                }
            },
            {"$skip": skip},
            {"$limit": limit},
        ]

        try:
            courses = list(
                self.db.get_collection(self.collection_name).aggregate(query)
            )
            return None, courses
        except Exception as error:
            return str(error), None

    def update_publish_status(self, course_id: str, is_published: bool):
        try:
            result = self.db.get_collection(self.collection_name).update_one(
                {"_id": ObjectId(course_id)}, {"$set": {"is_published": is_published}}
            )
            if result.matched_count == 0:
                return "Course not found.", None
            return None, {"course_id": course_id, "is_published": is_published}
        except Exception as error:
            return str(error), None

    def get_course_by_id(self, course_id: str):
        try:
            query = [
                {"$match": {"_id": ObjectId(course_id)}},
                {
                    "$addFields": {
                        "_id": {"$toString": "$_id"},
                        "author_id": {"$toString": "$author_id"},
                        "category_id": {"$toString": "$category_id"},
                    }
                },
            ]

            course = list(self.db.get_collection(self.collection_name).aggregate(query))
            if not course:
                return "Course not found.", None

            return None, course[0]
        except Exception as error:
            return str(error), None

    def get_courses_by_category(self, category_id: str, skip: int, limit: int):
        try:
            query = [
                {"$match": {"category_id": ObjectId(category_id)}},
                {
                    "$addFields": {
                        "_id": {"$toString": "$_id"},
                        "author_id": {"$toString": "$author_id"},
                        "category_id": {"$toString": "$category_id"},
                    }
                },
                {"$skip": skip},
                {"$limit": limit},
            ]
            courses = list(
                self.db.get_collection(self.collection_name).aggregate(query)
            )
            return None, courses
        except Exception as error:
            return str(error), None

    def delete(self, course_id=str):

        try:
            result = self.db.get_collection(self.collection_name).delete_one(
                {"_id": ObjectId(course_id)}
            )

            if result.deleted_count == 0:
                return "Course not found.", None
            return None, f"Course with ID {course_id} has been deleted."
        except Exception as error:
            return str(error), None
