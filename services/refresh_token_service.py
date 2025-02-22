from repository.refresh_token_repository import RefreshTokenRepository

class RefreshTokenService():
    def __init__(self, refresh_token_repository:RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository
        
    