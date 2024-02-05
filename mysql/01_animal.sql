-- Create the animal table
CREATE TABLE IF NOT EXISTS animal
(
    animal_id INT AUTO_INCREMENT,
    name      VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id)
);