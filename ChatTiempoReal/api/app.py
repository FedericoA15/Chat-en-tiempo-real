from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
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

# Almacenamiento temporal de conexiones de WebSocket por usuario
connections: Dict[str, List[WebSocket]] = {}


async def deliver_pending_messages(recipient_id: str):
    db = get_database()
    pending_messages = db.pending_messages.count_documents(
        {"recipient_id": recipient_id}
    )

    if pending_messages > 0:
        messages = db.pending_messages.find({"recipient_id": recipient_id})
        for message in messages:
            if recipient_id in connections:
                for connection in connections[recipient_id]:
                    await connection.send_text(message["message"])
            db.pending_messages.delete_one({"_id": message["_id"]})


# Ruta WebSocket para manejar las conexiones de chat
@app.websocket("/chat/{sender_id}/{recipient_id}")
async def chat_endpoint(websocket: WebSocket, sender_id: str, recipient_id: str):
    await websocket.accept()

    # Asignar el WebSocket a la conexión del remitente
    if sender_id not in connections:
        connections[sender_id] = []

    connections[sender_id].append(websocket)

    db = get_database()

    # Buscar el documento de la conversación
    conversation = db.conversations.find_one(
        {"participants": {"$all": [sender_id, recipient_id]}}
    )

    if conversation is None:
        # Crear un nuevo documento para la conversación si no existe
        conversation = {"participants": [sender_id, recipient_id], "messages": []}
        db.conversations.insert_one(conversation)

    try:
        # Entregar mensajes pendientes si el destinatario se ha reconectado
        await deliver_pending_messages(recipient_id)

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

            # Enviar el mensaje a todos los destinatarios conectados
            if recipient_id in connections:
                for connection in connections[recipient_id]:
                    await connection.send_text(message)
            else:
                # Almacenar el mensaje en la base de datos para entregarlo posteriormente
                db.pending_messages.insert_one(message_data)
    finally:
        # Eliminar la conexión del remitente al cerrar el WebSocket
        connections[sender_id].remove(websocket)
        if not connections[sender_id]:
            del connections[sender_id]


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
