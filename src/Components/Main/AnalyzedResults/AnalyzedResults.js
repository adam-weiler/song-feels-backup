// emotions_percent, emotions_sum, filtered_lyrics, vad_lyrics


// Vanilla React:
import React, { Component } from 'react';

// Third-party libraries:
// import axios from 'axios';

// Bootstrap-React components:
// import Button from 'react-bootstrap/Button';
// import Form from 'react-bootstrap/Form';
import Table from 'react-bootstrap/Table';

import Anger from './Img/angry-face.png';
import Bored from './Img/yawning-face.png';
import Excited from './Img/grinning-face-with-star-eyes.png';
import Fear from './Img/face-screaming-in-fear.png';
import Happy from './Img/grinning-face-with-smiling-eyes.png';
import Sad from './Img/pensive-face.png';

// Call stylesheet last:
import './AnalyzedResults.css';

export default class AnalyzedResults extends Component {

    render() {
        let emotionsPercentElements;
        let emotionsSumElements;
        let filteredLyricsElements;
        let vadLyricsElements;

        if (this.props.songAnalysis) {
            const emotionsImages = [Anger, Bored, Excited, Fear, Happy, Sad];

            const emotionsPercentEntries = Object.entries(this.props.songAnalysis.emotions_percent);  // Convert the emotions_percent object into an array.

            emotionsPercentElements = emotionsPercentEntries.map(  // Map over the newly created emotions_percent array.
                (elem, id) => <td>
                    <img class='emojiFace' src={emotionsImages[id]} /><br/>
                    <strong>{elem[0]}</strong><br/>
                    {parseFloat(elem[1] * 100).toFixed(2)+"%"}
                </td>
            )


            const emotionsSumEntries = Object.entries(this.props.songAnalysis.emotions_sum);  // Convert the emotions_sum object into an array.

            emotionsSumElements = emotionsSumEntries.map(  // Map over the newly created emotions_sum array.
                (elem, id) => <li>
                    <em>{elem[0]}</em> {elem[1]} words
                </li>
            );

            filteredLyricsElements = this.props.songAnalysis.filtered_lyrics.map(
                (elem, id) => <>{elem}, </>
            );

            vadLyricsElements = this.props.songAnalysis.vad_lyrics.map(
                (elem, id) => <tr>
                    <td>{id + 1}</td>
                    <td>{elem.word}</td>
                    <td>{elem.v_mean_sum}</td>
                    <td>{elem.a_mean_sum}</td>
                    <td>{elem.d_mean_sum}</td>
                    <td>{elem.emotionBasic}</td>
                </tr>
            );
        }

// hand-rock

// theater-masks

// smile

// bolt

        return (
            <>
                <br/>
                {
                    !this.props.songAnalysis
                    ? <h3>Please try again!</h3>
                    : 
                    <>
                        <h2>The song has been evaluated to display these emotions:</h2>
                        (List length of original song)<br/>
                        (infobox)
                        <ul>
                                <Table borderless responsive>
                                    <tbody>
                                    <tr>
                                        {emotionsPercentElements}
                                        </tr>
                                    </tbody>
                                </Table>
                        </ul>

                        <h2>These are emotion sums:</h2>
                        <ul>
                                {emotionsSumElements}
                        </ul>

                        <h2>After being filtered, there are {filteredLyricsElements.length} unique words:</h2>
                        (infobox)
                        <p>
                            {filteredLyricsElements}
                        </p>

                        <h2>We found {vadLyricsElements.length} of these in our database of words:</h2>
                        (Infobox)
                        <Table bordered hover responsive striped>
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Word:</th>
                                    <th>Valence:</th>
                                    <th>Arousal:</th>
                                    <th>Dominance</th>
                                    <th>Emotion:</th>
                                </tr>
                            </thead>
                            <tbody>
                                {vadLyricsElements}
                            </tbody>
                        </Table>
                    </>
                }
            </>
        )
    }
}