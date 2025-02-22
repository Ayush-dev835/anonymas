from bson.objectid import ObjectId


class User:
    def __init__(self, data: dict):

        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.phone_number = data.get("phone_number")
        self.role = data.get("role")

        self.verification_token = None
        self.forgot_password_token = None

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "password": self.password,
            "verification_token": self.verification_token,
            "forgot_password_token": self.forgot_password_token,
        }

    @staticmethod
    def validate(data: dict):
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "role",
        ]
        missing_fields = [field for field in required_fields if not data.get(field)]
       
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}", None
        return None, User(data)
