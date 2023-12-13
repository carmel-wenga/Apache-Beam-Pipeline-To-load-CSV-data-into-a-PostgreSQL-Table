-- @author : Carmel WENGA

DROP TABLE IF EXISTS tests;

CREATE TABLE salaries(
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    education_level VARCHAR(50) NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    year_of_experience FLOAT NOT NULL,
    salary FLOAT NOT NULL
);