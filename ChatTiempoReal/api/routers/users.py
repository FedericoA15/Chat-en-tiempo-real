from fastapi import APIRouter, HTTPException
from models.users import UserCreate
from services.user_services import create_user, get_all_users

router = APIRouter(prefix="/users", tags=["products"])


@router.post("/")
def create_user_route(user: UserCreate):
    created_user = create_user(user)
    return created_user


@router.get("/")
def get_all_users_route():
    return get_all_users()
