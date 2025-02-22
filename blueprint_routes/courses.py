from flask import Blueprint, request
from bson.objectid import ObjectId
from repository.course_repository import CourseRepository
from services.course_service import CourseService
from configs_and_constants.db import DB
from utils.response_handler import response_handler
from configs_and_constants.constants import Roles
from middlewares.check_auth_and_permission import check_auth_and_permission

courses = Blueprint("courses", __name__)

course_repository = CourseRepository(DB().db)
course_service = CourseService(course_repository)


@courses.route("/courses", methods=["POST"])
@check_auth_and_permission([Roles.mentor.value, Roles.admin.value])
def create_courses():
    course_data = request.get_json()

    if "category_id" in course_data:
        try:
            course_data["category_id"] = ObjectId(course_data["category_id"])
        except Exception as error:
            return response_handler({"message": f"Invalid category_id: {error}"}, 400)

    course_data.update({"author_id": ObjectId(request.user.get("_id"))})

    error, course = course_service.create_course(course_data)
    if error:
        return response_handler({"message": error}, 400)

    course.update(
        {
            "author_id": str(course.get("author_id")),
            "category_id": str(course.get("category_id")),
        }
    )

    return response_handler({"data": course}, 201)


@courses.route("/courses", methods=["GET"])
@check_auth_and_permission()
def get_courses():
    user = request.user

    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 10))
    category_id = request.args.get("category_id")

    if limit > 20:
        limit = 10

    skip = page * limit

    if category_id:
        error, courses = course_service.get_courses_by_category(
            category_id, skip, limit
        )

    else:
        if user.get("role") in [Roles.admin.value, Roles.operational_team.value]:
            error, courses = course_service.get_admin_courses(skip, limit)
        elif user.get("role") == Roles.mentor.value:
            error, courses = course_service.get_mentor_courses(
                user.get("_id"), skip, limit
            )
        # elif user.get("role") == Roles.learner.value:
        #     result = course_service.get_learner_courses(user.get("_id"), skip, limit)
        elif user.get("role") == Roles.learner.value:
            error, courses = course_service.get_all_courses(skip, limit)
        else:
            return response_handler({"message": "Invalid role."}, 403)

    if error:
        return response_handler({"message": error}, 400)
    return response_handler({"data": courses}, 200)


@courses.route("/courses/publish/<course_id>", methods=["PATCH"])
@check_auth_and_permission([Roles.admin.value])
def update_publish_status(course_id):
    data = request.get_json()
    print(data,"lllllll")

    if "is_published" not in data:
        return response_handler({"message": "Missing 'is_published' in request body."}, 400)

    is_published = data["is_published"]

    if not isinstance(is_published, bool):
        return response_handler({"message": "'is_published' should be a boolean value."}, 400)

    error, result = course_service.update_publish_status(course_id, is_published)

    if error:
        return response_handler({"message": error}, 400)

    return response_handler({"data": result}, 200)




@courses.route("/courses/<course_id>", methods=["GET"])
def get_course_details(course_id):
    error, course = course_service.get_course_by_id(course_id)
    if error:
        return response_handler({"message": error}, 404)
    return response_handler({"data": course}, 200)


@courses.route("/courses/<course_id>", methods=["DELETE"])
@check_auth_and_permission([Roles.admin.value, Roles.mentor.value])
def delete_coursecourse_id(course_id):
    user = request.user
    # print(course, "jjjjjjjjjjjjjjj")

    course = course_service.delete_course_by_id(course_id)

    if not course:
        return response_handler({"message": "Course not found."}, 404)

    if user.get("role") != Roles.admin.value:

        return response_handler(
            {"message": "You are not authorized to delete this course."}, 403
        )

    try:
        course_service.delete_course_by_id(course_id)
        return response_handler({"message": "Course deleted successfully."}, 200)
    except Exception as error:
        return response_handler({"message": f"Error: {error}"}, 400)
