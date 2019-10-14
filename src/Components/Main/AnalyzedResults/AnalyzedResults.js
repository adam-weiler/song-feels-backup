// Vanilla React:
import React, { Component } from 'react';

// Smaller components:
import EmojiCard from './EmojiCard/EmojiCard.js'

// Bootstrap-React components:
import CardColumns from 'react-bootstrap/CardColumns';
import Table from 'react-bootstrap/Table';

// Emoji image files:
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

            // emotionsPercentElements = emotionsPercentEntries.map(  // Map over the newly created emotions_percent array.
            //     (elem, id) => <td>
            //         <img class='emojiFace' src={emotionsImages[id]} /><br/>
            //         <strong>{elem[0]}</strong><br/>
            //         {parseFloat(elem[1] * 100).toFixed(2)+"%"}
            //     </td>
            // )

            emotionsPercentElements = emotionsPercentEntries.map(
                (elem, id) => <EmojiCard emotionImage={emotionsImages[id]} emotionText={elem[0]} emotionPercent={parseFloat(elem[1] * 100).toFixed(2)+"%"} />
            );

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
                {
                    !this.props.songAnalysis
                    ? <h3>Please try again!</h3>
                    : 
                    <>
                        <h2>The song has been evaluated to display these emotions:</h2>
                        (List length of original song)<br/>
                        (infobox)

                        <CardColumns>
                            {emotionsPercentElements}
                        </CardColumns>

                        <EmojiCard />

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
                                    <th>
                                        {/* <OverlayTrigger
                                        key='valence_overlay'
                                        placement='top'
                                        overlay={
                                            <Tooltip>
                                                Tooltip on <strong>thing</strong>.
                                            </Tooltip>
                                        }
                                        ><p>Valence:</p></OverlayTrigger> */}
                                        Valence: 
                                    </th>
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