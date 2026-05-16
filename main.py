import subprocess
import sys

scripts = [
    "src/ingestion/fetch_raw_data.py",
    "src/transformation/transform_leagues.py",
    "src/transformation/transform_teams.py",
    "src/transformation/transform_fixtures.py",
    "src/transformation/transform_standings.py",
    "src/transformation/transform_players.py",
    "src/load/create_db.py",
    "src/load/load_data.py"
]

for script in scripts:
    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        print(f"Greška pri izvođenju skripte: {script}")
        sys.exit(result.returncode)