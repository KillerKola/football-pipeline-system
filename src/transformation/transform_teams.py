import json
from pathlib import Path

RAW_DIR = Path("data/raw/teams")
OUTPUT_DIR = Path("data/transformed/teams")
OUTPUT_FILE = OUTPUT_DIR / "transformed_teams.json"


def transform_teams_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed_rows = []

    for item in data.get("response", []):
        team = item.get("team", {})
        venue = item.get("venue", {})

        transformed_rows.append({
            "team_id": team.get("id"),
            "team_name": team.get("name"),
            "country": team.get("country"),
            "founded": team.get("founded"),
            "logo": team.get("logo"),
            "venue": venue.get("name"),
            "venue_city": venue.get("city")
        })

    return transformed_rows


def transform_all_teams():
    all_rows = []

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Folder ne postoji: {RAW_DIR}")

    for json_file in RAW_DIR.glob("*.json"):
        try:
            rows = transform_teams_file(json_file)
            all_rows.extend(rows)
        except Exception as e:
            print(f"Greška u datoteci {json_file.name}: {e}")

    unique = {}
    for row in all_rows:
        key = (row["team_id"])
        unique[key] = row

    final_rows = sorted(unique.values(), key=lambda x: (x["team_id"]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transform_all_teams()