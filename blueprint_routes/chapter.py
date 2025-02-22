from flask import Blueprint, request
from repository.chapter_repository import ChapterRepository
from configs_and_constants.db import DB
from services.chapter_service import ChapterService
from utils.response_handler import response_handler
from bson.objectid import ObjectId

chapters = Blueprint("chapters", __name__)

chapter_repository = ChapterRepository(DB().db)
chapter_service = ChapterService(chapter_repository)


@chapters.route("/chapters", methods=["POST"])
def create_chapter():
    data = request.get_json()

    data["course_id"] = ObjectId(data["course_id"])

    error, chapter = chapter_service.create_cheapter(data)
    if error:
        return response_handler({"message": error}, 400)

    # if "course_id" in chapter:
    #     chapter["course_id"] = str(chapter["course_id"])
    chapter["course_id"] = str(chapter["course_id"])
    return response_handler({"data": chapter}, 201)


@chapters.route("/chapters/<course_id>", methods=["GET"])
def get_chapter(course_id):

    course_id = ObjectId(course_id)

    error, chapter = chapter_service.get_chapter(course_id)
    if error:
        return response_handler({"message": error}, 404)

    chapters = list(chapter)

    for chapter in chapters:
        chapter["_id"] = str(chapter["_id"])
        chapter["course_id"] = str(chapter["course_id"])

    return response_handler({"data": chapters}, 200)


#
@chapters.route('/chapters', methods=["DELETE"])
def delete_chapter():
    data = request.get_json()
    chapter_id = data["chapter_id"]
    error = chapter_service.delete_chapter(str(chapter_id))
    if error:
        return response_handler({"message": error}, 404)
    
    