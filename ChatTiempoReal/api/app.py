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


# Función para guardar el mensaje en la base de datos
def save_message(sender_id: str, recipient_id: str, message: str):
    # Obtener la colección de mensajes (crearla si no existe)
    collection = db["chat_messages"]

    # Crear el documento del mensaje
    message_data = {
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "message": message,
    }

    # Insertar el documento en la colección
    collection.insert_one(message_data)


# Ruta principal
@app.get("/")
def home():
    return {"message": "Welcome to the chat application"}


def get_chat_messages(sender_id: str, recipient_id: str):
    # Obtener la colección de mensajes
    collection = db["chat_messages"]

    # Consultar los documentos de la colección que coinciden con el remitente y el destinatario
    messages = collection.find(
        {
            "$or": [
                {"sender_id": sender_id, "recipient_id": recipient_id},
                {"sender_id": recipient_id, "recipient_id": sender_id},
            ]
        }
    )

    # Devolver los mensajes como una lista de diccionarios
    return list(messages)


@app.websocket("/chat/{user_id}/{recipient_id}")
async def chat_websocket(websocket: WebSocket, user_id: str, recipient_id: str):
    global websocket_connections  # Declarar la variable como global

    await websocket.accept()

    # Registrar la conexión WebSocket
    websocket_connections.append({"user_id": user_id, "websocket": websocket})

    try:
        # Recuperar los mensajes del chat desde la base de datos
        chat_messages = get_chat_messages(user_id, recipient_id)

        # Enviar los mensajes anteriores al usuario recién conectado
        for message_data in chat_messages:
            sender = message_data["sender_id"]
            message = message_data["message"]
            previous_message = f"User {sender}: {message}"
            await websocket.send_text(previous_message)

        while True:
            # Recibir mensaje del cliente
            message = await websocket.receive_text()

            # Guardar el mensaje en la base de datos
            save_message(user_id, recipient_id, message)

            # Enviar el mensaje al usuario actual
            await websocket.send_text(f"You: {message}")

            # Buscar la conexión del destinatario
            recipient_connection = next(
                (
                    connection
                    for connection in websocket_connections
                    if connection["user_id"] == recipient_id
                ),
                None,
            )

            if recipient_connection:
                # Enviar el mensaje al destinatario
                await recipient_connection["websocket"].send_text(
                    f"User {user_id}: {message}"
                )

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
