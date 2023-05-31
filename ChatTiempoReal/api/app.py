from fastapi import FastAPI
import uvicorn
from database.db import get_database

app = FastAPI()

db = get_database()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
