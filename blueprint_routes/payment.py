# from flask import Blueprint, request, jsonify
# from configs_and_constants.db import DB
# from repository.payment_repository import PaymentRepository
# from services.payment_service import PaymentService

# payment = Blueprint("payment", __name__)

# payment_repository = PaymentRepository(DB().db)
# payment_service = PaymentService(payment_repository)


# @payment.route("/create_order", methods=["POST"])
# def create_payment_order():
#     try:

#         data = request.json
#         amount = data["amount"]


#         order_id = payment_service.create_order(amount)
#         return jsonify({"order_id": order_id})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @payment.route("/verify_payment", methods=["POST"])
# def verify_payment():
#     try:

#         data = request.json
#         payment_id = data["payment_id"]
#         signature = data["signature"]
#         order_id = data["order_id"]
#         user_id = data["user_id"]
#         course_id = data["course_id"]
#         total_price = data["total_price"]
#         actual_price = data["actual_price"]
#         has_discount = data["has_discount"]


#         if payment_service.process_payment_and_save(
#             order_id,
#             payment_id,
#             signature,
#             user_id,
#             course_id,
#             total_price,
#             actual_price,
#             has_discount,
#         ):
#             return jsonify(
#                 {"message": "Payment verified and course purchased successfully."}
#             )
#         else:
#             return jsonify({"message": "Payment verification failed."}), 400

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


from flask import Blueprint, request, jsonify
from configs_and_constants.db import DB
from repository.payment_repository import PaymentRepository
from services.payment_service import PaymentService
import razorpay
from datetime import datetime
from bson.objectid import ObjectId
import hmac
import hashlib

payment = Blueprint("payment", __name__)

payment_repository = PaymentRepository(DB().db)
payment_service = PaymentService(payment_repository)


WEBHOOK_SECRET = "your_razorpay_webhook_secret_key"


@payment.route("/create_order", methods=["POST"])
def create_payment_order():
    try:
        data = request.json
        amount = data["amount"]
        order_id = payment_service.create_order(amount)
        return jsonify({"order_id": order_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@payment.route("/verify_payment", methods=["POST"])
def verify_payment():
    try:
        data = request.json
        payment_id = data["payment_id"]
        signature = data["signature"]
        order_id = data["order_id"]
        user_id = data["user_id"]
        course_id = data["course_id"]
        total_price = data["total_price"]
        actual_price = data["actual_price"]
        has_discount = data["has_discount"]

        if payment_service.process_payment_and_save(
            order_id,
            payment_id,
            signature,
            user_id,
            course_id,
            total_price,
            actual_price,
            has_discount,
        ):
            return jsonify(
                {"message": "Payment verified and course purchased successfully."}
            )
        else:
            return jsonify({"message": "Payment verification failed."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@payment.route("/razorpay_webhook", methods=["POST"])
def razorpay_webhook():
    try:
        webhook_data = request.json
        signature = request.headers.get("X-Razorpay-Signature")

        if verify_webhook_signature(webhook_data, signature):

            event = webhook_data.get("event")
            payload = webhook_data.get("payload", {}).get("payment")

            if event == "payment.captured":
                payment_id = payload.get("id")
                order_id = payload.get("order_id")
                user_id = payload.get("notes", {}).get("user_id")
                course_id = payload.get("notes", {}).get("course_id")
                total_price = payload.get("amount") / 100
                actual_price = payload.get("amount") / 100
                has_discount = payload.get("notes", {}).get("has_discount")

                if payment_service.process_payment_and_save(
                    order_id,
                    payment_id,
                    signature,
                    user_id,
                    course_id,
                    total_price,
                    actual_price,
                    has_discount,
                ):
                    return jsonify(
                        {
                            "message": "Payment verified and course purchased successfully."
                        }
                    )
                else:
                    return jsonify({"message": "Payment verification failed."}), 400

            else:
                return jsonify({"message": "Event not handled"}), 400
        else:
            return jsonify({"message": "Invalid signature"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def verify_webhook_signature(webhook_data, signature):

    payload = str(webhook_data)
    secret = WEBHOOK_SECRET.encode("utf-8")
    computed_signature = hmac.new(
        secret, payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)
