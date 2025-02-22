from bson.objectid import ObjectId

class PaymentDetail:
    def __init__(self, order_id: str, method: str, date: str, amount: int, transaction_id: str):
        self.order_id = order_id
        self.method = method
        self.date = date
        self.amount = amount
        self.transaction_id = transaction_id
        
class PurchasedCourse:
    def __init__(self, course_id: ObjectId, user_id: ObjectId, hasDiscount: bool, total_price : int, actual_price: int, payment_detail: PaymentDetail):
        self.course_id = course_id
        self.user_id = user_id
        self.hasDiscount = hasDiscount
        self.total_price = total_price 
        self.actual_price = actual_price
        self.payment_detail = payment_detail
        