-- CREATE the response table
CREATE TABLE IF NOT EXISTS response
(
    response_id INT AUTO_INCREMENT,
    ticket_id   INT NOT NULL,
    answer_id   INT NOT NULL,
    PRIMARY KEY (response_id),
    CONSTRAINT FK_ResponseTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id),
    CONSTRAINT FK_ResponseAnswer FOREIGN KEY (answer_id) REFERENCES answer (answer_id)
)