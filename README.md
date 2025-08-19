Data Integration Portfolio Project

Overview
This project demonstrates a full data integration workflow, including data ingestion, transformation, validation, reporting, and visualization. The goal is to showcase skills in SQL Server, Python ETL, data analysis, and dashboard creation for a K-12 education dataset.

The dataset consists of student information and special education services, which are transformed and loaded into a SQL Server database (student_db) for analysis.

Folder Structure

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

Prerequisites
- Python 3.10+
- SQL Server running locally (Docker recommended)
- Python packages (listed in requirements.txt):
  pandas
  pyodbc
  matplotlib
  plotly
- VS Code or another SQL client for running .sql scripts

Setup Instructions

1. Clone the repository
   git clone https://github.com/yourusername/data-integration-project.git
   cd data-integration-project

2. Set up Python virtual environment
   python -m venv venv
   source venv/bin/activate       # macOS/Linux
   # or
   venv\Scripts\activate          # Windows
   pip install -r requirements.txt

3. Set up SQL Server
   - Run sql/setup.sql on your SQL Server instance to create student_db and tables.

4. Run ETL script
   python etl/etl.py
   - Loads students.csv and services.csv into the database
   - Handles duplicate records and data validation

5. Run analysis queries
   - Open sql/test.sql in your SQL client
   - Execute queries to verify joins, aggregations, and views

6. Generate dashboard
   python dashboards/dashboard.py
   - Creates dashboards/dashboard.html with visualizations of student services

Features

- ETL Workflow: Reads CSVs, cleans data, loads into SQL Server
- Data Integrity: Validates duplicates, enforces foreign key constraints
- SQL Analysis: Aggregation queries, joins, and views
- Visualization Dashboard: Automated charts for student-service distribution
- Portfolio-ready: Organized folder structure and reproducible environment

Notes
- Designed for K-12 Special Education and Student Services data
- Modular and reusable ETL and dashboard scripts
- Easily extended with additional datasets or visualizations

License
MIT License
