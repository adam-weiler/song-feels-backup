// Vanilla React:
import React, { Component, useState } from 'react';

// Third-party libraries:
import axios from 'axios';
// import CSRFToken from './csrftoken';

// Smaller components:
import AnalyzedResults from './AnalyzedResults/AnalyzedResults.js';
import ModalPopup from './ModalPopup/ModalPopup.js';
import SearchForm from './SearchForm/SearchForm.js';
import SearchResults from './SearchResults/SearchResults.js';

// Bootstrap-React components:
import Button from 'react-bootstrap/Button';

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

    handleShow = (modalTitle, modalBody) => (event) => {
        event.preventDefault();

        this.setState({
            showModal: true,
            modalTitle: modalTitle,
            modalBody: modalBody
        });
    }

    handleClose = () => {
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

    // handlePreviewClick = (event) => {
    //     event.preventDefault();
    //     console.log('User clicked preview a song:', event.target.id);
    //     console.log('Song data:', this.state.listOfSongs[event.target.id]);

    //             // this.setState({
    //             //     selectedSong: event.target.id
    //             // });

    //     this.handleShow('lyrics')
    //     console.log('yes')
    // }

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
                {/* This only appears when user clicks Tell me More, or Lyrics. */}
                <ModalPopup showModal={this.state.showModal} handleClose={this.handleClose} modalTitle={this.state.modalTitle} modalBody={this.state.modalBody} />
                <section className='section1'>
                    <h4>
                        <strong>SongFeels</strong> will analyze the lyrics of a song and determine which emotions the words are conveying. 
                        {/* <a href='#' onClick={this.handleShow('Explanation', '')}>Tell me More</a> */}
                        {/* <Button variant="info" onClick={this.handleShow('Explanation', '')}>Tell me More</Button> */}
                        <button type="button" className="btn-info" onClick={this.handleShow('Explanation', '')}>Tell me More</button>                        
                    </h4>

                    {/* This only appears if there is an error with the Song name inputbox. */}
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
