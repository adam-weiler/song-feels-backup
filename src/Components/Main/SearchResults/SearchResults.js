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
            (elem, id) => <div key={elem.song_id} className='search-results'>
                <div className='rightText'>
                    "{elem.title}" by <em>{elem.artist}</em>&nbsp;
                </div>
                <div className='leftText'>                                     
                    <Button className='btn-lyrics' variant="secondary" onClick={props.handleShow('Lyrics', props.listOfSongs[id])}>Lyrics</Button>

                    <Button className='btn-analyze' variant="primary" onClick={props.handleAnalyzeClick(id)}>Analyze</Button>
                    {/* <Form.Check type="checkbox" label="Ignore Repeated Words" /> */}
                </div>
            </div>
        );
    }

    return (
        <section className='section2'>
            <h2>We found {props.listOfSongs.length} results:</h2>

            {
                props.listOfSongs.length < 1  // If there are no songs, display nothing.
                ? <h3>Please try again!</h3>
                : <div>  {/* Else display search results, Lyrics buttons, and Analyze buttons. */}
                        {songElements}
                </div>
            }
        </section>
    );
}

export default SearchResults;
