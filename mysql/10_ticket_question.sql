-- Create the ticket question table
CREATE TABLE IF NOT EXISTS ticket_question
(
    ticket_question_id INT AUTO_INCREMENT,
    ticket_question    VARCHAR(255) NOT NULL,
    pattern            ENUM ('text', 'choice', 'birthDate'),
    ordinal            INT          NOT NULL,
    PRIMARY KEY (ticekt_question_id)
);

-- Insert mock data into the ticket question table
INSERT INTO ticket_question
VALUES (1, 'Pet ID', 'text', 1),
       (2, 'Sex', 'choice', 2),
       (3, 'Neutered or not neutered', 'choice', 3),
       (4, 'Breed', 'text', 4),
       (5, 'Birthdate', 'birthDate', 5)