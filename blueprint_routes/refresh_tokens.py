from flask import Blueprint, request, jsonify
from repository.refresh_token_repository import RefreshTokenRepository
from services.refresh_token_service import RefreshTokenService
from configs_and_constants.db import DB

refresh_token = Blueprint("refresh_token", __name__)

refresh_token_service = RefreshTokenService(DB().db)