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
        songAnalysis: ''  // Switch this back
        
        // songAnalysis: {  // For Testing only.
        //     "filtered_lyrics": [
        //       "bbridge",
        //       "bchorus",
        //       "boutro",
        //       "bpre",
        //       "bring",
        //       "butler",
        //       "bverse",
        //       "c",
        //       "called",
        //       "can",
        //       "center",
        //       "chew",
        //       "chorus",
        //       "come",
        //       "complicate",
        //       "d",
        //       "drink",
        //       "elevate",
        //       "empty",
        //       "f",
        //       "fall",
        //       "find",
        //       "finger",
        //       "forever",
        //       "fucking",
        //       "has",
        //       "imbecile",
        //       "jesus",
        //       "leave",
        //       "liar",
        //       "like",
        //       "making",
        //       "mary",
        //       "mother",
        //       "murder",
        //       "must",
        //       "past",
        //       "path",
        //       "pointing",
        //       "promise",
        //       "q",
        //       "rests",
        //       "s",
        //       "shadow",
        //       "shrouding",
        //       "sleep",
        //       "sober",
        //       "son",
        //       "stalking",
        //       "start",
        //       "step",
        //       "t",
        //       "take",
        //       "things",
        //       "trust",
        //       "upon",
        //       "waiting",
        //       "want",
        //       "whisper",
        //       "whistle",
        //       "will",
        //       "won",
        //       "work",
        //       "worthless"
        //     ],
        //     "vad_lyrics": [
        //       {
        //         "word": "bring",
        //         "v_mean_sum": 5.68,
        //         "a_mean_sum": 4.29,
        //         "d_mean_sum": 5.72,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "butler",
        //         "v_mean_sum": 5.62,
        //         "a_mean_sum": 2.55,
        //         "d_mean_sum": 6.04,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "can",
        //         "v_mean_sum": 6.41,
        //         "a_mean_sum": 3.14,
        //         "d_mean_sum": 6.44,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "center",
        //         "v_mean_sum": 5.56,
        //         "a_mean_sum": 2.62,
        //         "d_mean_sum": 5.72,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "chew",
        //         "v_mean_sum": 5.58,
        //         "a_mean_sum": 3.8,
        //         "d_mean_sum": 6.48,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "chorus",
        //         "v_mean_sum": 6,
        //         "a_mean_sum": 4.2,
        //         "d_mean_sum": 5.26,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "come",
        //         "v_mean_sum": 5.64,
        //         "a_mean_sum": 3.57,
        //         "d_mean_sum": 5.94,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "complicate",
        //         "v_mean_sum": 3.3,
        //         "a_mean_sum": 4.95,
        //         "d_mean_sum": 4.52,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "drink",
        //         "v_mean_sum": 6.67,
        //         "a_mean_sum": 5.19,
        //         "d_mean_sum": 5.87,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "elevate",
        //         "v_mean_sum": 6.42,
        //         "a_mean_sum": 4.65,
        //         "d_mean_sum": 5.67,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "empty",
        //         "v_mean_sum": 3.78,
        //         "a_mean_sum": 2.25,
        //         "d_mean_sum": 3.61,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "fall",
        //         "v_mean_sum": 3.89,
        //         "a_mean_sum": 4.24,
        //         "d_mean_sum": 3.83,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "find",
        //         "v_mean_sum": 6.45,
        //         "a_mean_sum": 3.52,
        //         "d_mean_sum": 6.24,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "finger",
        //         "v_mean_sum": 5.8,
        //         "a_mean_sum": 4.15,
        //         "d_mean_sum": 5.32,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "fucking",
        //         "v_mean_sum": 5.09,
        //         "a_mean_sum": 6.86,
        //         "d_mean_sum": 4.94,
        //         "emotionBasic": "Anger"
        //       },
        //       {
        //         "word": "imbecile",
        //         "v_mean_sum": 3,
        //         "a_mean_sum": 5.17,
        //         "d_mean_sum": 3.12,
        //         "emotionBasic": "Fear"
        //       },
        //       {
        //         "word": "leave",
        //         "v_mean_sum": 4.68,
        //         "a_mean_sum": 4.48,
        //         "d_mean_sum": 5.47,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "liar",
        //         "v_mean_sum": 2.41,
        //         "a_mean_sum": 6.6,
        //         "d_mean_sum": 4.74,
        //         "emotionBasic": "Anger"
        //       },
        //       {
        //         "word": "like",
        //         "v_mean_sum": 7.44,
        //         "a_mean_sum": 4.4,
        //         "d_mean_sum": 6.28,
        //         "emotionBasic": "Happy"
        //       },
        //       {
        //         "word": "mother",
        //         "v_mean_sum": 7.53,
        //         "a_mean_sum": 4.73,
        //         "d_mean_sum": 6.11,
        //         "emotionBasic": "Happy"
        //       },
        //       {
        //         "word": "murder",
        //         "v_mean_sum": 1.48,
        //         "a_mean_sum": 6.24,
        //         "d_mean_sum": 3.38,
        //         "emotionBasic": "Fear"
        //       },
        //       {
        //         "word": "must",
        //         "v_mean_sum": 5.45,
        //         "a_mean_sum": 4.1,
        //         "d_mean_sum": 5.06,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "past",
        //         "v_mean_sum": 5.09,
        //         "a_mean_sum": 4.71,
        //         "d_mean_sum": 5.18,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "path",
        //         "v_mean_sum": 5.71,
        //         "a_mean_sum": 3.74,
        //         "d_mean_sum": 4.62,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "promise",
        //         "v_mean_sum": 6.64,
        //         "a_mean_sum": 3.9,
        //         "d_mean_sum": 6.47,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "shadow",
        //         "v_mean_sum": 5.07,
        //         "a_mean_sum": 3.1,
        //         "d_mean_sum": 4.41,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "sleep",
        //         "v_mean_sum": 7.22,
        //         "a_mean_sum": 3.6,
        //         "d_mean_sum": 5.3,
        //         "emotionBasic": "Happy"
        //       },
        //       {
        //         "word": "sober",
        //         "v_mean_sum": 5.95,
        //         "a_mean_sum": 4.32,
        //         "d_mean_sum": 6.86,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "son",
        //         "v_mean_sum": 6.91,
        //         "a_mean_sum": 4.43,
        //         "d_mean_sum": 5,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "start",
        //         "v_mean_sum": 6.41,
        //         "a_mean_sum": 4.81,
        //         "d_mean_sum": 5.5,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "step",
        //         "v_mean_sum": 5.68,
        //         "a_mean_sum": 3.48,
        //         "d_mean_sum": 6,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "take",
        //         "v_mean_sum": 4.82,
        //         "a_mean_sum": 4.52,
        //         "d_mean_sum": 4.83,
        //         "emotionBasic": "Sad"
        //       },
        //       {
        //         "word": "trust",
        //         "v_mean_sum": 7.24,
        //         "a_mean_sum": 4.3,
        //         "d_mean_sum": 6.95,
        //         "emotionBasic": "Happy"
        //       },
        //       {
        //         "word": "want",
        //         "v_mean_sum": 6,
        //         "a_mean_sum": 5.29,
        //         "d_mean_sum": 5.39,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "whisper",
        //         "v_mean_sum": 6.14,
        //         "a_mean_sum": 4.1,
        //         "d_mean_sum": 5.66,
        //         "emotionBasic": "Excited"
        //       },
        //       {
        //         "word": "whistle",
        //         "v_mean_sum": 5.7,
        //         "a_mean_sum": 3.94,
        //         "d_mean_sum": 5.78,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "will",
        //         "v_mean_sum": 5.32,
        //         "a_mean_sum": 2.9,
        //         "d_mean_sum": 6.61,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "work",
        //         "v_mean_sum": 5.05,
        //         "a_mean_sum": 4.33,
        //         "d_mean_sum": 6.12,
        //         "emotionBasic": "Bored"
        //       },
        //       {
        //         "word": "worthless",
        //         "v_mean_sum": 1.89,
        //         "a_mean_sum": 4.45,
        //         "d_mean_sum": 2.71,
        //         "emotionBasic": "Sad"
        //       }
        //     ],
        //     "emotions_sum": {
        //       "Anger": 2,
        //       "Bored": 12,
        //       "Excited": 11,
        //       "Fear": 2,
        //       "Happy": 4,
        //       "Sad": 8
        //     },
        //     "emotions_percent": {
        //       "Anger": 0.05128205128205128,
        //       "Bored": 0.3076923076923077,
        //       "Excited": 0.28205128205128205,
        //       "Fear": 0.05128205128205128,
        //       "Happy": 0.10256410256410256,
        //       "Sad": 0.20512820512820512
        //     }
        //   }
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
                        <Form.Control type='text' name='songInput' placeholder='Song name' required />
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
                    <h2>These are the original lyrics:</h2>
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