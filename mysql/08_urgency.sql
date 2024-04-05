-- CREATE the urgency table
CREATE TABLE IF NOT EXISTS urgency
(
    urgency_id     INT          NOT NULL AUTO_INCREMENT,
    urgency_detail VARCHAR(255) NOT NULL,
    duration       VARCHAR(255) NOT NULL,
    urgency_level  INT          NOT NULL,
    PRIMARY KEY (urgency_id),
    CONSTRAINT UC_Urgency UNIQUE (urgency_detail, duration, urgency_level)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;;

-- Insert mock data into the urgency table
INSERT INTO urgency
VALUES (1, 'Dead', '0 min', 1),
       (2, 'Almost Dead', '1-5 min', 2),
       (3, 'Will Die soon', '5-10 min', 3);