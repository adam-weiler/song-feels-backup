// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Card from 'react-bootstrap/Card';

// Call stylesheet last:
import './EmojiCard.css';

export default function EmojiCard(props) {
    return (
        <Card>
            <Card.Img variant="top" src={props.emotionImage} />
            <Card.Body>
            <Card.Title>{props.emotionText}</Card.Title>
            <Card.Text>
                {props.emotionPercent}
            </Card.Text>
            </Card.Body>
        </Card>
    )
}
