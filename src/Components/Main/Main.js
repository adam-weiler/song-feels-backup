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

        listOfSongs: '',  // Switch this back
        // listOfSongs: [{'song_id': '87427', 'artist_id': '24716', 'title': 'The House of the Rising Sun', 'title_with_featured': 'The House of the Rising Sun', 'full_title': 'The House of the Rising Sun by\xa0The\xa0Animals', 'artist': 'The Animals', 'lyrics': "There is a house in New Orleans\r\n They call the Rising Sun\r\n And it's been the ruin of many a poor boy\r\n And God I know I'm one\r\n \r\n My mother was a tailor\r\n She sewed my new bluejeans\r\n My father was a gamblin' man\r\n Down in New Orleans\r\n \r\n Now the only thing a gambler needs\r\n Is a suitcase and trunk\r\n And the only time he's satisfied\r\n Is when he's on a drunk\r\n \r\n [Organ Solo]\r\n \r\n Oh mother tell your children\r\n Not to do what I have done\r\n Spend your lives in sin and misery\r\n In the House of the Rising Sun\r\n \r\n Well, I got one foot on the platform\r\n The other foot on the train\r\n I'm goin' back to New Orleans\r\n To wear that ball and chain\r\n \r\n Well, there is a house in New Orleans\r\n They call the Rising Sun\r\n And it's been the ruin of many a poor boy\r\n And God I know I'm one", 'media': '[{"provider":"apple_music","provider_id":"1108150799","type":"audio","url":"https:\\/\\/itunes.apple.com\\/lookup?entity=song&id=1108150799"},{"native_uri":"spotify:track:61Q9oJNd9hJQFhSDh6Qlap","provider":"spotify","type":"audio","url":"https:\\/\\/open.spotify.com\\/track\\/61Q9oJNd9hJQFhSDh6Qlap"},{"provider":"youtube","start":0,"type":"video","url":"http:\\/\\/www.youtube.com\\/watch?v=0sB3Fjw3Uvc"}]'}], // For testing only.

        errorMessage: '',
        selectedSong: '',

        songAnalysis: ''  // Switch this back
        // songAnalysis: { "filtered_lyrics": [ "back", "ball", "bluejeans", "boy", "call", "chain", "children", "do", "drunk", "father", "foot", "gambler", "gamblin'", "god", "goin'", "got", "have", "he's", "house", "i'm", "it's", "know", "lives", "man", "misery", "mother", "needs", "new", "one", "organ", "orleans", "other", "platform", "poor", "rising", "ruin", "satisfied", "sewed", "sin", "solo", "spend", "suitcase", "sun", "tailor", "tell", "thing", "time", "train", "trunk", "wear" ], "vad_lyrics": [ { "word": "back", "v_mean_sum": 4.76, "a_mean_sum": 2.59, "d_mean_sum": 5.22, "emotionBasic": "Bored" }, { "word": "ball", "v_mean_sum": 6.14, "a_mean_sum": 3.48, "d_mean_sum": 5.47, "emotionBasic": "Excited" }, { "word": "boy", "v_mean_sum": 5.84, "a_mean_sum": 4.11, "d_mean_sum": 5.5, "emotionBasic": "Bored" }, { "word": "call", "v_mean_sum": 6.18, "a_mean_sum": 3.29, "d_mean_sum": 5.61, "emotionBasic": "Excited" }, { "word": "chain", "v_mean_sum": 4.79, "a_mean_sum": 4.05, "d_mean_sum": 4.2, "emotionBasic": "Sad" }, { "word": "children", "v_mean_sum": 6.36, "a_mean_sum": 5.09, "d_mean_sum": 5.95, "emotionBasic": "Excited" }, { "word": "do", "v_mean_sum": 5.41, "a_mean_sum": 3.67, "d_mean_sum": 6.35, "emotionBasic": "Bored" }, { "word": "drunk", "v_mean_sum": 4.06, "a_mean_sum": 5.05, "d_mean_sum": 2.94, "emotionBasic": "Fear" }, { "word": "father", "v_mean_sum": 6.88, "a_mean_sum": 3.68, "d_mean_sum": 5.19, "emotionBasic": "Excited" }, { "word": "foot", "v_mean_sum": 4.68, "a_mean_sum": 2.77, "d_mean_sum": 5.97, "emotionBasic": "Bored" }, { "word": "gambler", "v_mean_sum": 4.15, "a_mean_sum": 5.8, "d_mean_sum": 4.44, "emotionBasic": "Anger" }, { "word": "god", "v_mean_sum": 5.9, "a_mean_sum": 5.56, "d_mean_sum": 5, "emotionBasic": "Excited" }, { "word": "have", "v_mean_sum": 5.86, "a_mean_sum": 3.52, "d_mean_sum": 5.72, "emotionBasic": "Bored" }, { "word": "house", "v_mean_sum": 7.19, "a_mean_sum": 3.95, "d_mean_sum": 6.41, "emotionBasic": "Happy" }, { "word": "know", "v_mean_sum": 6.82, "a_mean_sum": 3.24, "d_mean_sum": 5.78, "emotionBasic": "Excited" }, { "word": "man", "v_mean_sum": 5.42, "a_mean_sum": 4.36, "d_mean_sum": 5.44, "emotionBasic": "Bored" }, { "word": "misery", "v_mean_sum": 2.2, "a_mean_sum": 4.82, "d_mean_sum": 3.8, "emotionBasic": "Sad" }, { "word": "mother", "v_mean_sum": 7.53, "a_mean_sum": 4.73, "d_mean_sum": 6.11, "emotionBasic": "Happy" }, { "word": "new", "v_mean_sum": 7.68, "a_mean_sum": 5.14, "d_mean_sum": 5.22, "emotionBasic": "Happy" }, { "word": "one", "v_mean_sum": 6.09, "a_mean_sum": 2.67, "d_mean_sum": 5.56, "emotionBasic": "Excited" }, { "word": "organ", "v_mean_sum": 4.95, "a_mean_sum": 3.41, "d_mean_sum": 5.55, "emotionBasic": "Bored" }, { "word": "other", "v_mean_sum": 5.41, "a_mean_sum": 3.48, "d_mean_sum": 6, "emotionBasic": "Bored" }, { "word": "platform", "v_mean_sum": 5, "a_mean_sum": 4.18, "d_mean_sum": 6.42, "emotionBasic": "Bored" }, { "word": "poor", "v_mean_sum": 3.67, "a_mean_sum": 4.67, "d_mean_sum": 4, "emotionBasic": "Sad" }, { "word": "ruin", "v_mean_sum": 2.32, "a_mean_sum": 5.4, "d_mean_sum": 5.16, "emotionBasic": "Anger" }, { "word": "satisfied", "v_mean_sum": 7.16, "a_mean_sum": 3.95, "d_mean_sum": 6.26, "emotionBasic": "Happy" }, { "word": "sin", "v_mean_sum": 3.08, "a_mean_sum": 5.82, "d_mean_sum": 5.74, "emotionBasic": "Anger" }, { "word": "solo", "v_mean_sum": 5.91, "a_mean_sum": 4.12, "d_mean_sum": 6.04, "emotionBasic": "Excited" }, { "word": "spend", "v_mean_sum": 5.91, "a_mean_sum": 4.48, "d_mean_sum": 5.88, "emotionBasic": "Excited" }, { "word": "suitcase", "v_mean_sum": 5.25, "a_mean_sum": 3.24, "d_mean_sum": 5.5, "emotionBasic": "Bored" }, { "word": "sun", "v_mean_sum": 6.92, "a_mean_sum": 4.64, "d_mean_sum": 4.98, "emotionBasic": "Excited" }, { "word": "tailor", "v_mean_sum": 5.29, "a_mean_sum": 3.61, "d_mean_sum": 6.17, "emotionBasic": "Bored" }, { "word": "tell", "v_mean_sum": 5.27, "a_mean_sum": 3.86, "d_mean_sum": 4.94, "emotionBasic": "Sad" }, { "word": "thing", "v_mean_sum": 5.55, "a_mean_sum": 3.43, "d_mean_sum": 5.41, "emotionBasic": "Bored" }, { "word": "time", "v_mean_sum": 5.6, "a_mean_sum": 3.41, "d_mean_sum": 4.36, "emotionBasic": "Sad" }, { "word": "train", "v_mean_sum": 6.36, "a_mean_sum": 4.05, "d_mean_sum": 5.72, "emotionBasic": "Excited" }, { "word": "trunk", "v_mean_sum": 5.02, "a_mean_sum": 3.51, "d_mean_sum": 5.46, "emotionBasic": "Bored" }, { "word": "wear", "v_mean_sum": 6.36, "a_mean_sum": 3.33, "d_mean_sum": 5.72, "emotionBasic": "Excited" } ], "emotions_sum_percent": { "Anger": [ 3, 0.07894736842105263 ], "Bored": [ 13, 0.34210526315789475 ], "Excited": [ 12, 0.3157894736842105 ], "Fear": [ 1, 0.02631578947368421 ], "Happy": [ 4, 0.10526315789473684 ], "Sad": [ 5, 0.13157894736842105 ] } } // For Testing only.
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
        console.log('User clicked preview a song:', event.target.id);
        console.log('Song data:', this.state.listOfSongs[event.target.id]);

        this.setState({
            selectedSong: event.target.id
        });
    }

    handleAnalyzeClick = (event) => {
        event.preventDefault();
        // console.log('User clicked a analyze a song:', this.state.selectedSong);
        // console.log('Song data:', this.state.listOfSongs[this.state.selectedSong]['lyrics']);

        let query = this.state.listOfSongs[this.state.selectedSong]['lyrics'];
        // console.log('query', query)

        axios.post(`/api/song_analyze/`, {
            original_lyrics: this.state.listOfSongs[this.state.selectedSong]['lyrics']
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
                        <strong>SongFeels</strong> will analyze the lyrics of a song and determine which emotions the words are conveying. <a href='' onClick={this.handleShow}>Tell me More</a>
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
                        <SearchResults listOfSongs={this.state.listOfSongs} handlePreviewClick={this.handlePreviewClick} selectedSong={this.state.selectedSong} handleAnalyzeClick={this.handleAnalyzeClick} />
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
