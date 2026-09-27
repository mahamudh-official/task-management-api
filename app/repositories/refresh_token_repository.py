from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, refresh_token: RefreshToken)-> RefreshToken:
        self.db.add(refresh_token)
        return refresh_token

    def get_by_token(self, token: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def revoke(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked = True
        self.db.add(refresh_token)