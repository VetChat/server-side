-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS vetchat;
USE vetchat;

-- Source other SQL files to create tables
SOURCE docker-entrypoint-initdb.d/01_animal.sql;
SOURCE docker-entrypoint-initdb.d/02_symptom.sql;
SOURCE docker-entrypoint-initdb.d/03_question_set.sql;
SOURCE docker-entrypoint-initdb.d/04_question.sql;
SOURCE docker-entrypoint-initdb.d/05_answer.sql;
SOURCE docker-entrypoint-initdb.d/06_ticket.sql;
SOURCE docker-entrypoint-initdb.d/07_response.sql;