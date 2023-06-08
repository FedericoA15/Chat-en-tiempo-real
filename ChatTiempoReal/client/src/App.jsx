import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import User1 from "./pages/user1";
import User2 from "./pages/User2";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path='/user1' element={<User1 />} />
          <Route path='/user2' element={<User2 />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
