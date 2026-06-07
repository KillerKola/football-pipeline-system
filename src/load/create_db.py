import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5544")
DB_NAME = os.getenv("DB_NAME", "football_pipeline")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

SQL_DIR = Path("sql")
SCHEMA_FILE = SQL_DIR / "schema.sql"
VIEWS_FILE = SQL_DIR / "views.sql"


def create_database_if_not_exists():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(f'CREATE DATABASE "{DB_NAME}"')
    else:
        print("Baza već postoji.")

    cur.close()
    conn.close()


def execute_sql_file(file_path):
    if not file_path.exists():
        return

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cur.execute(sql_script)
    conn.commit()

    cur.close()
    conn.close()


def main():
    create_database_if_not_exists()
    execute_sql_file(SCHEMA_FILE)
    execute_sql_file(VIEWS_FILE)


if __name__ == "__main__":
    main()