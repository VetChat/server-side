-- Create the symptom table
CREATE TABLE IF NOT EXISTS symptom
(
    symptom_id   INT          NOT NULL AUTO_INCREMENT,
    symptom_name varchar(255) NOT NULL,
    PRIMARY KEY (symptom_id),
    CONSTRAINT UC_Symptom UNIQUE (symptom_name)
);

-- Insert mock data into the symptom table
INSERT INTO symptom
VALUES (1, 'Diarrhea'),
       (2, 'Vomit'),
       (3, 'Loss of appetite');