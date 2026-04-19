from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://sm_admin:sm_password@localhost:5432/sales_manager"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True  # 🔥 important for long-lived desktop apps
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  # 🔥 IMPORTANT for ORM stability in UI apps
)