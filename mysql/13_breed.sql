SET NAMES 'utf8mb4';
-- Create the breed table
CREATE TABLE IF NOT EXISTS breed
(
    breed_id   INT          NOT NULL AUTO_INCREMENT,
    breed_name VARCHAR(255) NOT NULL,
    animal_id  INT          NOT NULL,
    PRIMARY KEY (breed_id),
    CONSTRAINT FK_BreedAnimal FOREIGN KEY (animal_id) REFERENCES animal (animal_id) ON DELETE CASCADE,
    CONSTRAINT UC_Animal UNIQUE (breed_name),
    INDEX idx_animal_name (breed_name)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Insert mock data into the animal table
INSERT INTO breed
VALUES (1, 'โกลเด้นรีทรีฟเวอร์', 1),
       (2, 'บลูด็อก', 1);
