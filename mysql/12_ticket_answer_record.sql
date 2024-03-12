-- Create the ticket answer record table
CREATE TABLE IF NOT EXISTS ticket_answer_record
(
    ticket_answer_record_id INT AUTO_INCREMENT,
    ticket_id               INT          NOT NULL,
    ticket_question_id      INT          NOT NULL,
    ticket_answer           VARCHAR(255) NOT NULL,
    PRIMARY KEY (ticket_answer_record_id),
    CONSTRAINT FK_TicketAnswerRecordTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id),
    CONSTRAINT FK_TicketAnswerRecordQuestion FOREIGN KEY (ticket_question_id) REFERENCES ticket_question (ticket_question_id),
    CONSTRAINT UC_TicketAnswerTicket UNIQUE (ticket_id, ticket_answer)
);

-- Mock data to the ticket answer record table
INSERT INTO ticket_answer_record
VALUES (1, 1, 1, '1234'),
       (2, 1, 2, 'Male'),
       (3, 1, 3, 'Sterile'),
       (4, 1, 4, 'Golden Retriever'),
       (5, 1, 5, '2022-02-01'),
       (6, 2, 1, '1454'),
       (7, 2, 2, 'Male'),
       (8, 2, 3, 'Non-Sterile'),
       (9, 2, 4, 'Bulldog'),
       (10, 2, 5, '2021-10-01'),
       (11, 3, 1, '1111'),
       (12, 3, 2, 'Female'),
       (13, 3, 3, 'Sterile'),
       (14, 3, 4, 'Golden Retriever'),
       (15, 3, 5, '2024-04-04')