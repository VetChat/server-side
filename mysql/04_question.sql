-- Create the question table
CREATE TABLE IF NOT EXISTS question
(
    question_id     INT AUTO_INCREMENT,
    question_set_id INT          NOT NULL,
    question        VARCHAR(255) NOT NULL,
    pattern         ENUM ('choice', 'yes/no', 'duration'),
    image_path      VARCHAR(255),
    ordinal         INT          NOT NULL,
    PRIMARY KEY (question_id),
    INDEX idx_question_set_id (question_set_id),
    CONSTRAINT FK_QuestionSet FOREIGN KEY (question_set_id) REFERENCES question_set (question_set_id) ON DELETE CASCADE
);

-- Insert mock data into the question table
INSERT INTO question
VALUES (1, 1, 'First Question', 'yes/no', NULL, 1),
       (2, 1, 'Second Question', 'yes/no', NULL, 2),
       (3, 1, 'Third Question', 'duration', NULL, 3),
       (4, 1, 'Fourth Question', 'yes/no', NULL, 4),
       (5, 2, 'First Question', 'choice', NULL, 1),
       (6, 2, 'Second Question', 'duration', NULL, 2),
       (7, 2, 'Third Question', 'yes/no', NULL, 3),
       (8, 2, 'Fourth Question', 'choice', NULL, 4),
       (9, 3, 'First Question', 'yes/no', NULL, 1),
       (10, 3, 'Second Question', 'yes/no', NULL, 2),
       (11, 3, 'Third Question', 'yes/no', NULL, 3),
       (12, 3, 'Fourth Question', 'yes/no', NULL, 4),
       (13, 3, 'Fifth Question', 'yes/no', NULL, 5),
       (14, 4, 'First Question', 'yes/no', NULL, 1),
       (15, 4, 'Second Question', 'choice', NULL, 2),
       (16, 4, 'Third Question', 'yes/no', NULL, 3),
       (17, 4, 'Fourth Question', 'yes/no', NULL, 4),
       (18, 5, 'First Question', 'duration', NULL, 1),
       (19, 5, 'Second Question', 'duration', NULL, 2),
       (20, 5, 'Third Question', 'duration', NULL, 3),
       (21, 6, 'First Question', 'choice', NULL, 1),
       (22, 6, 'Second Question', 'choice', NULL, 2),
       (23, 6, 'Third Question', 'choice', NULL, 3);
