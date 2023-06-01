from fastapi import FastAPI
import uvicorn
from database.db import get_database
from routers.users import router as users_router

app = FastAPI()

db = get_database()

# Registrar los enrutadores
app.include_router(users_router)


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
