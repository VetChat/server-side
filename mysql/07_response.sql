-- CREATE the response table
CREATE TABLE IF NOT EXISTS response
(
    response_id INT AUTO_INCREMENT,
    ticket_id   INT NOT NULL,
    answer_id   INT NOT NULL,
    PRIMARY KEY (response_id),
    CONSTRAINT FK_ResponseTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id),
    CONSTRAINT FK_ResponseAnswer FOREIGN KEY (answer_id) REFERENCES answer (answer_id)
);

-- Insert mock data to the response table
INSERT INTO response
VALUES (1, 1, 2),
       (2, 1, 5),
       (3, 1, 7),
       (4, 2, 10),
       (5, 2, 14),
       (6, 2, 16),
       (7, 3, 22),
       (8, 3, 23),
       (8, 3, 26),
       (8, 3, 28);
