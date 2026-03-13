from sqlalchemy.orm import Session
from app.models.base import BaseRepo
from app.models.db import User
from app.modules.auth.schemas import UserCreate
from app.core.security import get_password_hash

class UserRepo(BaseRepo):
    model = User

    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        return db.query(cls.model).filter(cls.model.email == email).first()

    @classmethod
    def create_user(cls, db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = cls.model(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
