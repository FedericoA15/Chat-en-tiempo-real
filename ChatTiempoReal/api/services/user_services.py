from models.users import UserCreate
from database.db import get_database
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

db = get_database()


def create_user(user: UserCreate):
    user_data = user.dict()

    if db["users"].find_one({"email": user_data["email"]}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data["_id"] = str(ObjectId())
    try:
        db["users"].insert_one(user_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_data
