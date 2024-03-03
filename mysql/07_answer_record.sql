-- CREATE the answer record table
CREATE TABLE IF NOT EXISTS answer_record
(
    answer_record_id INT AUTO_INCREMENT,
    ticket_id        INT NOT NULL,
    answer_id        INT NOT NULL,
    PRIMARY KEY (answer_record_id),
    CONSTRAINT FK_AnswerRecordTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id),
    CONSTRAINT FK_AnswerRecordAnswer FOREIGN KEY (answer_id) REFERENCES answer (answer_id),
    CONSTRAINT UC_AnswerTicket UNIQUE (ticket_id, answer_id)
);

-- Insert mock data to the answer record table
INSERT INTO answer_record
VALUES (1, 1, 2),
       (2, 1, 5),
       (3, 1, 7),
       (4, 2, 10),
       (5, 2, 14),
       (6, 2, 16),
       (7, 3, 22),
       (8, 3, 23),
       (9, 3, 26),
       (10, 3, 28);
