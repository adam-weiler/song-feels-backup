// Vanilla React:
import React from 'react';

// Smaller components:
import Footer from './Components/Footer/Footer.js';
import Main from './Components/Main/Main.js';

// Call stylesheet last:
import './App.css';

const App = () => {
    return (
        <div className="App">
            <header>
                <h1>SongFeels</h1>
            </header>
            <Main />
            <Footer />
        </div>
    );
}

export default App;
