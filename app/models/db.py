from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    users = relationship("User", back_populates="company")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(Role), nullable=False, default=Role.USER)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")
    social_accounts = relationship("SocialAccount", back_populates="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="social_accounts")
    provider = Column(String, nullable=False)
    provider_user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())