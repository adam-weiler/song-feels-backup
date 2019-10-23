// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import CSRFToken from '../csrftoken.js'

// Call stylesheet last:
import './SearchForm.css';

const SearchForm = (props) => {
    return (
        <Form>
            {/* {% csrf_token %} */}
            {/* <CSRFToken /> */}
            
            <Form.Group controlId='songInput'>
                <Form.Label>Enter the name of the song you want to search for:</Form.Label>
                <Form.Control type='text' name='songInput' placeholder='Song name' required />
                <CSRFToken/>
                <Form.Control.Feedback type="invalid">
                    Please provide a valid song title.
                </Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId='artistInput'>
                <Form.Label>Enter the name of the band or artist:</Form.Label>
                <Form.Control type='text' name='artistInput' placeholder='Artist name (optional)' />
            </Form.Group>
            <Button variant='primary' type='submit' onClick={props.handleSearchClick} >
                Search
            </Button>

            {
                !props.errorMessage
                ? ''
                : <Alert variant='danger'>{props.errorMessage}</Alert>
            }
        </Form>
    );
}

export default SearchForm;
