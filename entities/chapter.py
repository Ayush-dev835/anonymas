from configs_and_constants.constants import ContentTypes
from bson.objectid import ObjectId


class Chapter:
    def __init__(
        self,
        title: str,
        # content_type: ContentTypes,
        content_url: str,
        description: str,
        course_id: ObjectId,
        # content_length: str,
    ):
        self.title = title
        # self.content_type = content_type
        self.content_url = content_url
        self.description = description
        self.course_id = course_id
        
        # self.content_length = content_length

    def serialize(self):
        return {
            "title": self.title,
            # "content_type": self.content_type,
            "content_url": self.content_url,
            "description": self.description,
            "course_id": self.course_id,
            
        }

    @staticmethod
    def validate(data: dict):

        required_fields = [
            "title",
            "description",
            "content_url",
            "course_id",
        ]
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}", None
        return None, Chapter(
            data.get("title"),
            data.get("description"),
            data.get("content_url"),
            data.get("course_id"),
        )
