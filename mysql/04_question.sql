-- Create the question table
CREATE TABLE IF NOT EXISTS question
(
    question_id     INT AUTO_INCREMENT,
    question_set_id INT  NOT NULL,
    question        TEXT NOT NULL,
    pattern         ENUM ('choice', 'yes/no', 'duration'),
    image_path      VARCHAR(255),
    ordinal         INT  NOT NULL,
    PRIMARY KEY (question_id),
    CONSTRAINT FK_QuestionSet FOREIGN KEY (set_id) REFERENCES question_set (set_id)
);