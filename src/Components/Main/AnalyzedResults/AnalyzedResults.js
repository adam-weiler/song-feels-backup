// emotions_percent, emotions_sum, filtered_lyrics, vad_lyrics


// Vanilla React:
import React, { Component } from 'react';

// Third-party libraries:
// import axios from 'axios';

// Bootstrap-React components:
// import Button from 'react-bootstrap/Button';
// import Form from 'react-bootstrap/Form';

// Call stylesheet last:
import './AnalyzedResults.css';

export default class AnalyzedResults extends Component {

    render() {
        let emotionPercentElements;
        let filteredLyricsElements;
        let vadLyricsElements

        if (this.props.songAnalysis) {
            // emotionPercentElements = this.props.songAnalysis.emotions_percent.map(
            //     (elem, id) => <li key={elem.id}>
            //         "{elem.title}" by <em>{elem.artist}</em>&nbsp;
            //     </li>
            // )

            filteredLyricsElements = this.props.songAnalysis.filtered_lyrics.map(
                (elem, id) => <li key={id}>{elem}
                </li>
            )

            vadLyricsElements = this.props.songAnalysis.vad_lyrics.map(
                (elem, id) => <>
                <li key={id}>{elem.word}
                </li>
                <li key={id}>{elem.v_mean_sum}
                </li>
                <li key={id}>{elem.a_mean_sum}
                </li>
                <li key={id}>{elem.d_mean_sum}
                </li>
                <li key={id}>{elem.emotionBasic}
                </li>
                </>
            )
        }


        return (
            <>
                <br/>
                <h2>These are emotion percents:</h2>

                {
                    !this.props.songAnalysis
                    ? <h3>Please try again!</h3>
                    : 
                    <>
                    <ul>
                            {/* {emotionPercentElements} */}
                    </ul>
                    <h2>These are the filtered lyrics:</h2>
                    <ul>
                        {filteredLyricsElements}

                    </ul>
                    <h2>These are the VAD lyrics that were analyzed:</h2>
                    <ul>
                        {vadLyricsElements}
                    </ul>
                    </>
                }
            </>
        )
    }
}