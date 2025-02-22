from flask import Flask, g
import signal
import sys
from blueprint_routes.index import init_routes
from configs_and_constants.env import env
from configs_and_constants.init_roles import init_roles
from configs_and_constants.db import DB
from flask_cors import CORS

db = DB()

server = None


def init_server():
    server = Flask(__name__)
    CORS(server, supports_credentials=True, origins="*")
    # init_roles(db.db)
    init_routes(server)
    server.run(
        debug=env.get("flask_env") == "development",
        host="0.0.0.0",
        port=env.get("port"),
    )


def handle_gracefull_shutdown(_, __):
    db.close()
    print("System is going offline")
    sys.exit(0)


def init_signals():
    for signal_type in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(signal_type, handle_gracefull_shutdown)


if __name__ == "__main__":
    init_signals()
    init_server()
