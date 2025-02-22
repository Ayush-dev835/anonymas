from configs_and_constants.constants import DiscountTypes 
from bson.objectid import ObjectId

class Discount:
    def __init__(
        self, course_ids: list[ObjectId], discount_type: DiscountTypes, discount_value: int,
    ):
        self.course_ids = list[course_ids]
        self.discount_type = discount_type
        self.discount_value = discount_value
