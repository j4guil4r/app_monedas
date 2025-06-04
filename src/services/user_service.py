from ..database.session import SessionLocal
from ..database.models import User

class UserService:
    def __init__(self):
        self.db = SessionLocal()

    def create_user(self, name: str):
        try:
            user = User(name=name)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al crear usuario: {str(e)}")
        finally:
            self.db.close()