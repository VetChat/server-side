-- CREATE the urgent case table
CREATE TABLE IF NOT EXISTS urgent_case
(
    urgent_id   INT          NOT NULL AUTO_INCREMENT,
    urgent_name VARCHAR(255) NOT NULL,
    urgency_id  INT          NOT NULL,
    animal_id   INT          NOT NULL,
    PRIMARY KEY (urgent_id),
    CONSTRAINT UC_Urgent UNIQUE (urgent_name, animal_id),
    CONSTRAINT FK_UrgencyUrgent FOREIGN KEY (urgency_id) REFERENCES urgency (urgency_id),
    CONSTRAINT FK_AnimalUrgent FOREIGN KEY (animal_id) REFERENCES animal (animal_id)
);

-- Insert mock data into the urgent_case table
INSERT INTO urgent_case
VALUES (1, 'Shock', 3, 1),
       (2, 'Heat Stork', 2, 1),
       (3, 'Heart Attack', 1, 1),
       (4, 'Heat Stork', 3, 2),
       (5, 'Addicted to Weed', 3, 2),
       (6, 'Depression', 3, 3);
