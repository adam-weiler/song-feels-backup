// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Spinner from 'react-bootstrap/Spinner';

// Call stylesheet last:
import './LoadingWheel.css';

const LoadingWheel = () => {
    return (
        <div class='spinnerContainer'>
            <Spinner animation="border" role="status">
                <span className="sr-only">Loading...</span>
            </Spinner>
            <br/>
            Loading...
        </div>
    );
}

export default LoadingWheel;
