import pandas as pd
import pyodbc
import numpy as np

# Connection string to connect to SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=MyPassword123!"
)

# Connect to master to create the database if it doesn't exist
print("Connecting to SQL Server (master)...")
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()
cursor.execute("IF DB_ID('student_db') IS NULL CREATE DATABASE student_db")
print("Database 'student_db' is ready.")
cursor.close()
conn.close()

# Reconnect to student_db
print("Connecting to 'student_db'...")
conn_str_db = conn_str.replace("DATABASE=master", "DATABASE=student_db")
conn = pyodbc.connect(conn_str_db)
cursor = conn.cursor()

# Drop existing table to avoid schema mismatch
cursor.execute("IF OBJECT_ID('students', 'U') IS NOT NULL DROP TABLE students")

# Create table with correct schema
cursor.execute("""
    CREATE TABLE students (
        student_id INT PRIMARY KEY,
        full_name NVARCHAR(100),
        dob DATE,
        grade_level INT NULL,
        service_code NVARCHAR(10) NULL
    )
""")
print("Table 'students' is ready.")

# Load data from CSV
print("Loading data from CSV...")
df = pd.read_csv("students.csv")

# Clean and format data
df.replace({np.nan: None, "": None}, inplace=True)  # Replace NaN and blank with None
df['grade_level'] = pd.to_numeric(df['grade_level'], errors='coerce').astype("Int64")  # Coerce invalid to NA
df['dob'] = pd.to_datetime(df['dob'], errors='coerce').dt.date  # Convert to date

# Insert data
print("Inserting data...")
insert_query = """
    INSERT INTO students (student_id, full_name, dob, grade_level, service_code)
    VALUES (?, ?, ?, ?, ?)
"""

for _, row in df.iterrows():
    try:
        cursor.execute(insert_query,
                       row['student_id'],
                       row['full_name'],
                       row['dob'],
                       row['grade_level'],
                       row['service_code'])
    except pyodbc.IntegrityError:
        print(f"⚠️ Skipping duplicate student_id: {row['student_id']}")

conn.commit()
print("✅ ETL process completed successfully!")

cursor.close()
conn.close()
