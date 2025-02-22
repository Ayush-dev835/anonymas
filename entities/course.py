from bson.objectid import ObjectId
from configs_and_constants.constants import ContentTypes


class Course:
    def __init__(
        self,
        title: str,
        description: str,
        category_id: ObjectId,
        objectives: list[str],
        thumbnail_url: str,
        overview_url: str,
        hasChapters: bool,
        content_type: ContentTypes,
        content_url: str,
        price: int,
        author_id: ObjectId,
        is_published: bool = False,
    ):
        self.title = title
        self.description = description
        self.category_id = category_id
        self.objectives = objectives
        self.thumbnail_url = thumbnail_url
        self.overview_url = overview_url
        self.hasChapters = hasChapters

        self.price = price
        self.content_type = None if hasChapters else content_type
        self.content_url = None if hasChapters else content_url
        self.author_id = author_id
        self.is_published = is_published

    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "objectives": self.objectives,
            "thumbnail_url": self.thumbnail_url,
            "overview_url": self.overview_url,
            "hasChapters": self.hasChapters,
            "price": self.price,
            "content_type": self.content_type,
            "content_url": self.content_url,
            "author_id": self.author_id,
            "is_published": self.is_published,
            
        }

    @staticmethod
    def validate(data: dict):

        required_fields = [
            "title",
            "description",
            "objectives",
            "thumbnail_url",
            "overview_url",
            # "hasChapters",
            "category_id",
            "price",
            "content_type",
            "content_url",
            "author_id"
        ]

        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}", None
        return None, Course(
            data.get("title"),
            data.get("description"),
            data.get("category_id"),
            data.get("objectives"),
            data.get("thumbnail_url"),
            data.get("overview_url"),
            data.get("hasChapters"),
            data.get("content_type"),
            data.get("content_url"),
            data.get("price"),
            data.get("author_id"),
        )
