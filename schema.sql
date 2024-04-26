DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS students_result;


CREATE TABLE students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL
);

CREATE TABLE quizzes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
subject TEXT NOT NULL,
number_of_questions INTEGER NOT NULL,
date_given VARCHAR NOT NULL);

CREATE TABLE students_result (
student_id INTEGER NOT NULL,
quiz_id INTEGER NOT NULL,
score INTEGER CHECK (score >= 0 AND score < 100) NOT NULL
);

INSERT INTO students VALUES(1, 'John', 'Smith');
INSERT INTO quizzes VALUES(1, 'Python Basics', 5, 'February 5th, 2015');
INSERT INTO students_result VALUES(1, 1, 85)