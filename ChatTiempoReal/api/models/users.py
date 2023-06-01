from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., description="El nombre de usuario es obligatorio.")
    email: str = Field(..., description="El email es obligatorio.")
    password: str = Field(..., description="La contraseña es obligatoria.")


class User(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        orm_mode = True
