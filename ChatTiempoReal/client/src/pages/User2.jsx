import React, { useState, useEffect } from "react";
import { w3cwebsocket as WebSocket } from "websocket";

const User2 = () => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    // Obtener la conversación completa antes de establecer la conexión WebSocket
    fetch("http://127.0.0.1:8000/conversation/2/1")
      .then((response) => response.json())
      .then((data) => {
        const retrievedMessages = data.messages.map((messageData) => messageData.message);
        console.log(retrievedMessages);
        setMessages(retrievedMessages);
      })
      .catch((error) => {
        console.error("Error al obtener la conversación:", error);
      });

    // Crea una nueva instancia de WebSocket
    const newWebsocket = new WebSocket("ws://127.0.0.1:8000/chat/2/1");
    setWebsocket(newWebsocket);

    // Configura los controladores de eventos del WebSocket
    newWebsocket.onopen = () => {
      console.log("Conexión WebSocket establecida");
    };

    newWebsocket.onmessage = (event) => {
      const message = event.data;
      console.log(event);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    newWebsocket.onclose = () => {
      console.log("Conexión WebSocket cerrada");
    };

    // Limpia la instancia de WebSocket al desmontar el componente
    return () => {
      newWebsocket.close();
      setWebsocket(null);
    };
  }, []);

  const sendMessage = () => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(messageInput);
      setMessages((prevMessages) => [...prevMessages, messageInput]); // Agrega el mensaje enviado a la lista de mensajes
      setMessageInput("");
    }
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index}>{message}</div>
        ))}
      </div>
      <input type='text' value={messageInput} onChange={(e) => setMessageInput(e.target.value)} />
      <button onClick={sendMessage}>Enviar</button>
    </div>
  );
};

export default User2;
