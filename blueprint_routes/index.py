from .users import users
from flask import Flask
from .courses import courses
from .refresh_tokens import refresh_token
from .files_uploader import files_uploader
from .category import categories
from .chapter import chapters
from .payment import payment


def init_routes(server: Flask):
    server.register_blueprint(files_uploader)
    for routes in (users, refresh_token, courses, categories, chapters, payment):
        server.register_blueprint(routes, url_prefix="/api")
