from fastapi import HTTPException
from models.users import UserCreate
import re


def validate_user_create(user: UserCreate):
    print("pase por aca")
    if not isinstance(user.username, str) or len(user.username) > 20:
        raise HTTPException(status_code=400, detail="Invalid username.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(status_code=400, detail="Invalid email.")
    if not isinstance(user.password, str) or len(user.password) > 15:
        raise HTTPException(status_code=400, detail="Invalid password.")
