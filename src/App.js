// Vanilla React:
import React, { Component } from 'react';
// import logo from './logo.svg';

// Smaller components:
import Main from './Components/Main/Main.js';

// Call stylesheet last:
import './App.css';

function App() {
    return (
        <div className="App">
            <header>
                <h1>SongFeels</h1>
            </header>
            <Main />
        </div>
    );
}

export default App;
