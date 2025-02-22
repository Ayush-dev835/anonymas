import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), "./.env"))

env = {
    "port": os.environ.get("PORT"),
    "flask_env":  os.environ.get("FLASK_ENV"),
    "db_name":  os.environ.get("DB_NAME"),
    "db_uri":  os.environ.get("Db_URI"),
    "access_token_secret" : os.environ.get("ACCESS_TOKEN_SECRET"),
    "refresh_token_secret" : os.environ.get("REFRESH_TOKEN_SECRET"),
    
}