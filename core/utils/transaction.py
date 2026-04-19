from functools import wraps
from infrastructure.database.session import SessionLocal


def atomic_transaction(func):
    """
    Wraps a service method in a safe DB transaction.
    Handles commit, rollback, and session closing automatically.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()

        try:
            # inject session into function if needed
            result = func(*args, db=db, **kwargs)

            db.commit()
            return result

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    return wrapper