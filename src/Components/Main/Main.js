// Vanilla React:
import React, { Component, useState } from 'react';

// Third-party libraries:
import axios from 'axios';

// Smaller components:
import AnalyzedResults from './AnalyzedResults/AnalyzedResults.js';
import SearchResults from './SearchResults/SearchResults.js';

// Bootstrap-React components:
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
// import Jumbotron from 'react-bootstrap/Jumbotron';

// Call stylesheet last:
import './Main.css';

export default class Main extends Component {
    state = {
        searchInput: '',
        listOfSongs: '',
        errorMessage: '',
        selectedSong: '',
        songAnalysis: ''
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
                console.log(response.data.lyrics);
                // TODO: Replace /r/n with return, or . punctuation.

                this.setState({
                    errorMessage: '',
                    listOfSongs: response.data.lyrics
                });
            })
            .catch(error => {
                console.log('Error', error)
            });
        }
    }

    handlePreviewClick = (event) => {
        event.preventDefault();
        console.log('User clicked preview a song:', event.target.id);
        console.log('Song data:', this.state.listOfSongs[event.target.id]);

        this.setState({
            selectedSong: event.target.id
        });
    }

    handleAnalyzeClick = (event) => {
        event.preventDefault();
        console.log('User clicked a analyze a song:', this.state.selectedSong);
        console.log('Song data:', this.state.listOfSongs[this.state.selectedSong]['lyrics']);

        // let query = this.state.selectedSong;
        let query = this.state.listOfSongs[this.state.selectedSong]['lyrics'];
        console.log('query', query)

        axios.get(`/api/song_analyze/?q=${query}`)
        .then(response => {
            console.log('Then statement.')
            console.log(response.data);

            this.setState({
                songAnalysis: response.data
            })

            // this.setState({
            //     errorMessage: '',
            //     listOfSongs: response.data.songList
            // });
        })
        .catch(error => {
            console.log('Error', error)
        });
        console.log('Well thats over with!')
    }

    

    render() {
        return (
            // const [validated, setValidated] = useState(false);

            <main className='jumbotron jumbotron-fluid'>
                {/* <Form noValidate validated={validated}> */}
                <Form>
                    {/* {% csrf_token %} */}
                    <Form.Group controlId='songInput'>
                        <Form.Label>Enter the name of the song you want to search for:</Form.Label>
                        <Form.Control type='text' name='songInput' placeholder='Song name' required value='Sober'/>
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
                        <SearchResults listOfSongs={this.state.listOfSongs} handlePreviewClick={this.handlePreviewClick} />
                    </>
                }

                {
                    !this.state.selectedSong
                    ? ''
                    : <>
                    <p>"{this.state.listOfSongs[this.state.selectedSong]['lyrics']}"</p>
                    <Button variant="primary" onClick={this.handleAnalyzeClick}>Analyze</Button>
                        {/* <AnalysisResults  /> */}
                    </>
                }

                {
                    !this.state.songAnalysis
                    ? ''
                    : <>
                        <AnalyzedResults songAnalysis={this.state.songAnalysis} />
                        {/* {this.state.analyzedResults.emotions_percent} */}
                    </>
                }
            </main>
        );
    }
}