from fastapi import APIRouter, HTTPException
from models.users import UserCreate
from services.user_services import create_user, get_all_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["products"])


@router.post("/")
def create_user_route(user: UserCreate):
    created_user = create_user(user)
    return created_user


@router.get("/")
def get_all_users_route():
    return get_all_users()


@router.get("/{user_id}")
def get_user_by_id_route(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
