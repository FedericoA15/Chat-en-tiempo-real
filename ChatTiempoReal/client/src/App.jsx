import React, { useState, useEffect, useRef } from "react";
import { w3cwebsocket as WebSocket } from "websocket";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const userId = "6478c00321f12c3a7d8b7d2b";
  const recipientId = "6478064a6715d5ab6d35643e";
  const websocketRef = useRef(null);

  useEffect(() => {
    let websocket = websocketRef.current;

    if (!websocket) {
      websocket = new WebSocket("ws://127.0.0.1:8000/chat/" + userId + "/" + recipientId);
      websocketRef.current = websocket;
    }

    const handleOpen = () => {
      console.log("WebSocket connection established.");
    };

    const handleMessage = (message) => {
      const messageData = JSON.parse(message.data);
      console.log(messageData.message);

      const newMessage = {
        sender_id: messageData.userId,
        message: messageData.message,
      };

      setMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    const handleClose = () => {
      console.log("WebSocket connection closed.");
    };

    websocket.addEventListener("open", handleOpen);
    websocket.addEventListener("message", handleMessage);
    websocket.addEventListener("close", handleClose);

    return () => {
      websocket.removeEventListener("open", handleOpen);
      websocket.removeEventListener("message", handleMessage);
      websocket.removeEventListener("close", handleClose);
    };
  }, [userId, recipientId]);

  useEffect(() => {
    // Obtener los mensajes anteriores desde el backend al cargar la página
    const fetchChatMessages = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/chat_messages?sender_id=" + userId + "&recipient_id=" + recipientId
        );
        const data = await response.json();
        setMessages(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching chat messages:", error);
      }
    };

    fetchChatMessages();
  }, [userId, recipientId]);

  const sendMessage = () => {
    const message = {
      userId: userId,
      recipient_id: recipientId,
      message: inputMessage,
    };
    websocketRef.current.send(JSON.stringify(message));

    setInputMessage("");
  };

  return (
    <div>
      {loading ? (
        <div>Cargando mensajes...</div>
      ) : (
        <div>
          {messages.map((message, index) => (
            <div
              key={index}
              style={{
                textAlign: message.sender_id === userId ? "right" : "left",
                margin: "10px 0",
              }}
            >
              {message.message}
            </div>
          ))}
        </div>
      )}
      <div>
        <input type='text' value={inputMessage} onChange={(e) => setInputMessage(e.target.value)} />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default App;
