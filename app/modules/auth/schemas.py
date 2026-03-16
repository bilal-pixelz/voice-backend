from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    phone_number: str | None = None
    email: EmailStr

class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str | None = None

class User(UserBase):
    id: int
    is_active: bool
    company_id: int | None
    hashed_password: str

    class Config:
        from_attributes = True