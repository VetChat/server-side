-- CREATE the answer table
CREATE TABLE IF NOT EXISTS answer
(
    answer_id        INT AUTO_INCREMENT,
    question_id      INT          NOT NULL,
    answer           VARCHAR(255) NOT NULL,
    summary          VARCHAR(255),
    skip_to_question INT,
    PRIMARY KEY (answer_id),
    CONSTRAINT FK_QuestionAnswer FOREIGN KEY (question_id) REFERENCES question (question_id) ON DELETE CASCADE
);

-- Insert mock data to the answer table
INSERT INTO answer
VALUES (1, 1, 'yes', NULL, NULL),
       (2, 1, 'no', NULL, 3),
       (3, 2, 'yes', NULL, NULL),
       (4, 2, 'no', NULL, NULL),
       (5, 3, '<14', 'simple diarrhea', NULL),
       (6, 3, '>=14', 'advance diarrhea', NULL),
       (7, 4, 'yes', NULL, NULL),
       (8, 4, 'no', NULL, NULL),
       (9, 5, 'solid', NULL, NULL),
       (10, 5, 'liquid', NULL, 7),
       (11, 5, 'gas', NULL, NULL),
       (12, 6, '>10', NULL, NULL),
       (13, 6, '<=10', NULL, NULL),
       (14, 7, 'yes', NULL, NULL),
       (15, 7, 'no', NULL, NULL),
       (16, 8, 'Mage', NULL, NULL),
       (17, 8, 'Warrior', NULL, NULL),
       (18, 8, 'Thief', NULL, NULL),
       (19, 8, 'Archer', NULL, NULL),
       (20, 8, 'Healer', NULL, NULL),
       (21, 9, 'yes', NULL, 11),
       (22, 9, 'no', NULL, NULL),
       (23, 10, 'yes', NULL, NULL),
       (24, 10, 'no', NULL, 12),
       (25, 11, 'yes', NULL, 0),
       (26, 11, 'no', NULL, NULL),
       (27, 12, 'yes', NULL, NULL),
       (28, 12, 'no', NULL, 0),
       (29, 13, 'yes', NULL, NULL),
       (30, 13, 'no', NULL, NULL),
       (31, 14, 'yes', NULL, NULL),
       (32, 14, 'no', NULL, NULL),
       (33, 15, 'Very Happy', NULL, NULL),
       (34, 15, 'Happy', NULL, NULL),
       (35, 15, 'Good', NULL, NULL),
       (36, 15, 'Not Good', NULL, NULL),
       (37, 15, 'Bad', 'Holy Moly!!', 0),
       (38, 16, 'yes', NULL, NULL),
       (39, 16, 'no', NULL, NULL),
       (40, 17, 'yes', NULL, NULL),
       (41, 17, 'no', NULL, NULL),
       (42, 18, '>7', NULL, NULL),
       (43, 18, '<=7', NULL, NULL),
       (44, 19, '<6', NULL, NULL),
       (45, 19, '6-9', NULL, NULL),
       (46, 19, '>9', NULL, NULL),
       (47, 20, '1-4', 'Don\'t care', NULL),
       (48, 20, '4-7', 'Have to take a look', NULL),
       (49, 20, '7-15', 'Please take care', NULL),
       (50, 20, '15-30', 'Take a Rest', NULL),
       (51, 20, '>30', 'RIP', NULL),
       (52, 21, 'Drama', 'FameX', NULL),
       (53, 21, 'Not Drama', 'Ignorance', NULL),
       (54, 21, 'Normal', 'Just Normal Person', 0),
       (55, 22, 'Facebook', 'Mark', NULL),
       (56, 22, 'X', 'Elon', NULL),
       (57, 22, 'Instagram', 'Mark', NULL),
       (58, 22, 'Youtube', '3 Guys', NULL),
       (59, 22, 'Twitch', 'Justin', NULL),
       (60, 22, 'Discord', 'Jason', NULL),
       (61, 23, 'Communist', NULL, NULL),
       (62, 23, 'Monarchy', NULL, NULL);

