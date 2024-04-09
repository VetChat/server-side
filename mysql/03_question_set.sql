SET NAMES 'utf8mb4';
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
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Insert mock data into the question_set table
INSERT INTO question_set
VALUES -- สุนัข
       (1, 1, 1),
       (2, 2, 1),
       (3, 3, 1),
       (4, 4, 1),
       (5, 5, 1),
       -- แมว
       (6, 1, 2),
       (7, 2, 2),
       (8, 3, 2),
       (9, 4, 2),
       (10, 5, 2);
