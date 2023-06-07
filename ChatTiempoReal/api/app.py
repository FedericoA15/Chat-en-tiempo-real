from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
import uvicorn
from database.db import get_database
from routers.users import router as users_router
import json

app = FastAPI()

db = get_database()
websocket_connections = []

# Registrar los enrutadores
app.include_router(users_router)


# Función para guardar el mensaje en la base de datos
def save_message(sender_id: str, recipient_id: str, message: str):
    # Obtener la colección de conversaciones (crearla si no existe)
    collection = db["chat_conversations"]

    # Buscar el documento de la conversación entre el remitente y el destinatario
    conversation = collection.find_one(
        {
            "$or": [
                {"participants": [sender_id, recipient_id]},
                {"participants": [recipient_id, sender_id]},
            ]
        }
    )

    if conversation:
        # Actualizar el documento existente con el nuevo mensaje
        collection.update_one(
            {"_id": conversation["_id"]},
            {"$push": {"messages": json.loads(message)["message"]}},
        )
    else:
        # Crear un nuevo documento de conversación y agregar el mensaje
        conversation_data = {
            "participants": [sender_id, recipient_id],
            "messages": [json.loads(message)["message"]],
        }
        collection.insert_one(conversation_data)


# Ruta principal
@app.get("/")
def home():
    return {"message": "Bienvenido a la aplicación de chat"}


def get_chat_messages(sender_id: str, recipient_id: str):
    # Obtener la colección de conversaciones
    collection = db["chat_conversations"]

    # Buscar el documento de la conversación entre el remitente y el destinatario
    conversation = collection.find_one(
        {
            "$or": [
                {"participants": [sender_id, recipient_id]},
                {"participants": [recipient_id, sender_id]},
            ]
        }
    )

    if conversation:
        # Devolver los mensajes de la conversación
        return conversation["messages"]
    else:
        return []


@app.websocket("/chat/{user_id}/{recipient_id}")
async def chat_websocket(websocket: WebSocket, user_id: str, recipient_id: str):
    global websocket_connections  # Declarar la variable como global

    await websocket.accept()

    # Registrar la conexión WebSocket
    websocket_connections.append({"user_id": user_id, "websocket": websocket})

    try:
        # Recuperar los mensajes del chat desde la base de datos
        chat_messages = get_chat_messages(user_id, recipient_id)

        # Agregar los mensajes anteriores a una lista
        previous_messages = []
        for message in chat_messages:
            previous_message = {
                "userId": user_id,
                "recipient_id": recipient_id,
                "message": message,
            }
            previous_messages.append(previous_message)

        if previous_messages:
            # Enviar los mensajes anteriores al usuario recién conectado
            await websocket.send_json(previous_messages)

        while True:
            # Recibir mensaje del cliente
            message = await websocket.receive_text()

            # Guardar el mensaje en la base de datos
            save_message(user_id, recipient_id, message)

            # Enviar el mensaje al usuario actual
            await websocket.send_json(
                {"userId": user_id, "recipient_id": recipient_id, "message": message}
            )

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
                await recipient_connection["websocket"].send_json(
                    {
                        "userId": user_id,
                        "recipient_id": recipient_id,
                        "message": message,
                    }
                )

    except WebSocketDisconnect:
        # Remover la conexión WebSocket al desconectarse
        websocket_connections = [
            connection
            for connection in websocket_connections
            if connection["websocket"] != websocket
        ]


@app.get("/chat/{user_id}/{recipient_id}")
@app.get("/chat/{user_id}/{recipient_id}")
def get_chat_conversation(user_id: str, recipient_id: str):
    collection = db["chat_conversations"]

    conversation = collection.find_one(
        {
            "$or": [
                {"participants": [user_id, recipient_id]},
                {"participants": [recipient_id, user_id]},
            ]
        },
        {"messages": 1, "_id": 0},  # Proyectar solo el campo "messages" y excluir "_id"
    )

    if conversation:
        return conversation["messages"]
    else:
        return {"message": "Conversación no encontrada"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    print("Iniciando el servidor...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
