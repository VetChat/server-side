-- Create the ticket answer record table
CREATE TABLE IF NOT EXISTS ticket_answer_record
(
    ticket_answer_record_id INT AUTO_INCREMENT,
    ticket_id               INT          NOT NULL,
    ticket_question         VARCHAR(255) NOT NULL,
    ordinal                 INT          NOT NULL,
    ticket_answer           VARCHAR(255) NOT NULL,
    PRIMARY KEY (ticket_answer_record_id),
    CONSTRAINT FK_TicketAnswerRecordTicket FOREIGN KEY (ticket_id) REFERENCES ticket (ticket_id) ON DELETE CASCADE,
    CONSTRAINT UC_TicketAnswerTicket UNIQUE (ticket_id, ticket_question)
);

-- Mock data to the ticket answer record table
INSERT INTO ticket_answer_record
VALUES (1, 1, 'Pet ID', 1, '1234'),
       (2, 1, 'Sex', 2, 'Male'),
       (3, 1, 'Neutered or not neutered', 3, 'Sterile'),
       (4, 1, 'Breed', 4, 'Golden Retriever'),
       (5, 1, 'Birthdate', 5, '2022-02-01'),
       (6, 2, 'Pet ID', 1, '1454'),
       (7, 2, 'Sex', 2, 'Male'),
       (8, 2, 'Neutered or not neutered', 3, 'Non-Sterile'),
       (9, 2, 'Breed', 4, 'Bulldog'),
       (10, 2, 'Birthdate', 5, '2021-10-01'),
       (11, 3, 'Pet ID', 1, '1111'),
       (12, 3, 'Sex', 2, 'Female'),
       (13, 3, 'Neutered or not neutered', 3, 'Sterile'),
       (14, 3, 'Breed', 4, 'Golden Retriever'),
       (15, 3, 'Birthdate', 5, '2024-04-04')