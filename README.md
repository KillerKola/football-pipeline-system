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
- **psycopg2** - database creation and data loading
- **Prefect** – pipeline orchestration
- **Metabase** – visualization and dashboards
- **Docker** – local deployment and service isolation
- **Git / GitHub** – version control and development documentation

## System Architecture

Planned system architecture:

1. Data source (public football API)
2. Ingestion layer for data collection
3. Transformation layer for data cleaning and preparation
4. Relational database for storage
5. BI / dashboard layer for visualization


Setup guide:
requirements: Docker & Python
1) clone the repository
2) Create the .env file by copying the .env.example
3) (Necessary only if you want to add more data) Make an API-football account and copy your API key into the .env file
4) Start PostgreSQL, Metabase and Prefect in docker (install and open docker first and run the following command in the project root)
   'docker compose -f docker/docker-compose.yml up -d'
6) Run the docker containers if they aren't already running and then run the pipeline:
   - 'pip install -r requirements.txt'
   - if you want to fetch your own data, fill out the .env file and run this in the project root
     'python main.py fetch createdb load'
   - you can also run this if you want to use only the data already in the files
     'python main.py createdb load'
8) Open metabase via docker or go to http://localhost:3002
9) Login with
   -email: improjektr@gmail.com
   -password: xQt6UMU)2#90)j
10) That's it! You should be good to go. If you want to access metabase with an admin account to change the existing dashboards, please contact the owner of the repository

    -note: prefect automatically refreshes the seasons listed in your .env file every day at 3 AM which requires your system to be running. You can also open the prefect container and run it manually or change the running time in the .yml file


## Final Thesis

Final thesis title:

**Development of an Application for Collecting, Processing, and Visualizing Football Statistics from Public Data Sources**

This project is being developed as a final thesis at FER, with a focus on practical application of data engineering and data analytics principles.

## Author

Ivano Markić  
Faculty of Electrical Engineering and Computing  
University of Zagreb
