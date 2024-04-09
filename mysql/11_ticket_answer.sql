SET NAMES 'utf8mb4';
-- Create the ticket answer table
CREATE TABLE IF NOT EXISTS ticket_answer
(
    ticket_answer_id   INT AUTO_INCREMENT,
    ticket_question_id INT          NOT NULL,
    ticket_answer      VARCHAR(255) NOT NULL,
    PRIMARY KEY (ticket_answer_id),
    CONSTRAINT FK_TicketAnswer FOREIGN KEY (ticket_question_id) REFERENCES ticket_question (ticket_question_id) ON DELETE CASCADE
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Insert mock data to the ticket answer table
INSERT INTO ticket_answer
VALUES (1, 2, 'ผู้'),
       (2, 2, 'เมีย'),
       (3, 3, 'ทำหมัน'),
       (4, 3, 'ไม่ทำหมัน');