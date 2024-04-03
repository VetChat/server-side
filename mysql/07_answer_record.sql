-- CREATE the answer record table
CREATE TABLE IF NOT EXISTS answer_record
(
    answer_record_id INT AUTO_INCREMENT,
    ticket_id        INT          NOT NULL,
    question         VARCHAR(255) NOT NULL,
    answer           VARCHAR(255) NOT NULL,
    summary          VARCHAR(255),
    PRIMARY KEY (answer_record_id),
    CONSTRAINT FK_AnswerRecordTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id) ON DELETE CASCADE,
    CONSTRAINT UC_AnswerTicket UNIQUE (ticket_id, question)
);

-- Insert mock data to the answer record table
INSERT INTO answer_record
VALUES (1, 1, 'First Question', 'no', NULL),
       (2, 1, 'Third Question', '<14', 'advance diarrhea'),
       (3, 1, 'Fourth Question', 'yes', NULL),
       (4, 2, 'First Question', 'liquid', NULL),
       (5, 2, 'Third Question', 'yes', NULL),
       (6, 2, 'Fourth Question', 'Mage', NULL),
       (7, 3, 'First Question', 'no', NULL),
       (8, 3, 'Second Question', 'yes', NULL),
       (9, 3, 'Third Question', 'no', NULL),
       (10, 3, 'Fourth Question', 'no', NULL);
