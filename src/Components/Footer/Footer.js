// Vanilla React:
import React from 'react';

// Image files:
import audd_logo from './Img/AuddLogo.png';
import adam_weiler_logo from './Img/AdamWeilerLogo.png';

// Call stylesheet last:
import './Footer.css';

const Footer = () => {
    return (
        <footer className='footer'>
            <ul>
                <li>
                    <a href='https://adam-weiler.com' target='_blank' rel="noopener noreferrer" >
                        <img src={adam_weiler_logo} border='0' alt='App coded and designed by Adam Weiler.' /> 
                    </a> 
                    &nbsp; Developed by <a href='https://adam-weiler.com' target='_blank' rel="noopener noreferrer" >Adam Weiler</a> ©2019</li>
                <li>
                    Lyrics API: &nbsp;
                    <a href='https://audd.io/' target='_blank' rel="noopener noreferrer" >
                        <img src={audd_logo} border='0' alt='Our app powered by AudD Music Recognition API.' />
                    </a>
                </li>
            </ul>
        </footer>
    );
}

export default Footer;
