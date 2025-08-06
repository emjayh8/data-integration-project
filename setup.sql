-- Create the Students table
CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    dob DATE,
    grade_level VARCHAR(10),
    service_code VARCHAR(10)
);

-- Create the Services table
CREATE TABLE Services (
    service_code VARCHAR(10) PRIMARY KEY,
    service_name VARCHAR(100)
);