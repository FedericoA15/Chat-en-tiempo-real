from fastapi import APIRouter, HTTPException
from models.users import UserCreate
from services.user_services import create_user

router = APIRouter(prefix="/users", tags=["products"])


@router.post("/")
def create_user_route(user: UserCreate):
    created_user = create_user(user)
    return created_user
