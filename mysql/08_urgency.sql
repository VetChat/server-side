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
VALUES (1, 'ฉุกเฉินถึงแก่ชีวิต', 'ได้รับการตรวจทันที', 1),
       (2, 'ฉุกเฉินเร่งด่วน', 'สามารถรอได้ 5 - 15 นาที', 2),
       (3, 'ฉุกเฉิน (ไม่รุนแรง)', 'สามารถรอได้ 30 นาที', 3),
       (4, 'ไม่ฉุกเฉิน', 'ได้รับการพิจารณาใหม่ทุก 1 - 2 ชั่วโมง', 4);