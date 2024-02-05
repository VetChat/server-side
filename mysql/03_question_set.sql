-- CREATE the question set table
CREATE TABLE IF NOT EXISTS question_set
(
    question_set_id INT AUTO_INCREMENT,
    symptom_id      INT NOT NULL,
    animal_id       INT NOT NULL,
    PRIMARY KEY (question_set_id),
    CONSTRAINT FK_SymptomQuestion FOREIGN KEY (symptom_id) REFERENCES symptom (symptom_id),
    CONSTRAINT FK_AnimalQuestion FOREIGN KEY (animal_id) REFERENCES animal (animal_id)
)