import React, { useState, useEffect, useRef } from "react";
import { w3cwebsocket as WebSocket } from "websocket";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const userId = "6478c00321f12c3a7d8b7d2b";
  const recipientId = "6478064a6715d5ab6d35643e";
  const websocketRef = useRef(null);

  useEffect(() => {
    const websocket = new WebSocket("ws://127.0.0.1:8000/chat/" + userId + "/" + recipientId);
    websocketRef.current = websocket;

    websocket.onopen = () => {
      console.log("WebSocket connection established.");
    };

    websocket.onmessage = (message) => {
      const messageText = message.data;
      const regex = /Previous message: User (\w+): (.+)/;
      const matches = messageText.match(regex);

      if (matches && matches.length >= 3) {
        const senderId = matches[1];
        const messageContent = matches[2];

        const newMessage = {
          sender_id: senderId,
          message: messageContent,
        };

        setMessages((prevMessages) => [...prevMessages, newMessage]);
      }
    };

    websocket.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    return () => {
      // No se cierra la conexión WebSocket al desmontar el componente
    };
  }, [userId, recipientId]);

  const sendMessage = () => {
    const message = {
      sender_id: userId,
      recipient_id: recipientId,
      message: inputMessage,
    };
    websocketRef.current.send(JSON.stringify(message));
    setInputMessage("");
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index}>
            <span>{message.sender_id}: </span>
            <span>{message.message}</span>
          </div>
        ))}
      </div>
      <div>
        <input type='text' value={inputMessage} onChange={(e) => setInputMessage(e.target.value)} />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default App;
