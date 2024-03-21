-- Create the ticket answer table
CREATE TABLE IF NOT EXISTS ticket_answer
(
    ticket_answer_id   INT AUTO_INCREMENT,
    ticket_question_id INT          NOT NULL,
    ticket_answer      VARCHAR(255) NOT NULL,
    PRIMARY KEY (ticket_answer_id),
    CONSTRAINT FK_TicketAnswer FOREIGN KEY (ticket_question_id) REFERENCES ticket_question (ticket_question_id) ON DELETE CASCADE
);

-- Insert mock data to the ticket answer table
INSERT INTO ticket_answer
VALUES (1, 2, 'Male'),
       (2, 2, 'Female'),
       (3, 3, 'Sterile'),
       (4, 3, 'Non-Sterile')