# football-pipeline-system
A system for collecting, processing, storing, and visualizing football statistics from public APIs. The project focuses on an end-to-end data pipeline that regularly fetches match, team, and player data, transforms it into an analytics-ready format, stores it in a relational database, and presents key insights through dashboards and visualizations.


# Football Statistics Data Pipeline

A system for automated collection, processing, storage, and visualization of football statistics from public data sources.

## Project Description

This project is being developed as part of a final thesis at the Faculty of Electrical Engineering and Computing, University of Zagreb. The goal of the project is to build a system that collects data about football matches, teams, and players from publicly available sources, processes it, and stores it in a structured format suitable for analysis and visualization.

The system is designed as an end-to-end data pipeline that enables:
- data extraction from external sources,
- data transformation and cleaning,
- storage in a relational database,
- creation of an analytical data model,
- presentation of results through dashboards and visualizations.

The project is focused on developing practical data engineering skills, including working with APIs, ETL processes, databases, backend services, and BI tools.

## Features

Planned system features include:
- collection of data about matches, teams, and players,
- periodic data refresh,
- storage of raw and processed data,
- transformation of data into an analytical model,
- league table overview,
- match result analysis,
- team comparison throughout a season,
- overview of selected player statistics,
- presentation of data through dashboards and charts.

## Technologies

The following technologies are planned for use in the project:

- **Python** – data extraction, processing, and transformation
- **PostgreSQL** – data storage
- **SQLAlchemy** – database interaction
- **Prefect** or **Airflow** – pipeline orchestration
- **FastAPI** – application/API layer
- **Metabase** – visualization and dashboards
- **Docker** – local deployment and service isolation
- **Git / GitHub** – version control and development documentation

## System Architecture

Planned system architecture:

1. Data source (public football API)
2. Ingestion layer for data collection
3. Transformation layer for data cleaning and preparation
4. Relational database for storage
5. API layer for data access
6. BI / dashboard layer for visualization

## Final Thesis

Final thesis title:

**Development of an Application for Collecting, Processing, and Visualizing Football Statistics from Public Data Sources**

This project is being developed as a final thesis at FER, with a focus on practical application of data engineering and data analytics principles.

## Author

Ivano Markić  
Faculty of Electrical Engineering and Computing  
University of Zagreb
