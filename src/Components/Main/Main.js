// Vanilla React:
import React, { Component, useState } from 'react';

// Third-party libraries:
import axios from 'axios';
// import CSRFToken from './csrftoken';

// Smaller components:
import AnalyzedResults from './AnalyzedResults/AnalyzedResults.js';
import SearchForm from './SearchForm/SearchForm.js';
import SearchResults from './SearchResults/SearchResults.js';

// Bootstrap-React components:
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

// Call stylesheet last:
import './Main.css';

// axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
// axios.defaults.xsrfCookieName = "csrftoken";

export default class Main extends Component {
    state = {
        showModal: false,
        searchInput: '',
        listOfSongs: '',
        errorMessage: '',
        selectedSong: '',
        songAnalysis: ''
    }

    handleShow = (event) => {
        event.preventDefault();

        this.setState({
            showModal: true,
        });
    }

    handleClose = () => {
        this.setState({
            showModal: false
        });
    }

    handleSearchClick = (event) => {  // User clicks on Search button.
        event.preventDefault();
        // console.log('User clicked search.');

        let songQuery = document.querySelector('#songInput').value;
        let artistQuery = document.querySelector('#artistInput').value;

        if (!songQuery) {
            // console.error('Error; no song name.');
            this.setState({
                errorMessage: 'Please enter a valid song name.'
            });
        } else {
            // console.log('User entered valid song name: ', songQuery);

            let query = songQuery;
            if (artistQuery) {
                query += `_${artistQuery}`;
            }

            axios.get(`/api/song_search/?q=${query}`)
            .then(response => {
                // console.log(response.data.lyrics);

                this.setState({
                    songAnalysis: '',   // Removes any previous song analysis (happens if user searches twice).
                    errorMessage: '',   // Removes any previous error message.
                    listOfSongs: response.data.lyrics,
                    selectedSong: ''    // Removes any previous selected song (happens if user searches twice).
                });
            })
            .catch(error => {
                // console.error('Error', error);
            });
        }
    }

    handlePreviewClick = (event) => {
        event.preventDefault();
        // console.log('User clicked preview a song:', event.target.id);
        // console.log('Song data:', this.state.listOfSongs[event.target.id]);

        this.setState({
            selectedSong: event.target.id
        });
    }

    handleAnalyzeClick = (selectedSong) => event => {
        event.preventDefault();
        // console.log('User clicked a analyze a song:', this.state.selectedSong);
        // console.log('Song data:', this.state.listOfSongs[this.state.selectedSong]['lyrics']);

        axios.post(`/api/song_analyze/`, {
            // original_lyrics: this.state.listOfSongs[this.state.selectedSong]['lyrics']
            original_lyrics: this.state.listOfSongs[selectedSong]['lyrics']
        })
        .then(response => {
            // console.log('Then statement.');
            // console.log(response.data);

            this.setState({
                errorMessage: '',
                songAnalysis: response.data
            });
        })
        .catch(error => {
            // console.error('Error', error);
        });
    }

    render() {
        return (
            <main className='jumbotron jumbotron-fluid'>
                <section className='section1'>
                    <h4>
                        <strong>SongFeels</strong> will analyze the lyrics of a song and determine which emotions the words are conveying. <a href='#' onClick={this.handleShow}>Tell me More</a>
                    </h4>

                    {/* This only appears when user clicks Tell me More. */}
                    <Modal size="lg" show={this.state.showModal} onHide={this.handleClose} aria-labelledby="SongFeels explanation">
                        <Modal.Header closeButton>
                            <Modal.Title>Explanation:</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            <p><em>SongFeels</em> uses the <a href='https://audd.io/' target='_blank' rel="noopener noreferrer" >AudD Music Recognition API</a> to search for the user's song and lyrics.</p>
                            <p>Before touching the database, the lyrics are cleaned by removing symbols, numbers, common words, and duplicate words. This reduces most word counts significantly.</p>
                            <p>The cleaned lyrics are compared to the <a href='http://crr.ugent.be/archives/1003' target='_blank' rel="noopener noreferrer" >Warringer and Kuperman database</a> of 13,915 English words. Any lyrics that are found in the database are stored with their Valence, Arousal, Dominance score which is between 0 (low) and 10 (high).</p>
                            <ul>
                                <li>Valence is how negative or positive the word is viewed.</li>
                                <li>Arousal is how boring or exciting the word is viewed.</li>
                                <li>Dominance is how powerless or in control the word feels.</li>
                            </ul>
                            <p>Each of the lyrics that was found in the database is run through my algorithm, which looks at the 3 VAD scores and assigns a basic emotion to the word; Anger, Bored, Excited, Fear, Happy, or Sad.</p>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={this.handleClose}>
                                Close
                            </Button>
                        </Modal.Footer>
                    </Modal>
                    <SearchForm errorMessage={this.state.errorMessage} handleSearchClick={this.handleSearchClick} />
                </section>

                {
                    !this.state.listOfSongs
                    ? ''
                    : <>
                        <SearchResults listOfSongs={this.state.listOfSongs} handlePreviewClick={this.handlePreviewClick} selectedSong={this.state.selectedSong} showModal={this.state.showModal} handleShow={this.handleShow} handleClose={this.handleClose} handleAnalyzeClick={this.handleAnalyzeClick} />
                    </>
                }

                {
                    !this.state.songAnalysis
                    ? ''
                    : <>
                        <AnalyzedResults songAnalysis={this.state.songAnalysis} />
                    </>
                }
            </main>
        );
    }
}
