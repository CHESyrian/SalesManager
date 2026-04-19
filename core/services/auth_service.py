from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.models.user import User


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


class AuthService:

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password, hashed):
        return pwd_context.verify(password, hashed)

    @staticmethod
    def authenticate(db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return None

        if not user.is_active:
            return None

        if not AuthService.verify_password(password, user.password_hash):
            return None

        return user