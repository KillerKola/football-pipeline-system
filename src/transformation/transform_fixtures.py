import json
from pathlib import Path

RAW_DIR = Path("data/raw/fixtures")
OUTPUT_DIR = Path("data/transformed/fixtures")
OUTPUT_FILE = OUTPUT_DIR / "transformed_fixtures.json"


def transform_fixtures_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed_rows = []

    for item in data.get("response", []):
        fixture = item.get("fixture", {})
        league = item.get("league", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})

        transformed_rows.append({
            "fixture_id": fixture.get("id"),
            "league_id": league.get("id"),
            "season": league.get("season"),
            "round": int(league.get("round").split("-")[-1].strip()),
            "fixture_date": fixture.get("date"),
            "status_short": fixture.get("status").get("short"),
            "venue": fixture.get("venue").get("name"),
            "home_team_id": teams.get("home").get("id"),
            "away_team_id": teams.get("away").get("id"),
            "home_goals": goals.get("home"),
            "away_goals": goals.get("away")
        })

    return transformed_rows


def transform_all_fixtures():
    all_rows = []

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Folder ne postoji: {RAW_DIR}")

    for json_file in RAW_DIR.glob("*.json"):
        try:
            rows = transform_fixtures_file(json_file)
            all_rows.extend(rows)
        except Exception as e:
            print(f"Greška u datoteci {json_file.name}: {e}")

    unique = {}
    for row in all_rows:
        key = (row["fixture_id"])
        unique[key] = row

    final_rows = sorted(unique.values(), key=lambda x: (x["season"], x["round"], x["fixture_date"], x["fixture_id"]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transform_all_fixtures()