// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

// Call stylesheet last:
import './SearchResults.css';

const SearchResults = (props) => {
    let songElements;

    if (props.listOfSongs) {  // If there is a list of songs, map them out to songElements.
        songElements = props.listOfSongs.map(
            (elem, id) => <div key={elem.song_id} className='search-results'>
                <div className='rightText'>
                    "{elem.title}" by <em>{elem.artist}</em>&nbsp;
                </div>
                <div className='leftText'>                   
                    <button id={id} className="btn btn-secondary btn-lyrics" type="button" onClick={props.handlePreviewClick}>Lyrics</button>
                    
                    <Button className='btn-analyze' variant="primary" onClick={props.handleAnalyzeClick(id)}>Analyze</Button>
                </div>
                {/* This only appears when user clicks Tell me More. */}
                {/* <Modal size="lg" show={props.showModal} onHide={props.handleClose} aria-labelledby="SongFeels explanation">
                    <Modal.Header closeButton>
                        <Modal.Title>Explanation:</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <p></p>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={props.handleClose}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal> */}
            </div>
        );
    }

    return (
        <section className='section2'>
            <h2>We found {props.listOfSongs.length} results:</h2>

            {
                props.listOfSongs.length < 1
                ? <h3>Please try again!</h3>
                : <div>
                        {songElements}
                </div>
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
                        <Button variant="primary" onClick={props.handleAnalyzeClick(props.selectedSong)}>Analyze</Button>
                    </form>
                </>
            }
        </section>
    );
}

export default SearchResults;
