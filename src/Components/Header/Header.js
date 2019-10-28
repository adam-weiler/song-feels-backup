// Vanilla React:
import React from 'react';

// Image files:
import song_feels_logo from './Img/SongFeels-logo.png';

// Call stylesheet last:
import './Header.css';

const Header = () => {
    return (
        <header>
            {/* <img src={song_feels_logo} border='0' alt='SongFeels logo' />  */}
                {/* <div className="float-right pl-20"> */}
                    <h1 className="text-center">SongFeels</h1>
                    <p>Lyrics Sentiment Analysis</p>
                {/* </div> */}
        </header>
    );
}

export default Header;
