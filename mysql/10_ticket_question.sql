SET NAMES 'utf8mb4';
-- Create the ticket question table
CREATE TABLE IF NOT EXISTS ticket_question
(
    ticket_question_id INT AUTO_INCREMENT,
    ticket_question    VARCHAR(255) NOT NULL,
    pattern            ENUM ('text', 'choice', 'birthDate'),
    ordinal            INT          NOT NULL,
    is_required        BOOLEAN      NOT NULL DEFAULT TRUE,
    is_default         BOOLEAN      NOT NULL DEFAULT FALSE,
    is_editable        BOOLEAN      NOT NULL DEFAULT FALSE,
    PRIMARY KEY (ticket_question_id)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Insert mock data into the ticket question table
INSERT INTO ticket_question
VALUES (1, 'รหัสประจำสัตว์เลี้ยง', 'text', 1, FALSE, TRUE, TRUE),
       (2, 'เพศ', 'choice', 2, TRUE, TRUE, FALSE),
       (3, 'ทำหมัน หรือไม่ทำหมัน', 'choice', 3, TRUE, TRUE, FALSE),
       (4, 'พันธุ์', 'breed', 4, TRUE, TRUE, FALSE),
       (5, 'วันเกิด', 'birthDate', 5, TRUE, TRUE, FALSE);
