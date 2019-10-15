// Vanilla React:
import React from 'react';

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

const AnalyzedResults = (props) => {
    let emotionsSumPercentElements;

    let filteredLyricsElements;
    let vadLyricsElements;

    if (props.songAnalysis) {  // If song has been analyzed.
        const emotionsImages = [Anger, Bored, Excited, Fear, Happy, Sad];  // Stores all of the images in an array.

        const emotionsSumPercentEntries = Object.entries(props.songAnalysis.emotions_sum_percent);  // Convert the emotions_sum_percent object into an array. 
        //ie: emotionsSumPercentEntries[2] is ["Excitement", [12, 0.3157894736842105]]
        //This represents emotionName, emotionSum, and emotionPercent.
        
        emotionsSumPercentElements = emotionsSumPercentEntries.map(  // Map over the newly created emotions_percent array.  This is displayed as 6 EmojiCards.
            (elem, id) => <EmojiCard emotionImage={emotionsImages[id]} emotionName={elem[0]} emotionSum={elem[1][0]} emotionPercent={parseFloat(elem[1][1] * 100).toFixed(2)+"%"} />
        );

        filteredLyricsElements = props.songAnalysis.filtered_lyrics.map(  // Map over all filtered lyrics. This is displayed in a paragraph.
            (elem, id) => <>{elem}, </>
        );

        vadLyricsElements = props.songAnalysis.vad_lyrics.map(  // Map over all lyrics found in the VAD database. This is displayed as a table.
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
        <section className='section3'>
            {
                !props.songAnalysis
                ? <h3>This song could not be analyzed.</h3>
                : 
                <>
                    <h2>The song has been evaluated to these emotions:</h2>
                    {/* (infobox) */}

                    <CardColumns>
                        {emotionsSumPercentElements}
                    </CardColumns>

                    {/* <h2>The song originally had x words in the lyrics.</h2> */}

                    <h2>After being filtered, there are {filteredLyricsElements.length} unique words:</h2>
                    {/* (infobox) */}
                    <p>
                        {filteredLyricsElements}
                    </p>

                    <h2>We found {vadLyricsElements.length} of these in our database of words:</h2>
                    {/* (Infobox) */}
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
        </section>
    );
}

export default AnalyzedResults;
