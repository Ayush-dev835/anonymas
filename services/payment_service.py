from repository.payment_repository import PaymentRepository
from datetime import datetime
from entities.purchased_course import PaymentDetail, PurchasedCourse
import razorpay


class PaymentService:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository
        self.razorpay_client = razorpay.Client(
            auth=("rzp_test_5h5fUvEFbx5xiW", "psEGLchUH7MxrHrpN695Uwqv")
        )

    def create_order(self, amount: int, currency: str = "INR"):
        order_data = {
            "amount": amount * 100,
            "currency": currency,
            "payment_capture": "1",
        }
        order = self.razorpay_client.order.create(data=order_data)
        return order["id"]

    def verify_payment(self, payment_id: str, signature: str):
        data = {
            "razorpay_order_id": payment_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
        try:
            self.razorpay_client.utility.verify_payment_signature(data)
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

    def process_payment_and_save(
        self,
        order_id: str,
        payment_id: str,
        signature: str,
        user_id: str,
        course_id: str,
        total_price: int,
        actual_price: int,
        has_discount: bool,
    ):
        if self.verify_payment(payment_id, signature):

            payment_detail = PaymentDetail(
                order_id=order_id,
                method="Razorpay",
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                amount=total_price,
                transaction_id=payment_id,
            )
            self.payment_repository.save_payment_detail(payment_detail)

            purchased_course = PurchasedCourse(
                course_id=ObjectId(course_id),
                user_id=ObjectId(user_id),
                hasDiscount=has_discount,
                total_price=total_price,
                actual_price=actual_price,
                payment_detail=payment_detail,
            )
            self.payment_repository.save_purchased_course(purchased_course)

            return True
        return False
