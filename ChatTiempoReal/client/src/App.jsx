import React, { useState, useEffect, useRef } from "react";

const App = () => {
  const socketRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");

  const connectToWebSocket = () => {
    const userId = "6478064a6715d5ab6d35643e"; // Reemplazar con el ID de usuario actual
    const recipientId = "6478c00321f12c3a7d8b7d2b"; // Reemplazar con el ID del destinatario

    const socketUrl = `ws://127.0.0.1:8000/chat/${userId}/${recipientId}`;

    const newSocket = new WebSocket(socketUrl);

    newSocket.onopen = () => {
      console.log("WebSocket connected");
    };

    newSocket.onmessage = (event) => {
      try {
        const messagesArray = JSON.parse(event.data);
        console.log(messagesArray);

        if (Array.isArray(messagesArray)) {
          setMessages((prevMessages) => [...prevMessages, ...messagesArray]);
        } else {
          console.error("Received data is not an array:", messagesArray);
        }
      } catch (error) {
        console.error("Error parsing JSON:", error);
      }
    };

    newSocket.onclose = () => {
      console.log("WebSocket closed");
    };

    socketRef.current = newSocket;
  };

  const sendMessage = () => {
    if (socketRef.current && inputMessage.trim() !== "") {
      const message = inputMessage.trim();
      socketRef.current.send(message);
      setInputMessage("");
    }
  };

  useEffect(() => {
    connectToWebSocket();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    setMessages([]);

    return () => {
      setMessages([]);
    };
  }, []);

  useEffect(() => {
    const handleUnload = () => {
      setMessages([]);
    };

    window.addEventListener("beforeunload", handleUnload);

    return () => {
      window.removeEventListener("beforeunload", handleUnload);
    };
  }, []);

  return (
    <div>
      <div className='message-container'>
        {messages.map((message, index) => {
          return (
            <div
              key={index}
              className={`message ${message.sender_id === "YOUR_USER_ID" ? "sent" : "received"}`}
            >
              {message.message}
            </div>
          );
        })}
      </div>
      <div className='input-container'>
        <input
          type='text'
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder='Type a message...'
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default App;
