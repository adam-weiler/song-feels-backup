// Vanilla React:
import React, { Component } from 'react';

// Third-party libraries:
// import axios from 'axios';

// Bootstrap-React components:
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
import Row from 'react-bootstrap/Row';
import Tab from 'react-bootstrap/Tab';
// import Button from 'react-bootstrap/Button';
// import Form from 'react-bootstrap/Form';
// import Jumbotron from 'react-bootstrap/Jumbotron';

// Call stylesheet last:
import './SearchResults.css';

export default class SearchResults extends Component {

    render() {
        let jsonElements;

        if (this.props.listOfSongs) {
            jsonElements = this.props.listOfSongs.map(
                (elem, id) => <li key={elem.song_id} onClick="">{elem.title} by {elem.artist}</li>
            )
        }


        return (
            <>
                <br/>
                <h2>We found {this.props.listOfSongs.length} results:</h2>

                {
                    this.props.listOfSongs.length < 1
                    ? <h3>Please try again!</h3>
                    : <ul>
                        {jsonElements}
                    </ul>
                }

                
            </>
        )
    }
}