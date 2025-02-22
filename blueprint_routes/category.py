from flask import Blueprint, request
from configs_and_constants.constants import Roles
from middlewares.check_auth_and_permission import check_auth_and_permission
from repository.category_repository import CategoryRepository
from services.category_sevice import CategoryService
from configs_and_constants.db import DB
from utils.response_handler import response_handler

categories = Blueprint("categories", __name__)

category_repository = CategoryRepository(DB().db)
category_service = CategoryService(category_repository)


@categories.route("/categories", methods=["POST"])
@check_auth_and_permission([Roles.mentor.value, Roles.admin.value])
def create_category():
    category_data = request.get_json()

    error, category = category_service.create_category(category_data)
    if error:
        return response_handler({"message": error})
    return (
        response_handler(
            {"message": "Category created successfully", "category": category}
        ),
        201,
    )


@categories.route("/categories", methods=["GET"])
def get_category():
    error, categories = category_service.get_all_categories()
    if error:
        return response_handler({"message": error})
    return response_handler({"categories": categories})


#
@categories.route("/categories", methods=["DELETE"])
def delete_category():
    data = request.get_json()
    category_id = data["category_id"]
    error = category_service.delete_category(str(category_id))
    if error:
        return response_handler({"message": error})
    return response_handler({"message": "Category deleted successfully"})
