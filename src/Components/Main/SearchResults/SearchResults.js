// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Button from 'react-bootstrap/Button';

// Call stylesheet last:
import './SearchResults.css';

const SearchResults = (props) => {
    let songElements;

    if (props.listOfSongs) {  // If there is a list of songs, map them out to songElements.
        songElements = props.listOfSongs.map(
            (elem, id) => <li key={elem.song_id}>
                "{elem.title}" by <em>{elem.artist}</em>&nbsp;<Button id={id} variant="secondary" onClick={props.handlePreviewClick}>Preview</Button>
            </li>
        );
    }

    return (
        <section className='section2'>
            <h2>We found {props.listOfSongs.length} results:</h2>

            {
                props.listOfSongs.length < 1
                ? <h3>Please try again!</h3>
                : <ul>
                        {songElements}
                </ul>
            }

            {
                !props.selectedSong
                ? ''
                : <>
                    <hr/>
                    <h2>"{props.listOfSongs[props.selectedSong]['title']}" by <em>{props.listOfSongs[props.selectedSong]['artist']}</em>:</h2>
                    <p className='original-lyrics'>{props.listOfSongs[props.selectedSong]['lyrics']}</p>
                    <form>
                        <input type="hidden" id="hidden_lyrics" value={props.listOfSongs[props.selectedSong]['lyrics']} />
                        {/* <Form.Check type="checkbox" label="Ignore Repeated Words" /> */}
                        <Button variant="primary" onClick={props.handleAnalyzeClick}>Analyze</Button>
                    </form>
                </>
            }
        </section>
    );
}

export default SearchResults;
