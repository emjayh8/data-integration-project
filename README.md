# Data Integration Portfolio Project

## Overview

This project demonstrates a complete data integration workflow for a K-12 education dataset, including data ingestion, transformation, validation, reporting, and visualization. It showcases skills in SQL Server, Python ETL, data analysis, and dashboard creation.

Student and service data are loaded from CSV files, transformed, and stored in a SQL Server database (`student_db`). The project includes scripts for database setup, ETL, analysis queries, and dashboard generation.

---

## Folder Structure

```
data-integration-project/
│
├── etl/
│   ├── etl.py              # Extract, transform, load script
│   ├── students.csv        # Source student data
│   └── services.csv        # Source services data
│
├── sql/
│   ├── setup.sql           # Database and table creation
│   └── test.sql            # Queries, joins, views for analysis
│
├── dashboards/
│   ├── dashboard.py        # Python visualization script
│   └── dashboard.html      # Generated HTML dashboard
│
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.10+
- SQL Server running locally (Docker recommended)
- Python packages (listed in `requirements.txt`):
  - pandas
  - pyodbc
  - matplotlib
  - plotly
- VS Code or another SQL client for running `.sql` scripts

---

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/data-integration-project.git
   cd data-integration-project
   ```

2. **Set up Python virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate       # macOS/Linux
   # or
   venv\Scripts\activate          # Windows
   pip install -r requirements.txt
   ```

3. **Set up SQL Server**
   - Run `sql/setup.sql` on your SQL Server instance to create `student_db` and all required tables.

4. **Run ETL script**
   ```sh
   python etl/etl.py
   ```
   - Loads `students.csv` and `services.csv` into the database
   - Handles duplicate records and data validation

5. **Run analysis queries**
   - Open `sql/test.sql` in your SQL client
   - Execute queries to verify joins, aggregations, and views

6. **Generate dashboard**
   ```sh
   python dashboards/dashboard.py
   ```
   - Creates `dashboards/dashboard.html` with visualizations of student services

---

## Database Tables Explained

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

---

## SQL Analysis Queries Explained (`test.sql`)

1. **Create or update the summary view**
   ```sql
   CREATE OR ALTER VIEW student_services_summary AS
   SELECT s.grade_level, sv.service_name, COUNT(*) AS num_students
   FROM students AS s
   JOIN services AS sv ON s.service_code = sv.service_code
   GROUP BY s.grade_level, sv.service_name;
   ```
   *Creates a view summarizing the number of students per grade level for each service.*

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

---

## Features

- **ETL Workflow:** Reads CSVs, cleans data, loads into SQL Server
- **Data Integrity:** Validates duplicates, enforces foreign key constraints
- **SQL Analysis:** Aggregation queries, joins, and views
- **Visualization Dashboard:** Automated charts for student-service distribution
- **Portfolio-ready:** Organized folder structure and reproducible environment

---

## Notes

- Designed for K-12 Special Education and Student Services data
- Modular and reusable ETL and dashboard scripts
- Easily extended with additional datasets or visualizations

---

## License

MIT License
