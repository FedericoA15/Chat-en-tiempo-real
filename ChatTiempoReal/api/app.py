# main.py
from fastapi import FastAPI
from fastapi import WebSocket
from typing import Dict

app = FastAPI()

# Almacenamiento temporal de conexiones de WebSocket por usuario
connections: Dict[str, WebSocket] = {}


# Ruta WebSocket para manejar las conexiones de chat
@app.websocket("/chat/{sender_id}/{recipient_id}")
async def chat_endpoint(websocket: WebSocket, sender_id: str, recipient_id: str):
    await websocket.accept()

    # Asignar el WebSocket a la conexión del remitente
    connections[sender_id] = websocket

    while True:
        message = await websocket.receive_text()
        # Lógica para procesar y guardar los mensajes en la base de datos

        # Enviar el mensaje al destinatario si está conectado
        recipient_connection = connections.get(recipient_id)
        if recipient_connection:
            await recipient_connection.send_text(message)
