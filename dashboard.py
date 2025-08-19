import pyodbc
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 1. Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=student_db;"
    "UID=sa;"
    "PWD=MyPassword123!;"
)

# --------------------------
# 2. Query: Students per service
# --------------------------
query_service = """
SELECT sv.service_name, COUNT(*) AS num_students
FROM students AS s
JOIN services AS sv
    ON s.service_code = sv.service_code
GROUP BY sv.service_name
ORDER BY num_students DESC
"""
df_service = pd.read_sql(query_service, conn)

# --------------------------
# 3. Query: Students per grade + service
# --------------------------
query_grade_service = """
SELECT s.grade_level, sv.service_name, COUNT(*) AS num_students
FROM students AS s
JOIN services AS sv
    ON s.service_code = sv.service_code
GROUP BY s.grade_level, sv.service_name
ORDER BY s.grade_level, num_students DESC
"""
df_grade_service = pd.read_sql(query_grade_service, conn)

# --------------------------
# 4. Create charts
# --------------------------

# Chart 1: Students per service (bar chart)
fig1 = px.bar(
    df_service,
    x="service_name",
    y="num_students",
    title="Total Students per Service",
    text_auto=True
)

# Chart 2: Students per grade + service (grouped bar)
fig2 = px.bar(
    df_grade_service,
    x="service_name",
    y="num_students",
    color="grade_level",
    barmode="group",
    title="Students per Service by Grade Level"
)

# --------------------------
# 5. Combine into single dashboard
# --------------------------
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Total Students per Service", "Students per Service by Grade Level")
)

# Add first chart
for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)

# Add second chart
for trace in fig2.data:
    fig.add_trace(trace, row=2, col=1)

fig.update_layout(
    height=900,
    showlegend=True,
    title_text="📊 Student Services Dashboard"
)

# --------------------------
# 6. Export as interactive HTML
# --------------------------
fig.write_html("dashboard.html", include_plotlyjs="cdn")
print("✅ Dashboard saved as dashboard.html")
