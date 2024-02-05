-- Create the symptom table
CREATE TABLE IF NOT EXISTS symptom
(
    symptom_id   INT AUTO_INCREMENT,
    symptom_name varchar(255) NOT NULL,
    PRIMARY KEY (symptom_id)
)