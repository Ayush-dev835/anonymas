from enum import Enum


class Roles(Enum):
    admin = "admin"
    operational_team = "operational_team"
    mentor = "mentor"
    learner = "learner"


class ContentTypes(Enum):
    video = "video"


class DiscountTypes(Enum):
    percentage = "percentage"
    flat = "flat"


class CollectionNames(Enum):
    roles = "roles"
    users = "users"
    courses = "courses"
    discounts = "discounts"
    chapters = "chapters"
    refresh_tokens = "refresh_tokens"
    watch_trackings = "watch_trackings"
    purchased_courses = "purchased_courses"
    payment = "payment"

    categories = "categories"
