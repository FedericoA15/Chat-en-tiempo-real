from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from database.db import get_database

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Almacenamien

# Almacenamiento temporal de conexiones de WebSocket por usuario
connections: Dict[str, WebSocket] = {}


# Ruta WebSocket para manejar las conexiones de chat
@app.websocket("/chat/{sender_id}/{recipient_id}")
async def chat_endpoint(websocket: WebSocket, sender_id: str, recipient_id: str):
    await websocket.accept()

    # Asignar el WebSocket a la conexión del remitente
    connections[sender_id] = websocket

    db = get_database()

    # Buscar el documento de la conversación
    conversation = db.conversations.find_one(
        {"participants": {"$all": [sender_id, recipient_id]}}
    )

    if conversation is None:
        # Crear un nuevo documento para la conversación si no existe
        conversation = {"participants": [sender_id, recipient_id], "messages": []}
        db.conversations.insert_one(conversation)

    while True:
        message = await websocket.receive_text()
        # Lógica para procesar y guardar los mensajes en la base de datos
        message_data = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message": message,
        }
        db.conversations.update_one(
            {"_id": conversation["_id"]}, {"$push": {"messages": message_data}}
        )

        # Enviar el mensaje al destinatario si está conectado
        recipient_connection = connections.get(recipient_id)
        if recipient_connection:
            await recipient_connection.send_text(message)


# Ruta para recuperar todos los mensajes de una conversación
@app.get("/conversation/{sender_id}/{recipient_id}")
def get_conversation(sender_id: str, recipient_id: str):
    db = get_database()

    # Buscar el documento de la conversación
    conversation = db.conversations.find_one(
        {"participants": {"$all": [sender_id, recipient_id]}}
    )

    if conversation is None:
        return {"message": "Conversación no encontrada"}

    messages = conversation.get("messages", [])
    return {"messages": messages}
