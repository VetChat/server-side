SET NAMES 'utf8mb4';
-- Create the animal table
CREATE TABLE IF NOT EXISTS animal
(
    animal_id   INT          NOT NULL AUTO_INCREMENT,
    animal_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (animal_id),
    CONSTRAINT UC_Animal UNIQUE (animal_name),
    INDEX idx_animal_name (animal_name)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Insert mock data into the animal table
INSERT INTO animal
VALUES (1, 'หมา'),
       (2, 'แมว');
