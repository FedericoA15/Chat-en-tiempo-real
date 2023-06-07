import React, { useEffect, useState } from "react";
import axios from "axios";
import { w3cwebsocket as WebSocket } from "websocket";

const App = () => {
  const userId = "6478c00321f12c3a7d8b7d2b";
  const recipientId = "6478064a6715d5ab6d35643e";
  const socket = new WebSocket(`ws://127.0.0.1:8000/chat/${userId}/${recipientId}`);

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    // Establecer los listeners de eventos
    socket.onopen = () => {
      console.log("Conexión WebSocket establecida");
    };

    socket.onmessage = (message) => {
      const data = JSON.parse(message.data);
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    socket.onclose = () => {
      console.log("Conexión WebSocket cerrada");
    };

    // Obtener los mensajes al montar el componente
    getMessages();

    return () => {
      // Cerrar la conexión WebSocket al desmontar el componente
      // socket.close();
    };
  }, []);

  const getMessages = () => {
    const { data } = axios
      .get(`http://127.0.0.1:8000/chat/${userId}/${recipientId}`)
      .catch((error) => {
        console.error("Error al obtener los mensajes:", error);
      });
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const sendMessage = () => {
    if (inputValue.trim() !== "") {
      socket.send(inputValue);
      setInputValue("");
    }
  };

  return (
    <div>
      <h1>Chat en tiempo real</h1>
      <div>
        {messages.map((message, index) => (
          <div key={index}>
            <p>{message.message}</p>
          </div>
        ))}
      </div>
      <input type='text' value={inputValue} onChange={handleInputChange} />
      <button onClick={sendMessage}>Enviar</button>
    </div>
  );
};

export default App;
