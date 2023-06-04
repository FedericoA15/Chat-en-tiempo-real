from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
import uvicorn
from database.db import get_database
from routers.users import router as users_router

app = FastAPI()

db = get_database()
websocket_connections = []

# Registrar los enrutadores
app.include_router(users_router)


# Ruta principal
@app.get("/")
def home():
    return {"message": "Welcome to the chat application"}


# Ruta de WebSocket para manejar las conexiones de chat
@app.websocket("/chat/{user_id}")
async def chat_websocket(websocket: WebSocket, user_id: str):
    global websocket_connections  # Declarar la variable como global

    await websocket.accept()

    # Registrar la conexión WebSocket
    websocket_connections.append({"user_id": user_id, "websocket": websocket})

    try:
        while True:
            # Recibir mensaje del cliente
            message = await websocket.receive_text()

            # Enviar el mensaje a todos los clientes conectados
            for connection in websocket_connections:
                await connection["websocket"].send_text(f"User {user_id}: {message}")

    except WebSocketDisconnect:
        # Remover la conexión WebSocket al desconectarse
        websocket_connections = [
            connection
            for connection in websocket_connections
            if connection["websocket"] != websocket
        ]


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
