SET NAMES 'utf8mb4';
-- CREATE the answer table
CREATE TABLE IF NOT EXISTS answer
(
    answer_id        INT AUTO_INCREMENT,
    question_id      INT          NOT NULL,
    answer           VARCHAR(255) NOT NULL,
    summary          VARCHAR(255),
    skip_to_question INT,
    PRIMARY KEY (answer_id),
    CONSTRAINT FK_QuestionAnswer FOREIGN KEY (question_id) REFERENCES question (question_id) ON DELETE CASCADE,
    CONSTRAINT UC_Answer UNIQUE (question_id, answer),
    INDEX idx_answer (answer),
    INDEX idx_question_id (question_id)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
;
-- Insert mock data to the answer table
INSERT INTO answer
VALUES -- ท้องเสีย สุนัข
       -- Question No. 1
       (1, 1, '1', NULL, NULL),
       (2, 1, '2', NULL, NULL),
       (3, 1, '3', NULL, NULL),
       (4, 1, '4', NULL, NULL),
       (5, 1, '5', NULL, NULL),
       (6, 1, '6', NULL, NULL),
       (7, 1, '7', NULL, NULL),
       -- Question No. 2
       (8, 2, '<=14 วัน', 'Acute diarrhea', NULL),
       (9, 2, '>14 วัน', 'Chronic diarrhea', NULL),
       -- Question No. 3
       (10, 3, 'ใช่', NULL, NULL),
       (11, 3, 'ไม่', NULL, NULL),
       -- Question No. 4
       (12, 4, 'ใช่', NULL, NULL),
       (13, 4, 'ไม่', NULL, NULL),
       -- Question No. 5
       (14, 5, 'ใช่', NULL, NULL),
       (15, 5, 'ไม่', NULL, NULL),
       -- Question No. 6
       (16, 6, 'ใช่', NULL, NULL),
       (17, 6, 'ไม่', NULL, NULL),
       -- Question No. 7
       (18, 7, 'ใช่', NULL, NULL),
       (19, 7, 'ไม่', NULL, NULL),
       -- Question No. 8
       (20, 8, 'ใ่ช่', NULL, NULL),
       (21, 8, 'ไม่', NULL, NULL),
       -- Question No. 9
       (22, 9, 'ใช่', NULL, NULL),
       (23, 9, 'ไม่', NULL, NULL),
       -- Question No. 11
       (24, 11, 'ใช่', NULL, NULL),
       (25, 11, 'ไม่', NULL, NULL),
       -- Question No. 12
       (26, 12, 'ใช่', NULL, NULL),
       (27, 12, 'ไม่', NULL, NULL),
       -- ไอ สุนัข
       -- Question No. 1
       (28, 13, 'มี', NULL, NULL),
       (29, 13, 'ไม่มี', NULL, 15),
       -- Question No. 2
       (30, 15, 'ตลอดเวลา', NULL, NULL),
       (31, 15, 'มากกว่า 1 ชม./วัน', NULL, NULL),
       (32, 15, 'น้อยกว่า 1 ชม./วัน', NULL, NULL),
       -- Question No. 3
       (33, 16, 'ไอต่อเนื่อง', NULL, NULL),
       (34, 16, 'ไอแล้วหยุด', NULL, NULL),
       -- Question No. 4
       (35, 17, 'ใช่', NULL, NULL),
       (36, 17, 'ไม่ใช่', NULL, NULL),
       -- Question No. 5
       (37, 18, 'ครบ', NULL, NULL),
       (38, 18, 'ไม่ครบ', NULL, NULL),
       -- Question No. 6
       (39, 19, 'ทำ', NULL, NULL),
       (40, 19, 'ไม่ได้ทำ', NULL, NULL),
       -- Question No. 7
       (41, 20, 'มี', NULL, NULL),
       (42, 20, 'ไม่มี', NULL, NULL),
       -- Question No. 8
       (43, 21, 'มี', NULL, NULL),
       (44, 21, 'ไม่มี', NULL, NULL),
       -- เหงือกซีด สุนัข
       -- Question No. 1
       (45, 22, 'ครบ', NULL, NULL),
       (46, 22, 'ไม่ครบ', NULL, NULL),
       -- Question No. 2
       (47, 23, 'ทำ', NULL, NULL),
       (48, 23, 'ไม่ได้ทำ', NULL, NULL),
       -- Question No. 3
       (49, 24, 'มี', NULL, NULL),
       (50, 24, 'ไม่มี', NULL, NULL),
       -- Question No. 4
       (51, 25, 'มี', NULL, NULL),
       (52, 25, 'ไม่มี', NULL, NULL),
       -- Question No. 5
       (53, 26, 'มี', NULL, NULL),
       (54, 26, 'ไม่มี', NULL, NULL),
       -- Question No. 6
       (55, 27, 'มี', NULL, NULL),
       (56, 27, 'ไม่มี', NULL, NULL),
       -- ขนร่วง สุนัข
       -- Question No. 1
       (57, 28, 'ทำ', NULL, NULL),
       (58, 28, 'ไม่ได้ทำ', NULL, NULL),
       -- Question No. 2
       (59, 29, 'ใช่', NULL, NULL),
       (60, 29, 'ไม่ใช่', NULL, NULL),
       -- Question No. 3
       (61, 30, 'ใช่', NULL, NULL),
       (62, 30, 'ไม่ใช่', NULL, NULL),
       -- Question No. 4
       (63, 31, 'ใช่', NULL, NULL),
       (64, 31, 'ไม่ใช่', NULL, NULL),
       -- Question No. 5
       (65, 32, 'มี', NULL, NULL),
       (66, 32, 'ไม่มี', NULL, NULL),
       -- Question No. 6
       (67, 33, 'มี', NULL, NULL),
       (68, 33, 'ไม่มี', NULL, NULL),
       -- Question No. 7
       (69, 34, 'เช้า', NULL, NULL),
       (70, 34, 'กลางวัน', NULL, NULL),
       (71, 34, 'ดึก', NULL, NULL),
       (72, 34, 'ตลอดเวลา', NULL, NULL),
       (73, 34, 'ไม่มีอาการคัน', NULL, NULL),
       -- อึไม่ออก สุนัข
       -- Question No. 2
       (74, 36, 'ได้', NULL, NULL),
       (75, 36, 'ไม่ได้', NULL, NULL),
       -- Question No. 3
       (76, 37, 'มี', NULL, NULL),
       (77, 37, 'ไม่มี', NULL, NULL),
       -- Question No. 4
       (78, 38, 'มี', NULL, NULL),
       (79, 38, 'ไม่มี', NULL, NULL),
       -- Question No. 5
       (80, 39, 'มี', NULL, NULL),
       (81, 39, 'ไม่มี', NULL, NULL),
       -- Question No. 6
       (82, 40, 'เดินได้เอง', NULL, NULL),
       (83, 40, 'เดินเองไม่ได้', NULL, NULL),
       -- Question No. 7
       (84, 41, 'มี', NULL, NULL),
       (85, 41, 'ไม่มี', NULL, NULL),
       -- ท้องเสีย แมว
       -- Question No. 1
       (86, 42, '1', NULL, NULL),
       (87, 42, '2', NULL, NULL),
       (88, 42, '3', NULL, NULL),
       (89, 42, '4', NULL, NULL),
       (90, 42, '5', NULL, NULL),
       (91, 42, '6', NULL, NULL),
       (92, 42, '7', NULL, NULL),
       -- Question No. 2
       (93, 43, '<=14 วัน', 'Acute diarrhea', NULL),
       (94, 43, '>14 วัน', 'Chronic diarrhea', NULL),
       -- Question No. 3
       (95, 44, 'ใช่', NULL, NULL),
       (96, 44, 'ไม่', NULL, NULL),
       -- Question No. 4
       (97, 45, 'ใช่', NULL, NULL),
       (98, 45, 'ไม่', NULL, NULL),
       -- Question No. 5
       (99, 46, 'ใช่', NULL, NULL),
       (100, 46, 'ไม่', NULL, NULL),
       -- Question No. 6
       (101, 47, 'ใช่', NULL, NULL),
       (102, 47, 'ไม่', NULL, NULL),
       -- Question No. 7
       (103, 48, 'ใช่', NULL, NULL),
       (104, 48, 'ไม่', NULL, NULL),
       -- Question No. 8
       (105, 49, 'ใช่', NULL, NULL),
       (106, 49, 'ไม่', NULL, NULL),
       -- Question No. 9
       (107, 50, 'ใช่', NULL, NULL),
       (108, 50, 'ไม่', NULL, NULL),
       -- Question No. 11
       (109, 52, 'ใช่', NULL, NULL),
       (110, 52, 'ไม่', NULL, NULL),
       -- Question No. 12
       (111, 53, 'ใช่', NULL, NULL),
       (112, 53, 'ไม่', NULL, NULL),
       -- ไอ แมว
       -- Question No. 1
       (113, 54, 'มี', NULL, NULL),
       (114, 54, 'ไม่มี', NULL, 60),
       -- Question No. 2
       (115, 56, 'ตลอดเวลา', NULL, NULL),
       (116, 56, 'มากกว่า 1 ชม./วัน', NULL, NULL),
       (117, 56, 'น้อยกว่า 1 ชม./วัน', NULL, NULL),
       -- Question No. 3
       (118, 57, 'ไอต่อเนื่อง', NULL, NULL),
       (119, 57, 'ไอแล้วหยุด', NULL, NULL),
       -- Question No. 4
       (120, 58, 'ใช่', NULL, NULL),
       (121, 58, 'ไม่ใช่', NULL, NULL),
       -- Question No. 5
       (122, 59, 'ครบ', NULL, NULL),
       (123, 59, 'ไม่ครบ', NULL, NULL),
       -- Question No. 6
       (124, 60, 'ทำ', NULL, NULL),
       (125, 60, 'ไม่ได้ทำ', NULL, NULL),
       -- Question No. 7
       (126, 61, 'มี', NULL, NULL),
       (127, 61, 'ไม่มี', NULL, NULL),
       -- Question No. 8
       (128, 62, 'มี', NULL, NULL),
       (129, 62, 'ไม่มี', NULL, NULL),
       -- เหงือกซีด แมว
       -- Question No. 1
       (130, 63, 'ครบ', NULL, NULL),
       (131, 63, 'ไม่ครบ', NULL, NULL),
       -- Question No. 2
       (132, 64, 'ทำ', NULL, NULL),
       (133, 64, 'ไม่ได้ทำ', NULL, NULL),
       -- Question No. 3
       (134, 65, 'มี', NULL, NULL),
       (135, 65, 'ไม่มี', NULL, NULL),
       -- Question No. 4
       (136, 66, 'มี', NULL, NULL),
       (137, 66, 'ไม่มี', NULL, NULL),
       -- Question No. 5
       (138, 67, 'มี', NULL, NULL),
       (139, 67, 'ไม่มี', NULL, NULL),
       -- Question No. 6
       (140, 68, 'มี', NULL, NULL),
       (141, 68, 'ไม่มี', NULL, NULL),
       -- ขนร่วง แมว
       -- Question No. 1
       (142, 69, 'ทำ', NULL, NULL),
       (143, 69, 'ไม่ได้ทำ', NULL, NULL),
       -- Question No. 2
       (144, 70, 'ใช่', NULL, NULL),
       (145, 70, 'ไม่ใช่', NULL, NULL),
       -- Question No. 3
       (146, 71, 'ใช่', NULL, NULL),
       (147, 71, 'ไม่ใช่', NULL, NULL),
       -- Question No. 4
       (148, 72, 'ใช่', NULL, NULL),
       (149, 72, 'ไม่ใช่', NULL, NULL),
       -- Question No. 5
       (150, 73, 'มี', NULL, NULL),
       (151, 73, 'ไม่มี', NULL, NULL),
       -- Question No. 6
       (152, 74, 'มี', NULL, NULL),
       (153, 74, 'ไม่มี', NULL, NULL),
       -- Question No. 7
       (154, 75, 'เช้า', NULL, NULL),
       (155, 75, 'กลางวัน', NULL, NULL),
       (156, 75, 'ดึก', NULL, NULL),
       (157, 75, 'ตลอดเวลา', NULL, NULL),
       (158, 75, 'ไม่มีอาการคัน', NULL, NULL),
       -- อึไม่ออก แมว
       -- Question No. 2
       (159, 77, 'ได้', NULL, NULL),
       (160, 77, 'ไม่ได้', NULL, NULL),
       -- Question No. 3
       (161, 78, 'มี', NULL, NULL),
       (162, 78, 'ไม่มี', NULL, NULL),
       -- Question No. 4
       (163, 79, 'มี', NULL, NULL),
       (164, 79, 'ไม่มี', NULL, NULL),
       -- Question No. 5
       (165, 80, 'มี', NULL, NULL),
       (166, 80, 'ไม่มี', NULL, NULL),
       -- Question No. 6
       (167, 81, 'เดินได้เอง', NULL, NULL),
       (168, 81, 'เดินเองไม่ได้', NULL, NULL),
       -- Question No. 7
       (169, 82, 'มี', NULL, NULL),
       (170, 82, 'ไม่มี', NULL, NULL);