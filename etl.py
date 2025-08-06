import pyodbc
import pandas as pd
from datetime import datetime

# STEP 1: Load CSV
df = pd.read_csv("students.csv")

# STEP 2: Clean and validate data
def split_name(full_name):
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return parts[0], " ".join(parts[1:])
    else:
        return parts[0], ""

def is_valid(row):
    try:
        int(row["student_id"])
        datetime.strptime(row["dob"], "%Y-%m-%d")
        int(row["grade_level"])
        return True
    except:
        return False

df = df[df.apply(is_valid, axis=1)].copy()
df["first_name"], df["last_name"] = zip(*df["full_name"].map(split_name))

# Drop duplicate student_id rows
df = df.drop_duplicates(subset="student_id")

# STEP 3: Connect to master DB with autocommit to create database if needed
conn_str_master = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=MyPassword123!"
)

conn_master = pyodbc.connect(conn_str_master, autocommit=True)  # autocommit=True avoids transaction error
cursor_master = conn_master.cursor()

cursor_master.execute("IF DB_ID('student_db') IS NULL CREATE DATABASE student_db")

conn_master.close()

# STEP 4: Connect to the new student_db database normally
conn_str_student_db = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=student_db;"
    "UID=sa;"
    "PWD=MyPassword123!"
)

conn = pyodbc.connect(conn_str_student_db)
cursor = conn.cursor()

# STEP 5: Create students table if not exists
cursor.execute("""
IF OBJECT_ID('students', 'U') IS NULL
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    dob DATE,
    grade_level INT,
    service_code NVARCHAR(10) NULL
)
""")
conn.commit()

# STEP 6: Insert valid, deduped data into students table
for _, row in df.iterrows():
    cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = ?)
        INSERT INTO students (student_id, first_name, last_name, dob, grade_level, service_code)
        VALUES (?, ?, ?, ?, ?, ?)
    """, row["student_id"], row["student_id"], row["first_name"], row["last_name"],
         row["dob"], row["grade_level"], row["service_code"] if pd.notna(row["service_code"]) else None)

conn.commit()
conn.close()

print("ETL from students.csv complete!")