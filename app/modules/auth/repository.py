from sqlalchemy.orm import Session
from app.models.base import BaseRepo
from app.models.db import User, SocialAccount
from app.modules.auth.schemas import UserCreate
from app.core.passwords import get_password_hash

class UserRepo(BaseRepo):
    model = User

    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        return db.query(cls.model).filter(cls.model.email == email).first()

    @classmethod
    def create_user(cls, db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = cls.model(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def create_user_for_social_login(cls, db: Session, user_info: dict):
        db_user = cls.model(
            email=user_info["email"],
            first_name=user_info.get("given_name"),
            last_name=user_info.get("family_name"),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def get_social_account(
        cls, db: Session, provider: str, provider_user_id: str
    ) -> SocialAccount | None:
        return (
            db.query(SocialAccount)
            .filter(
                SocialAccount.provider == provider,
                SocialAccount.provider_user_id == provider_user_id,
            )
            .first()
        )

    @classmethod
    def create_social_account(
        cls, db: Session, user_id: int, provider: str, provider_user_id: str
    ) -> SocialAccount:
        db_social_account = SocialAccount(
            user_id=user_id, provider=provider, provider_user_id=provider_user_id
        )
        db.add(db_social_account)
        db.commit()
        db.refresh(db_social_account)
        return db_social_account
