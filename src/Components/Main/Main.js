// Vanilla React:
import React, { Component, useState } from 'react';

// Third-party libraries:
import axios from 'axios';

// Bootstrap-React components:
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Jumbotron from 'react-bootstrap/Jumbotron';

// Call stylesheet last:
import './Main.css';

export default class Main extends Component {
    state = {
        searchInput: '',
        listOfSongs: '',
        errorMessage: ''
    }

    handleSearchClick = (event) => {
        event.preventDefault();
        console.log('User clicked search:');

        let songQuery = document.querySelector('#songInput').value;
        let artistQuery = document.querySelector('#artistInput').value;

        if (!songQuery) {
            console.error('Error; no song name.');
            this.setState({
                errorMessage: 'Please enter a valid song name.'
            });
        } else {
            console.log('Good to go; song name: ', songQuery);

            let query = songQuery;
            if (artistQuery) {
                query += `_${artistQuery}`;
            }

            axios.get(`/api/song_search/?q=${query}`)
            .then(response => {
                console.log(response.data.songList);

                this.setState({
                    errorMessage: '',
                    listOfSongs: response.data.songList
                });
            });
        }
    }

    render() {
        return (
            // const [validated, setValidated] = useState(false);

            <main className='jumbotron jumbotron-fluid'>
                {/* <Form noValidate validated={validated}> */}
                <Form>
                    <Form.Group controlId='songInput'>
                        <Form.Label>Enter the name of the song you want to search for:</Form.Label>
                        <Form.Control type='text' name='songInput' placeholder='Song name' required/>
                    </Form.Group>

                    {
                        !this.state.errorMessage
                        ? ''
                        : <Alert variant='danger'>{this.state.errorMessage}</Alert>
                        
                    }

                    <Form.Group controlId='artistInput'>
                        <Form.Label>Enter the name of the band or artist:</Form.Label>
                        <Form.Control type='text' name='artistInput' placeholder='Artist name (optional)' required/>
                    </Form.Group>
                    <Button variant='primary' type='submit' onClick={this.handleSearchClick}>
                        Search
                    </Button>
                </Form>

                {
                    !this.state.listOfSongs
                    ? ''
                    : <>
                        <p>We found 2 results:</p><p>{this.state.listOfSongs[0].artist}</p>
                    </>
                }
            </main>
        );
    }
}