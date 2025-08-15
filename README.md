# Data Integration Project

This project sets up a SQL Server database for managing student and service data, supporting ETL workflows and many-to-many relationships between students and services.

## Features

- SQL scripts to drop and recreate tables for a clean setup
- Three main tables:
  - `services`: Stores service codes and names
  - `students`: Stores student details and links to services
  - `student_services`: Supports many-to-many relationships between students and services
- Foreign key constraints for data integrity

## Requirements

- SQL Server (tested with ODBC Driver 17)
- Python 3.x (for ETL scripts, if used)
- `pyodbc` and `pandas` (for ETL scripts)
- Access to the database `student_db`

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

## Table Structure

- **services**
  - `service_code` (PK)
  - `service_name`
- **students**
  - `student_id` (PK)
  - `first_name`
  - `last_name`
  - `dob`
  - `grade_level`
  - `service_code` (FK to services)
- **student_services**
  - `student_service_id` (PK)
  - `student_id` (FK to students)
  - `service_code` (FK to services)
  - `start_date`
  - `end_date`

## Usage

- Use the provided SQL scripts to set up and query your database.
- Use the ETL script to load and process CSV data.
