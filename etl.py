import pyodbc
import csv

# === SQL Server connection ===
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"  # replace with your Docker SQL Server name if needed
    "DATABASE=student_db;"
    "UID=sa;"
    "PWD=MyPassword123!;"  # replace with your SA password
)
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

# === Create 'services' table if it doesn't exist ===
cursor.execute("""
IF OBJECT_ID('services', 'U') IS NULL
CREATE TABLE services (
    service_code VARCHAR(10) PRIMARY KEY,
    service_name VARCHAR(100)
)
""")
print("Table 'services' is ready.")

# === Load services.csv ===
print("Loading services data...")
with open('services.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM services WHERE service_code = ?)
        INSERT INTO services (service_code, service_name)
        VALUES (?, ?)
        """, row['service_code'], row['service_code'], row['service_name'])
print("✅ Services data loaded.")

# === Create 'students' table if it doesn't exist ===
cursor.execute("""
IF OBJECT_ID('students', 'U') IS NULL
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    dob DATE,
    grade_level INT NULL,
    service_code VARCHAR(10) NULL,
    FOREIGN KEY (service_code) REFERENCES services(service_code)
)
""")
print("Table 'students' is ready.")

# === Load students.csv ===
print("Loading students data...")
with open('students.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = ?)
        INSERT INTO students (student_id, first_name, last_name, dob, grade_level, service_code)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        row['student_id'],
        row['student_id'],
        row['first_name'],
        row['last_name'],
        row['dob'],
        row['grade_level'],
        row['service_code'] if row['service_code'] else None)
print("✅ Students data loaded.")

# === Close connection ===
cursor.close()
conn.close()
print("ETL finished successfully.")
