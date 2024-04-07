-- Create the ticket question table
CREATE TABLE IF NOT EXISTS ticket_question
(
    ticket_question_id INT AUTO_INCREMENT,
    ticket_question    VARCHAR(255) NOT NULL,
    pattern            ENUM ('text', 'choice', 'birthDate'),
    ordinal            INT          NOT NULL,
    is_required        BOOLEAN      NOT NULL DEFAULT TRUE,
    PRIMARY KEY (ticket_question_id)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;;

-- Insert mock data into the ticket question table
INSERT INTO ticket_question
VALUES (1, 'Pet ID', 'text', 1, TRUE),
       (2, 'Sex', 'choice', 2, TRUE),
       (3, 'Neutered or not neutered', 'choice', 3, TRUE),
       (4, 'Breed', 'text', 4, FALSE),
       (5, 'Birthdate', 'birthDate', 5, TRUE)