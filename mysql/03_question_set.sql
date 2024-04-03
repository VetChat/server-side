-- CREATE the question set table
CREATE TABLE IF NOT EXISTS question_set
(
    question_set_id INT NOT NULL AUTO_INCREMENT,
    symptom_id      INT NOT NULL,
    animal_id       INT NOT NULL,
    PRIMARY KEY (question_set_id),
    CONSTRAINT FK_SymptomQuestion FOREIGN KEY (symptom_id) REFERENCES symptom (symptom_id) ON DELETE CASCADE,
    CONSTRAINT FK_AnimalQuestion FOREIGN KEY (animal_id) REFERENCES animal (animal_id) ON DELETE CASCADE,
    CONSTRAINT UC_QuestionSet UNIQUE (symptom_id, animal_id)
);

-- Insert mock data into the question_set table
INSERT INTO question_set
VALUES (1, 1, 1),
       (2, 2, 1),
       (3, 3, 1),
       (4, 1, 2),
       (5, 3, 2),
       (6, 2, 3);