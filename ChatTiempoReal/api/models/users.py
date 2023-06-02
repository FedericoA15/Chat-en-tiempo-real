from pydantic import BaseModel, EmailStr, constr, ValidationError, validator


class UserCreate(BaseModel):
    username: constr(min_length=5, max_length=20)
    email: EmailStr
    password: constr(min_length=8, max_length=15)


class User(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        orm_mode = True
