from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    name: str
    email:EmailStr
    disabled: bool

class UserCreateSchema(UserBaseSchema):
    password: str

class UserSchema(UserBaseSchema):
    id: int
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str