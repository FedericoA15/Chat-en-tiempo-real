from fastapi import APIRouter, HTTPException
from models.users import UserCreate
from services.user_services import create_user, email_exists

router = APIRouter(prefix="/users", tags=["products"])


@router.post("/")
def create_user_route(user: UserCreate):
    email = user.email

    if email_exists(email):
        raise HTTPException(status_code=400, detail="Email already exists")

    created_user = create_user(user)
    return created_user


@router.get("/")
def prueba():
    return {"Hello": "sexo"}
