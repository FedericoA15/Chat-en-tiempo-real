from models.users import UserCreate
from database.db import get_database
from bson import ObjectId
from fastapi import HTTPException

db = get_database()


def create_user(user: UserCreate):
    user_data = user.dict()
    user_data["_id"] = str(ObjectId())
    db["users"].insert_one(user_data)
    return user_data
