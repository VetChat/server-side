-- CREATE the answer record table
CREATE TABLE IF NOT EXISTS answer_record
(
    answer_record_id INT AUTO_INCREMENT,
    ticket_id        INT          NOT NULL,
    symptom_id       INT          NOT NULL,
    symptom_name     VARCHAR(255) NOT NULL,
    question         VARCHAR(255) NOT NULL,
    image_path       VARCHAR(255),
    ordinal          INT          NOT NULL,
    answer           VARCHAR(255) NOT NULL,
    summary          VARCHAR(255),
    PRIMARY KEY (answer_record_id),
    CONSTRAINT FK_AnswerRecordTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id) ON DELETE CASCADE,
    CONSTRAINT UC_AnswerTicket UNIQUE (ticket_id, question)
);

-- Insert mock data to the answer record table
INSERT INTO answer_record
VALUES (1, 1, 1, 'Diarrhea', 'First Question', NULL, 1, 'no', NULL),
       (2, 1, 1, 'Diarrhea', 'Third Question', NULL, 3, '<14', 'advance diarrhea'),
       (3, 1, 1, 'Diarrhea', 'Fourth Question', NULL, 4, 'yes', NULL),
       (4, 2, 2, 'Vomit', 'First Question', NULL, 1, 'liquid', NULL),
       (5, 2, 2, 'Vomit', 'Third Question', NULL, 3, 'yes', NULL),
       (6, 2, 2, 'Vomit', 'Fourth Question', NULL, 4, 'Mage', NULL),
       (7, 3, 3, 'Loss of appetite', 'First Question', NULL, 1, 'no', NULL),
       (8, 3, 3, 'Loss of appetite', 'Second Question', NULL, 2, 'yes', NULL),
       (9, 3, 3, 'Loss of appetite', 'Third Question', NULL, 3, 'no', NULL),
       (10, 3, 3, 'Loss of appetite', 'Fourth Question', NULL, 4, 'no', NULL);
