-- Create the animal table
CREATE TABLE IF NOT EXISTS animal
(
    animal_id INT          NOT NULL AUTO_INCREMENT,
    name      VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id)
);

-- Insert mock data into the animal table
INSERT INTO animal
VALUES (1, 'หมา'),
       (2, 'แมว'),
       (3, 'กระต่าย');