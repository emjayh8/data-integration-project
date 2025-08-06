# Data Integration ETL Project

This project performs an ETL (Extract, Transform, Load) process on student data from a CSV file and loads it into a SQL Server database.

## Features

- Loads student data from `students.csv`
- Cleans and validates data (checks for valid IDs, dates, and grade levels)
- Removes duplicate student IDs
- Creates a SQL Server database and table if they do not exist
- Inserts cleaned data into the database

## Requirements

- Python 3.x
- pandas
- pyodbc
- SQL Server (running locally on port 1433)
- ODBC Driver 17 for SQL Server

## Setup

1. **Install dependencies:**
   ```sh
   pip install pandas pyodbc
   ```

2. **Ensure SQL Server is running locally** and accessible with the following credentials:
   - Server: `localhost,1433`
   - User: `sa`
   - Password: `MyPassword123!`

3. **Place your `students.csv` file** in the project directory.

## Usage

Run the ETL script:

```sh
python etl.py
```

This will create a database called `student_db` and a table called `students`, then load the cleaned data.

## Querying the Data

You can use the provided `test.sql` script to query the loaded data:

```sql
USE student_db;
GO

SELECT * FROM students;
```

To run this script, use a SQL client (such as Azure Data Studio, SQL Server Management Studio, or the `sqlcmd` utility):

```sh
sqlcmd -S localhost,1433 -U sa -P MyPassword123! -i test.sql
```

## Notes

- Update the connection strings in `etl.py` if your SQL Server uses different credentials.
- The script is idempotent: it will not insert duplicate student records.
