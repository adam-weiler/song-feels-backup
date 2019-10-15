// Vanilla React:
import React from 'react';

// Bootstrap-React components:
import Card from 'react-bootstrap/Card';

// Call stylesheet last:
import './EmojiCard.css';

const EmojiCard = (props) => {
    return (
        <Card>
            <Card.Img variant="top" src={props.emotionImage} />
            <Card.Body>
                <Card.Title>{props.emotionName}</Card.Title>
                <Card.Text>
                    {props.emotionPercent}
                </Card.Text>
                <Card.Text>
                    <span className="text-muted">{props.emotionSum} words</span>
                </Card.Text>
            </Card.Body>
        </Card>
    );
}

export default EmojiCard;
