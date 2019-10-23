// Vanilla React:
import React, { Component, useState } from 'react';

// Third-party libraries:
import axios from 'axios';
// import CSRFToken from './csrftoken';

// Smaller components:
import AnalyzedResults from './AnalyzedResults/AnalyzedResults.js';
import LoadingWheel from './LoadingWheel/LoadingWheel.js';
import ModalPopup from './ModalPopup/ModalPopup.js';
import SearchForm from './SearchForm/SearchForm.js';
import SearchResults from './SearchResults/SearchResults.js';

// Bootstrap-React components:
// import Button from 'react-bootstrap/Button';

// Call stylesheet last:
import './Main.css';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default class Main extends Component {
    state = {
        showModal: false,
        searchInput: '',
        listOfSongs: '',
        errorMessage: '',
        // selectedSong: '',
        songAnalysis: ''
    }

    handleShowModal = (modalTitle, modalBody) => (event) => {
        event.preventDefault();

        this.setState({
            showModal: true,
            modalTitle: modalTitle,
            modalBody: modalBody
        });
    }

    handleCloseModal = () => {
        this.setState({
            showModal: false,
            modalTitle: '',
            modalBody: ''
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

            this.setState({
                analyzing: true,
            });

            let query = songQuery;
            if (artistQuery) {
                query += `_${artistQuery}`;
            }

            axios.get(`/api/song_search/?q=${query}`)
            .then(response => {
                // console.log(response)
                // console.log(response.data.lyrics);

                if (response.data.error) {
                    // console.log(response.data.error);
                    // console.log(response.data.message);

                    this.setState({
                        analyzing: false,
                        errorMessage: response.data.message,   // Returns error message to user.
                    });

                } else {
                    // console.log('no error')
                    this.setState({
                        analyzing: false,
                        songAnalysis: '',   // Removes any previous song analysis (happens if user searches twice).
                        errorMessage: '',   // Removes any previous error message.
                        listOfSongs: response.data.lyrics,
                        // selectedSong: ''    // Removes any previous selected song (happens if user searches twice).
                    });
                }
            })
            .catch(error => {
                // console.error('Error', error);

                this.setState({
                    analyzing: false,
                    errorMessage: 'An error has occurred. Please try again later.',   // Returns error message to user.
                });
            });
        }
    }

    handleAnalyzeClick = (selectedSong) => event => {
        event.preventDefault();
        // console.log('User clicked a analyze a song:', selectedSong);
        // console.log('Song data:', this.state.listOfSongs[selectedSong]['lyrics']);

        this.setState({
            analyzing: true,
        });

        axios.post(`/api/song_analyze/`, {
            original_lyrics: this.state.listOfSongs[selectedSong]['lyrics']
        })
        .then(response => {
            // console.log('Then statement.');
            // console.log(response.data);

            this.setState({
                analyzing: false,
                errorMessage: '',
                songAnalysis: response.data
            });
        })
        .catch(error => {
            // console.error('Error', error);

            this.setState({
                analyzing: false,
                errorMessage: 'An error has occurred. Please try again later.',   // Returns error message to user.
            });
        });
    }

    render() {
        return (
            <main className='jumbotron jumbotron-fluid'>
                {/* This only appears when user clicks Tell me More, or Lyrics. */}
                <ModalPopup showModal={this.state.showModal} handleCloseModal={this.handleCloseModal} modalTitle={this.state.modalTitle} modalBody={this.state.modalBody} />
                
                {
                    !this.state.analyzing
                    ? ''
                    : <>
                        <LoadingWheel />
                    </>
                }
                
                <section className='section1'>
                    <h4>
                        <strong>SongFeels</strong> will analyze the lyrics of a song and determine which emotions the words are conveying. 
                        <button type="button" className="btn-info" onClick={this.handleShowModal('Explanation', '')}>Tell me More</button>                        
                    </h4>

                    <SearchForm errorMessage={this.state.errorMessage} handleSearchClick={this.handleSearchClick} />
                </section>

                {
                    !this.state.listOfSongs
                    ? ''
                    : <>
                        <SearchResults listOfSongs={this.state.listOfSongs} handleShowModal={this.handleShowModal} handleAnalyzeClick={this.handleAnalyzeClick} />
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
