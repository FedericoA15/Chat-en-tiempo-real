from fastapi import APIRouter
from models.users import UserCreate
from services.user_services import create_user
from validations.user_validation import validate_user_create

router = APIRouter(prefix="/users", tags=["products"])


@router.post("/")
def create_user_route(user: UserCreate):
    print("Antes de ejecutar el validador")
    validate_user_create(user)
    created_user = create_user(user)
    return created_user


@router.get("/")
def prueba():
    return {"Hello": "sexo"}
