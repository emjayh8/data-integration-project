import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ======================================
# 1. Connect to SQL Server
# ======================================
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=student_db;"
    "UID=sa;"
    "PWD=MyPassword123!;"
)
cursor = conn.cursor()

# ======================================
# 2. Query students + services
# ======================================
query = """
SELECT s.student_id,
       s.first_name,
       s.last_name,
       s.dob,
       s.grade_level,
       s.service_code,
       sv.service_name
FROM students s
LEFT JOIN services sv
    ON s.service_code = sv.service_code;
"""
df = pd.read_sql(query, conn)

# ======================================
# 3. Transformations
# ======================================

# Calculate age from dob
today = date.today()
df['dob'] = pd.to_datetime(df['dob'])
df['age'] = df['dob'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))

# Fill missing service names with "No Service"
df['service_name'] = df['service_name'].fillna("No Service")

# Group counts
students_per_grade = df.groupby("grade_level")["student_id"].count().reset_index(name="num_students")
students_per_service = df.groupby("service_name")["student_id"].count().reset_index(name="num_students")

# ======================================
# 4. Visualizations
# ======================================

# --- Bar chart: students per grade ---
plt.figure(figsize=(8,6))
plt.bar(students_per_grade["grade_level"], students_per_grade["num_students"])
plt.xlabel("Grade Level")
plt.ylabel("Number of Students")
plt.title("Number of Students per Grade")
plt.savefig("students_per_grade.png")
plt.close()

# --- Pie chart: students per service ---
plt.figure(figsize=(8,6))
plt.pie(students_per_service["num_students"], labels=students_per_service["service_name"], autopct="%1.1f%%")
plt.title("Distribution of Students per Service")
plt.savefig("students_per_service.png")
plt.close()

# --- Histogram: age distribution ---
plt.figure(figsize=(8,6))
plt.hist(df["age"], bins=8, edgecolor="black")
plt.xlabel("Age")
plt.ylabel("Number of Students")
plt.title("Student Age Distribution")
plt.savefig("student_age_distribution.png")
plt.close()

print("✅ Visualizations created: students_per_grade.png, students_per_service.png, student_age_distribution.png")
