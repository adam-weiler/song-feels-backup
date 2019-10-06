// Vanilla React:
import React, { Component } from 'react';

// Third-party libraries:
// import axios from 'axios';

// Bootstrap-React components:
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

// Call stylesheet last:
import './SearchResults.css';

export default class SearchResults extends Component {

    render() {
        let jsonElements;

        if (this.props.listOfSongs) {
            jsonElements = this.props.listOfSongs.map(
                (elem, id) => <li key={elem.song_id}>
                    "{elem.title}" by <em>{elem.artist}</em>&nbsp;<Button id={id} variant="secondary" onClick={this.props.handlePreviewClick}>Preview</Button>
                </li>
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


                    // <Form.Check type="checkbox" label="Ignore Repeated Words" />
                }

                
            </>
        )
    }
}