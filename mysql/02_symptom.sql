-- Create the symptom table
CREATE TABLE IF NOT EXISTS symptom
(
    symptom_id   INT          NOT NULL AUTO_INCREMENT,
    symptom_name varchar(255) NOT NULL,
    PRIMARY KEY (symptom_id),
    CONSTRAINT UC_Symptom UNIQUE (symptom_name)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;;

-- Insert mock data into the symptom table
INSERT INTO symptom
VALUES (1, 'ท้องเสีย'),
       (2, 'ไอ'),
       (3, 'เหงือกซีด'),
       (4, 'ขนร่วง'),
       (5, 'อึไม่ออก');