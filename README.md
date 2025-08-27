# Mini ETL Pipeline using Airflow, Pandas & Snowflake

## Project Overview:
- This project demonstrates a Mini Data Engineering Pipeline where data is extracted from an API, transformed using Pandas, orchestrated with Apache Airflow, and loaded into Snowflake.
- The goal was to practice building an industry-style ETL pipeline with scheduling, reproducibility, and cloud data warehouse integration.

## Key Highlights:
- Extract → Pulled random user data from RandomUser API.
- Transform → Cleaned & reshaped the data with Pandas (renamed columns, dropped unnecessary fields, converted datatypes).
- Load → Inserted the transformed dataset into Snowflake using SnowflakeHook.
- Orchestration → Built a DAG in Apache Airflow with PythonOperator for task scheduling and reproducibility.
- Version Control → Tracked changes with Git & GitHub.

## Tech Stack:
- Python (Pandas, Requests) – Data extraction & transformation
- Apache Airflow – Workflow orchestration
- Snowflake – Cloud data warehouse
- Git & GitHub – Version control

## 📂 Project Structure
- `README.md` → documentation
- `project_1_Mini ETL.py` → airflow DAG (ETL pipeline code)
- `api_data.csv` → extracted raw API data
- `transformed_api_data.csv` → transformed & cleaned data
- `project_1_DAG_run.png` → screenshot of Airflow DAG execution
  
## Workflow Architecture:
ETL Flow:
Extract (API) → Transform (Pandas) → Load (Snowflake)
