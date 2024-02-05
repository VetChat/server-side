-- CREATE the answer table
CREATE TABLE IF NOT EXISTS answer
(
    answer_id   INT AUTO_INCREMENT,
    question_id INT          NOT NULL,
    answer      VARCHAR(255) NOT NULL,
    summary     VARCHAR(255),
    skip_to     INT,
    PRIMARY KEY (answer_id),
    CONSTRAINT FK_QuestionAnswer FOREIGN KEY (question_id) REFERENCES question (question_id)
)