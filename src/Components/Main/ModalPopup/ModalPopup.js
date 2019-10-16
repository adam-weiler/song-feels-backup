// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

// Call stylesheet last:
import './ModalPopup.css';

const ModalPopup = (props) => {
    return (
        <Modal size="lg" show={props.showModal} onHide={props.handleClose} aria-labelledby="SongFeels explanation">
            <Modal.Header closeButton>
                <Modal.Title>{props.modalTitle}:</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {
                    !props.modalBody
                    ? <>
                    <p><em>SongFeels</em> uses the <a href='https://audd.io/' target='_blank' rel="noopener noreferrer" >AudD Music Recognition API</a> to search for the user's song and lyrics.</p>
                    <p>Before touching the database, the lyrics are cleaned by removing symbols, numbers, common words, and duplicate words. This reduces most word counts significantly.</p>
                    <p>The cleaned lyrics are compared to the <a href='http://crr.ugent.be/archives/1003' target='_blank' rel="noopener noreferrer" >Warringer and Kuperman database</a> of 13,915 English words. Any lyrics that are found in the database are stored with their Valence, Arousal, Dominance score which is between 0 (low) and 10 (high).</p>
                    <ul>
                        <li>Valence is how negative or positive the word is viewed.</li>
                        <li>Arousal is how boring or exciting the word is viewed.</li>
                        <li>Dominance is how powerless or in control the word feels.</li>
                    </ul>
                    <p>Each of the lyrics that was found in the database is run through my algorithm, which looks at the 3 VAD scores and assigns a basic emotion to the word; Anger, Bored, Excited, Fear, Happy, or Sad.</p>
                    </>
                    : <>
                        <h2>"{props.modalBody['title']}" by <em>{props.modalBody['artist']}</em>:</h2>
                        <p className='original-lyrics'>{props.modalBody['lyrics']}</p>
                    </>
                }
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default ModalPopup;
