from infrastructure.database.session import SessionLocal


class BaseController:

    def __init__(self):
        self.db = SessionLocal()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        if self.db:
            self.db.close()
            self.db = None