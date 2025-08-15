-- ================================================
-- setup.sql
-- Drops and recreates tables for Data Integration Project
-- ================================================
USE student_db;
GO
-- Drop dependent tables first
IF OBJECT_ID('student_services', 'U') IS NOT NULL
    DROP TABLE student_services;
GO

-- Drop students and services tables if they exist
IF OBJECT_ID('students', 'U') IS NOT NULL
    DROP TABLE students;
GO

IF OBJECT_ID('services', 'U') IS NOT NULL
    DROP TABLE services;
GO

-- Create services table
CREATE TABLE services (
    service_code VARCHAR(10) PRIMARY KEY,
    service_name VARCHAR(100)
);
GO

-- Create students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    grade_level INT,
    service_code VARCHAR(10) NULL,
    FOREIGN KEY (service_code) REFERENCES services(service_code)
);
GO

-- Optional: Create a join table for many-to-many relationships
CREATE TABLE student_services (
    student_service_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    service_code VARCHAR(10) NOT NULL,
    start_date DATE NULL,
    end_date DATE NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (service_code) REFERENCES services(service_code)
);
GO
