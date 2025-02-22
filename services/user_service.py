from repository.user_repository import UserRepository
from repository.refresh_token_repository import RefreshTokenRepository
from entities.user import User
import bcrypt
from configs_and_constants.constants import Roles
from utils.jwt_utils import generate_access_token, generate_refresh_token
from entities.refresh_token import RefreshToken
from bson.objectid import ObjectId


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    def create_user(self, data):
        validation_error, user = User.validate(data)

        if validation_error:
            return validation_error, None

        user = user.serialize()

        if user.get("role") not in [
            Roles.mentor.value,
            Roles.learner.value,
            Roles.operational_team.value,
        ]:
            return "Invalid role", None

        error, existing_user = self.user_repository.find_by_fields(
            {
                "$or": [
                    {"email": user.get("email")},
                    {"phone_number": user.get("phone_number")},
                ]
            }
        )

        if error:
            return error, None

        if existing_user:
            return "Email or phone_number are already exists", None

        hashed_password = bcrypt.hashpw(
            user.get("password").encode("utf-8"), bcrypt.gensalt()
        )

        user.update({"password": hashed_password.decode("utf-8")})

        return self.user_repository.create(user)

    def login_user(self, data):
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return "Email and password are required", None

        error, user = self.user_repository.find_by_fields({"email": email})
        if error:
            return error, None

        if not user:
            return "User not found", None

        hashedpassword = user["password"].encode("utf-8")
        if not bcrypt.checkpw(password.encode("utf-8"), hashedpassword):
            return "invalid password", None

        access_token = generate_access_token(
            {"_id": user.get("_id"), "role": user.get("role")}
        )
        refresh_token = generate_refresh_token(
            {"_id": user.get("_id"), "role": user.get("role")}
        )

        refresh_token_data = RefreshToken(
            refresh_token=refresh_token, user_id=ObjectId(user.get("_id"))
        )
        refresh_token_data = refresh_token_data.serialize()
        self.refresh_token_repository.create(refresh_token_data)

        return None, {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        }

    def get_users(self):
        return self.user_repository.find_all()
