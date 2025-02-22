from flask import Blueprint, request, jsonify, send_file
import os, uuid

from utils.response_handler import response_handler

files_uploader = Blueprint("files_uploader", __name__)

UPLOAD_FOLDER = "uploads/courses"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024  # 5 GB
ALLOWED_EXTENSIONS = {"mp4", "png", "jpeg", "jpg"}

if not os.path.exists(os.path.join(os.getcwd(), "uploads")):
    os.makedirs(os.path.join(os.getcwd(), "uploads"))


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_filename(filename):
    return str(uuid.uuid4()) + "-" + str(1e9) + "." + filename.rsplit(".", 1)[1]


def check_valid_file(file, request):
    if "file" not in request.files:
        return response_handler({"message": "File not found"}, 400)

    if file.filename == "":
        return response_handler({"message": "No file selected"}, 400)

    if not allowed_file(file.filename):
        return response_handler({"message": "File type not allowed"}, 400)

    return None


def upload_file(request):
    file = request.files.get("file")

    valid_file = check_valid_file(file, request)
    if valid_file:
        return valid_file

    filename = os.path.join(UPLOAD_FOLDER, generate_filename(file.filename))
    try:
        file.save(filename)
        return response_handler({"data": {"filename": filename}}, 201)
    except Exception as error:
        return response_handler(
            {"message": "Something went wrong. Please try again"}, 500
        )


def update_file(request):
    data = request.form
    old_filename = data.get("oldFilename")

    if not old_filename:
        return response_handler({"message": "Old filename not found"}, 400)

    old_file_full_path = os.path.join(os.getcwd(), old_filename)
    if os.path.exists(old_file_full_path):
        os.remove(old_file_full_path)
    else:
        return response_handler({"message": f'No file "{old_filename}" found'}, 400)

    file = request.files.get("file")

    valid_file = check_valid_file(file, request)
    if valid_file:
        return valid_file

    filename = os.path.join(UPLOAD_FOLDER, generate_filename(file.filename))
    try:
        file.save(filename)
        return response_handler({"data": {"filename": filename}}, 201)
    except Exception as error:
        return response_handler(
            {"message": "Something went wrong. Please try again"}, 500
        )


@files_uploader.route("/upload", methods=["POST", "PUT"])
@files_uploader.route("/uploads/<subFolder>/<fileName>", methods=["GET"])
def handle_file_upload(subFolder=None, fileName=None):
    if request.method == "POST":
        return upload_file(request)
    if request.method == "PUT":
        return update_file(request)
    if request.method == "GET":
        filePath = os.path.join(os.getcwd(), "uploads", subFolder, fileName)
        
        if not os.path.exists(filePath):

            return response_handler({"msg": "File Not Found"}, 404)
        return send_file(filePath)


# C:\Users\LENOVO\Desktop\myskillkronos_backend\uploads\courses\05ad4501-6af8-43b0-bc53-88c9451bdd59-1000000000.0.png
