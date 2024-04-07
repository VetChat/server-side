-- CREATE the ticket table
CREATE TABLE IF NOT EXISTS ticket
(
    ticket_id        INT          NOT NULL AUTO_INCREMENT,
    animal           VARCHAR(255) NOT NULL,
    rec_created_when DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_answered      BOOLEAN      NOT NULL DEFAULT FALSE,
    PRIMARY KEY (ticket_id)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;;

-- Insert mock data to the ticket table
INSERT INTO ticket
VALUES (1, 'Dog', '2024-02-06 15:35:44', FALSE),
       (2, 'Dog', '2024-02-07 08:12:35', FALSE),
       (3, 'Dog', '2024-02-09 15:53:59', FALSE);

