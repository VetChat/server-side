-- CREATE the ticket table
CREATE TABLE IF NOT EXISTS ticket
(
    ticket_id        INT          NOT NULL,
    animal_id        INT          NOT NULL,
    sex              ENUM ('male', 'female'),
    sterilize        ENUM ('sterile', 'non-sterile'),
    breed            VARCHAR(255) NOT NULL,
    birth_when       DATETIME     NOT NULL,
    rec_created_when DATETIME     NOT NULL DEFAULT CURRENT_DATE(),
    PRIMARY KEY (ticket_id),
    CONSTRAINT FK_TicketAnimal FOREIGN KEY (animal_id) REFERENCES animal (animal_id)
)