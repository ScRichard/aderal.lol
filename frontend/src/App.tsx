import React, { useState, useEffect } from 'react';

import Handler from "./Forms";


const App: React.FC = () => {
  const [username, setUsername] = useState("");
  const [token, setToken] = useState("");

  const [output, setOutput] = useState("");

  return (
    <div>
      <Handler.LoginPanel></Handler.LoginPanel>
    </div>
  );
};

export default App;