// Vanilla React:
import React from 'react';

// Smaller components:
import Footer from './Components/Footer/Footer.js';
import Header from './Components/Header/Header.js';
import Main from './Components/Main/Main.js';

// Call stylesheet last:
import './App.css';

const App = () => {
    return (
        <div className="App">
            <Header />
            <Main />
            <Footer />
        </div>
    );
}

export default App;
