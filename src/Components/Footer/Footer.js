// Vanilla React:
import React, { Component } from 'react';

// Third-party libraries:
// import axios from 'axios';

// Bootstrap-React components:
// import Col from 'react-bootstrap/Col';
// import ListGroup from 'react-bootstrap/ListGroup';
// import Row from 'react-bootstrap/Row';
// import Tab from 'react-bootstrap/Tab';
// import Button from 'react-bootstrap/Button';
// import Form from 'react-bootstrap/Form';
// import Jumbotron from 'react-bootstrap/Jumbotron';

import audd_logo from './Img/AuddLogo.png';
import adam_weiler_logo from './Img/AdamWeilerLogo.png';

// Call stylesheet last:
import './Footer.css';

export default class Footer extends Component {

    render() {
        return (
            <footer className='footer'>
                <ul>
                    <li>
                        <a href='https://adam-weiler.com' target='_blank'>
                            <img src={adam_weiler_logo} border='0' alt='App coded and designed by Adam Weiler.' /> 
                        </a> 
                        &nbsp; Developed by <a href='https://adam-weiler.com' target='_blank'>Adam Weiler</a> ©2019</li>
                    <li>
                        <a href='https://audd.io/' target='_blank'>
                            <img src={audd_logo} border='0' alt='Our app powered by AudD Music Recognition API.' />
                        </a>
                    </li>
                </ul>
            </footer>
        )
    }
}