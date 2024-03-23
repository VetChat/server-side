-- Create the animal table
CREATE TABLE IF NOT EXISTS animal
(
    animal_id   INT          NOT NULL AUTO_INCREMENT,
    animal_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id),
    CONSTRAINT UC_Animal UNIQUE (animal_name),
    INDEX idx_animal_name (animal_name)
);

-- Insert mock data into the animal table
INSERT INTO animal
VALUES (1, 'Dog'),
       (2, 'Cat'),
       (3, 'Rabbit');