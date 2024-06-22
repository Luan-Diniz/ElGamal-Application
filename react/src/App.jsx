// src/App.jsx
import React from 'react';
import './App.css';
import Survey from './components/survey';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Questionário</h1>
        <Survey />
      </header>
    </div>
  );
}

export default App;
