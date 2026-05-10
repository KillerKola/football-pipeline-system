import os
import json
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# UPUTE ZA POKRETANJE: pokrenuti skriptu iz root direktorija repozitorija
# naredbom 'python src/ingestion/fetch_raw_data.py'
# bitno je sacekati da se skripta izvrsi do kraja kako bi sve ekipe bile dohvacene
# svako novo pokretanje "gazi" stare podatke i stvara nove

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = os.getenv("API_BASE_URL")
LEAGUE_ID = 39
SEASON = 2024

HEADERS = {
    "x-apisports-key": API_KEY
}

RAW_DIR = Path("data/raw")
LEAGUES_DIR = RAW_DIR / "leagues"
TEAMS_DIR = RAW_DIR / "teams"
FIXTURES_DIR = RAW_DIR / "fixtures"
STANDINGS_DIR = RAW_DIR / "standings"
PLAYERS_DIR = RAW_DIR / "players"

for d in [LEAGUES_DIR, TEAMS_DIR, FIXTURES_DIR, STANDINGS_DIR, PLAYERS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def fetch_endpoint(endpoint: str, params: dict):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_json(data: dict, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_leagues():
    data = fetch_endpoint("leagues", {"id": LEAGUE_ID, "season": SEASON})
    save_json(data, LEAGUES_DIR / f"league_{LEAGUE_ID}_{SEASON}.json")
    return data


def fetch_teams():
    data = fetch_endpoint("teams", {"league": LEAGUE_ID, "season": SEASON})
    save_json(data, TEAMS_DIR / f"teams_{LEAGUE_ID}_{SEASON}.json")
    return data


def fetch_fixtures():
    data = fetch_endpoint("fixtures", {"league": LEAGUE_ID, "season": SEASON})
    save_json(data, FIXTURES_DIR / f"fixtures_{LEAGUE_ID}_{SEASON}.json")
    return data


def fetch_standings():
    data = fetch_endpoint("standings", {"league": LEAGUE_ID, "season": SEASON})
    save_json(data, STANDINGS_DIR / f"standings_{LEAGUE_ID}_{SEASON}.json")
    return data


def fetch_players_for_teams(teams_data):
    team_items = teams_data.get("response", [])

    for team_obj in team_items:
        team = team_obj.get("team", {})
        team_id = team.get("id")
        team_name = team.get("name", "unknown").replace(" ", "_").lower()

        if not team_id:
            continue

        all_players = []
        page = 1

        while True:
            data = fetch_endpoint(
                "players",
                {
                    "team": team_id,
                    "season": SEASON,
                    "page": page
                }
            )

            all_players.extend(data.get("response", []))

            paging = data.get("paging", {})
            current_page = paging.get("current", page)
            total_pages = paging.get("total", 1)

            if current_page >= total_pages:
                break

            page += 1
            if page > 3: #jer free plan konkretnog API-ja dopusta samo max page = 3
                break
            time.sleep(7)

        final_data = {
            "get": "players",
            "parameters": {
                "team": str(team_id),
                "season": str(SEASON)
            },
            "errors": data.get("errors", []),
            "results": len(all_players),
            "paging": {
                "current": 1,
                "total": 1
            },
            "response": all_players
        }

        save_json(
            final_data,
            PLAYERS_DIR / f"players_team_{team_id}_{SEASON}_{team_name}.json"
        )

        time.sleep(7)


def main():
    if not API_KEY:
        raise ValueError("Missing API_FOOTBALL_KEY in .env")

    fetch_leagues()
    teams_data = fetch_teams()
    fetch_fixtures()
    fetch_standings()
    fetch_players_for_teams(teams_data)


if __name__ == "__main__":
    main()