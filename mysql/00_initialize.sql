-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS vetchat;
USE vetchat;

-- Source other SQL files to create tables
SOURCE 01_animal.sql;
SOURCE 02_symptom.sql;
SOURCE 03_question_set.sql;
SOURCE 04_question.sql;
SOURCE 05_answer.sql;
SOURCE 06_ticket.sql;
SOURCE 07_response.sql;