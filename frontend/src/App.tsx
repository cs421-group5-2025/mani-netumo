import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import './App.css';

const Login: React.FC = () => {
  const [token, setToken] = useState('');
  const [username, setUsername] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/login', { username });
      setToken(response.data.access_token);
    } catch (error) {
      console.error('Login failed', error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
      <button onClick={handleLogin}>Login</button>
      {token && <p>Token: {token}</p>}
    </div>
  );
};

const Targets: React.FC = () => {
  const [targets, setTargets] = useState([]);
  const [newUrl, setNewUrl] = useState('');
  const token = localStorage.getItem('token') || '';

  useEffect(() => {
    const fetchTargets = async () => {
      try {
        const response = await axios.get('http://localhost:5000/targets/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setTargets(response.data);
      } catch (error) {
        console.error('Failed to fetch targets', error);
      }
    };
    fetchTargets();
  }, [token]);

  const addTarget = async () => {
    try {
      await axios.post(
        'http://localhost:5000/targets/',
        { url: newUrl },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNewUrl(''); // Refresh list
      window.location.reload(); // Simple refresh, improve later
    } catch (error) {
      console.error('Failed to add target', error);
    }
  };

  return (
    <div>
      <h2>Targets</h2>
      <input
        type="text"
        value={newUrl}
        onChange={(e) => setNewUrl(e.target.value)}
        placeholder="Enter URL"
      />
      <button onClick={addTarget}>Add Target</button>
      <ul>
        {targets.map((target: any) => (
          <li key={target.id}>
            {target.url} - {target.status} ({target.latency}ms)
          </li>
        ))}
      </ul>
    </div>
  );
};

const App: React.FC = () => {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  useEffect(() => {
    if (token) localStorage.setItem('token', token);
  }, [token]);

  return (
    <Router>
      <div className="App">
        <nav>
          <Link to="/">Login</Link> | <Link to="/targets">Targets</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route
            path="/targets"
            element={
              token ? (
                <Targets />
              ) : (
                <p>Please <Link to="/">login</Link> first.</p>
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;