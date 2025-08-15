# Data Integration Project

This project sets up a SQL Server database for managing student and service data, supporting ETL workflows and many-to-many relationships between students and services.

## Features

- SQL scripts to drop and recreate tables for a clean setup
- Three main tables for flexible data modeling
- Foreign key constraints for data integrity
- Example queries and a summary view for reporting

## Requirements

- SQL Server (tested with ODBC Driver 17)
- Python 3.x (for ETL scripts, if used)
- `pyodbc` and `pandas` (for ETL scripts)
- Access to the database `student_db`

## Table Structure

### `services`
Stores information about available services.

| Column        | Type         | Description                  |
|---------------|--------------|------------------------------|
| service_code  | VARCHAR(10)  | Primary key, unique code     |
| service_name  | VARCHAR(100) | Name of the service          |

### `students`
Stores student details and links each student to a service (optional).

| Column        | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| student_id    | INT          | Primary key, unique student ID       |
| first_name    | VARCHAR(50)  | Student's first name                 |
| last_name     | VARCHAR(50)  | Student's last name                  |
| dob           | DATE         | Date of birth                        |
| grade_level   | INT          | Grade level                          |
| service_code  | VARCHAR(10)  | Foreign key to `services` (nullable) |

### `student_services`
Supports many-to-many relationships between students and services, with optional start and end dates.

| Column             | Type         | Description                          |
|--------------------|--------------|--------------------------------------|
| student_service_id | INT          | Primary key, auto-increment          |
| student_id         | INT          | Foreign key to `students`            |
| service_code       | VARCHAR(10)  | Foreign key to `services`            |
| start_date         | DATE         | Service start date (optional)        |
| end_date           | DATE         | Service end date (optional)          |

## Setup

1. **Run the setup script:**
   - Open SQL Server Management Studio, Azure Data Studio, or use `sqlcmd`.
   - Execute `setup.sql` to drop existing tables and recreate them.

   ```sh
   sqlcmd -S localhost,1433 -U sa -P YourPassword -i setup.sql
   ```

2. **(Optional) Run the ETL script:**
   - Place your CSV files (`students.csv`, `services.csv`) in the project directory.
   - Run the ETL Python script to load data.

   ```sh
   python etl.py
   ```

## Querying and Reporting

The `test.sql` script provides several useful queries:

1. **Create or update the summary view**
   ```sql
   CREATE OR ALTER VIEW student_services_summary AS
   SELECT s.grade_level, sv.service_name, COUNT(*) AS num_students
   FROM students AS s
   JOIN services AS sv ON s.service_code = sv.service_code
   GROUP BY s.grade_level, sv.service_name;
   ```
   *Creates a view that summarizes the number of students per grade level for each service.*

2. **View all students and their services**
   ```sql
   SELECT s.student_id, s.first_name, s.last_name, sv.service_name
   FROM students AS s
   JOIN services AS sv ON s.service_code = sv.service_code
   ORDER BY s.student_id;
   ```
   *Lists every student along with the name of the service they are linked to.*

3. **Count services per student**
   ```sql
   SELECT s.student_id, s.first_name, s.last_name,
          CASE WHEN s.service_code IS NULL THEN 0 ELSE 1 END AS total_services
   FROM students AS s
   ORDER BY total_services DESC;
   ```
   *Shows how many services each student is linked to (0 or 1 in this model).*

4. **Count students per service (all grades)**
   ```sql
   SELECT sv.service_name, COUNT(*) AS num_students
   FROM students AS s
   JOIN services AS sv ON s.service_code = sv.service_code
   GROUP BY sv.service_name
   ORDER BY num_students DESC;
   ```
   *Counts the number of students assigned to each service, across all grade levels.*

5. **Use the view for grade-level summary**
   ```sql
   SELECT * FROM student_services_summary ORDER BY grade_level, service_name;
   ```
   *Retrieves the summary of students per grade level and service from the view.*
