-- CREATE the ticket table
CREATE TABLE IF NOT EXISTS ticket
(
    ticket_id        INT          NOT NULL AUTO_INCREMENT,
    animal_id        INT          NOT NULL,
    sex              ENUM ('male', 'female'),
    sterilize        ENUM ('sterile', 'non-sterile'),
    breed            VARCHAR(255) NOT NULL,
    birth_when       DATETIME     NOT NULL,
    rec_created_when DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_answered      INT          NOT NULL DEFAULT 0,
    PRIMARY KEY (ticket_id),
    CONSTRAINT FK_TicketAnimal FOREIGN KEY (animal_id) REFERENCES animal (animal_id)
);

-- Insert mock data to the ticket table
INSERT INTO ticket
VALUES (1, 1, 'male', 'sterile', 'Husky', '2012-03-07 00:00:00', '2024-02-06 15:35:44', 1),
       (2, 1, 'male', 'sterile', 'Bull dog', '2024-11-24 00:00:00', '2024-02-07 08:12:35', 1),
       (3, 1, 'female', 'non-sterile', 'Shiba', '2019-05-15 00:00:00', '2024-02-09 15:53:59', 1);

