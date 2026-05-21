import os
import json
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# UPUTE ZA POKRETANJE: pokrenuti skriptu main.py iz root direktorija repozitorija
# bitno je sacekati da se skripta izvrsi do kraja kako bi sve ekipe bile dohvacene i spremljene
# svako novo pokretanje "gazi" stare podatke

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = os.getenv("API_BASE_URL")

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

def get_league_seasons():
    raw_value = os.getenv("LEAGUE_SEASONS", "")
    pairs = []

    for item in raw_value.split(","):
        item = item.strip()
        if not item:
            continue

        league_id, season = item.split(":")
        pairs.append((int(league_id), int(season)))

    return pairs

def fetch_endpoint(endpoint: str, params: dict):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_json(data: dict, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_leagues(league_id, season):
    data = fetch_endpoint("leagues", {"id": league_id, "season": season})
    save_json(data, LEAGUES_DIR / f"league_{league_id}_{season}.json")
    return data


def fetch_teams(league_id, season):
    data = fetch_endpoint("teams", {"league": league_id, "season": season})
    save_json(data, TEAMS_DIR / f"teams_{league_id}_{season}.json")
    return data


def fetch_fixtures(league_id, season):
    data = fetch_endpoint("fixtures", {"league": league_id, "season": season})
    save_json(data, FIXTURES_DIR / f"fixtures_{league_id}_{season}.json")
    return data


def fetch_standings(league_id, season):
    data = fetch_endpoint("standings", {"league": league_id, "season": season})
    save_json(data, STANDINGS_DIR / f"standings_{league_id}_{season}.json")
    return data


def fetch_players_for_teams(teams_data, season, fetched_team_seasons):
    team_items = teams_data.get("response", [])

    for team_obj in team_items:
        team = team_obj.get("team", {})
        team_id = team.get("id")
        team_name = team.get("name", "unknown").replace(" ", "_").lower()

        if not team_id or (team_id, season) in fetched_team_seasons:
            continue

        fetched_team_seasons.add((team_id, season))

        all_players = []
        page = 1

        while True:
            data = fetch_endpoint(
                "players",
                {
                    "team": team_id,
                    "season": season,
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
                "season": str(season)
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
            PLAYERS_DIR / f"players_team_{team_id}_{season}_{team_name}.json"
        )

        time.sleep(7)


def main():
    if not API_KEY:
        raise ValueError("Missing API_FOOTBALL_KEY in .env")

    league_seasons = get_league_seasons()
    if not league_seasons:
        raise ValueError("Missing LEAGUE_SEASONS in .env")

    fetched_team_seasons = set()

    print("Approximately 8 minutes per league:season if on free plan.")
    for league_id, season in league_seasons:
        print(f"Fetching league {league_id}, season {season}...")

        fetch_leagues(league_id, season)
        teams_data = fetch_teams(league_id, season)
        fetch_fixtures(league_id, season)
        fetch_standings(league_id, season)
        fetch_players_for_teams(teams_data, season, fetched_team_seasons)


if __name__ == "__main__":
    main()