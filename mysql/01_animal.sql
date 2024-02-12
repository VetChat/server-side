-- Create the animal table
CREATE TABLE IF NOT EXISTS animal
(
    animal_id INT          NOT NULL AUTO_INCREMENT,
    name      VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id),
    CONSTRAINT UC_Animal UNIQUE (name)
);

-- Insert mock data into the animal table
INSERT INTO animal
VALUES (1, 'Dog'),
       (2, 'Cat'),
       (3, 'Rabbit');