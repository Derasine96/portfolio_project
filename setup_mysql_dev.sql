-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS PersonalDiary;

-- Use the PersonalDiary schema
USE PersonalDiary;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(45) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100),
    date_of_birth DATE NOT NULL
);

-- Create quotes table
CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote TEXT NOT NULL,
    author VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS diaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(60) NOT NULL,
    entry VARCHAR(2000) NOT NULL,
    createdAt DATE NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS diary_tags (
    diary_id INT,
    tag_id INT,
    PRIMARY KEY (diary_id, tag_id),
    FOREIGN KEY (diary_id) REFERENCES diaries(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Insert initial data into users table
INSERT INTO users (username, email, password, firstName, lastName, date_of_birth) 
VALUES 
    ('john_doe', 'john@example.com', 'hashed_password_here', 'John', 'Doe', '1990-01-01'),
    ('jane_smith', 'jane@example.com', 'hashed_password_here', 'Jane', 'Smith', '1995-05-15');

-- Insert initial data into quotes table
INSERT INTO quotes (quote, author)
VALUES 
    ('To be or not to be, that is the question.', 'William Shakespeare'),
    ('I think, therefore I am.', 'René Descartes');