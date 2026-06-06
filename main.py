import subprocess
import sys

SCRIPTS = {
    "fetch": [
        "src/ingestion/fetch_raw_data.py",

    ],
    "createdb": [
        "src/load/create_db.py",
    ],
    "load": [
        "src/transformation/transform_leagues.py",
        "src/transformation/transform_teams.py",
        "src/transformation/transform_fixtures.py",
        "src/transformation/transform_standings.py",
        "src/transformation/transform_players.py",
        "src/load/load_data.py",
    ]
}

def run_scripts(scripts):
    for script in scripts:
        result = subprocess.run([sys.executable, script])

        if result.returncode != 0:
            print(f"Greška pri izvođenju skripte: {script}")
            sys.exit(result.returncode)

def main():
    commands = sys.argv[1:]

    if not commands:
        print("Upotreba: python main.py fetch createdb load")
        sys.exit(1)

    for command in commands:
        if command not in SCRIPTS:
            print(f"Nepoznata komanda: {command}")
            print("Dozvoljene komande: fetch, createdb, load")
            sys.exit(1)

    for command in commands:
        run_scripts(SCRIPTS[command])

if __name__ == "__main__":
    main()