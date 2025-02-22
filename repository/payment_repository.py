from pymongo import MongoClient

from configs_and_constants.constants import CollectionNames
from entities.purchased_course import PaymentDetail, PurchasedCourse


class PaymentRepository:
    def __init__(self, db: MongoClient):
        self.db = db
        self.collection_name = CollectionNames.payment.value
        self.collection_name = CollectionNames.purchased_courses.value

    def save_payment_detail(self, payment_detail: PaymentDetail):
        payment_data = {
            "order_id": payment_detail.order_id,
            "method": payment_detail.method,
            "date": payment_detail.date,
            "amount": payment_detail.amount,
            "transaction_id": payment_detail.transaction_id,
        }
        self.db[self.collection_name].insert_one(payment_data)

    def save_purchased_course(self, purchased_course: PurchasedCourse):
        purchased_data = {
            "course_id": purchased_course.course_id,
            "user_id": purchased_course.user_id,
            "hasDiscount": purchased_course.hasDiscount,
            "total_price": purchased_course.total_price,
            "actual_price": purchased_course.actual_price,
            "payment_detail": {
                "order_id": purchased_course.payment_detail.order_id,
                "method": purchased_course.payment_detail.method,
                "date": purchased_course.payment_detail.date,
                "amount": purchased_course.payment_detail.amount,
                "transaction_id": purchased_course.payment_detail.transaction_id,
            },
        }
        self.db[self.collection_name].insert_one(purchased_data)
