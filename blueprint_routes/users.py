from flask import Blueprint, request, jsonify, g
from configs_and_constants.constants import Roles
from repository.user_repository import UserRepository
from repository.refresh_token_repository import RefreshTokenRepository
from services.user_service import UserService
from configs_and_constants.db import DB
from utils.response_handler import response_handler
from middlewares.check_auth_and_permission import check_auth_and_permission

users = Blueprint("users", __name__)

user_repository = UserRepository(DB().db)
refresh_token_repository = RefreshTokenRepository(DB().db)
user_service = UserService(user_repository, refresh_token_repository)


@users.route("/register", methods=["POST"])
def create_user():
    user_data = request.get_json()
    error, user = user_service.create_user(user_data)
    if error:
        return response_handler({"message": error}, 400)
    del user["password"]
    del user["forgot_password_token"]
    del user["verification_token"]
    return response_handler({"data": user}, 201)


@users.route("/register/operational-team", methods=["POST"])
@check_auth_and_permission([Roles.admin.value])
def register_operational_team():
    user_data = request.get_json()
    user_data["role"] = Roles.operational_team.value
    error, user = user_service.create_user(user_data)
    if error:
        return response_handler({"message": error}, 400)
    del user["password"]
    return response_handler({"data": user}, 201)


@users.route("/login", methods=["POST"])
def login_user():
    user_data = request.get_json()
    error, data = user_service.login_user(user_data)
    if error:
        return response_handler({"message": error}, 400)

    data["user"].pop("password", None)
    data["user"].pop("forgot_password_token", None)
    data["user"].pop("verification_token", None)
    return response_handler({"data": data}, 200, {"rf_tkn": data.get("refresh_token")})


@users.route("/login/operational-team", methods=["POST"])
def login_operational_team():
    user_data = request.get_json()
    error, data = user_service.login_user(user_data, role=Roles.operational_team.value)
    if error:
        return response_handler({"message": error}, 400)
    data["user"].pop("password", None)
    return response_handler({"data": data}, 200, {"rf_tkn": data.get("refresh_token")})


@users.route("/users", methods=["GET"])
def get_users():
    error, data = user_service.get_users()

    if error:
        return response_handler({"message": error}, 400)
    return response_handler({"data": data}, 200)
