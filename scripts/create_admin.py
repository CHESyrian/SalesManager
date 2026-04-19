from infrastructure.database.connection import SessionLocal
from domain.models.user import User
from core.services.auth_service import AuthService


db = SessionLocal()

username = "admin001"
password = "password001"

existing = db.query(User).filter(User.username == username).first()

if existing:
    print("Admin already exists.")
    
else:
    user = User(
        username=username,
        password_hash=AuthService.hash_password(password),
        role="admin"
    )

    db.add(user)
    db.commit()
    print("Admin created.")