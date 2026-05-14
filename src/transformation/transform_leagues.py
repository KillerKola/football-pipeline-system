import json
from pathlib import Path

RAW_DIR = Path("data/raw/leagues")
OUTPUT_DIR = Path("data/transformed/leagues")
OUTPUT_FILE = OUTPUT_DIR / "transformed_leagues.json"


def transform_league_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed_rows = []

    for item in data.get("response", []):
        league = item.get("league", {})
        country = item.get("country", {})
        seasons = item.get("seasons", [])

        for season in seasons:
            transformed_rows.append({
                "league_id": league.get("id"),
                "league_name": league.get("name"),
                "country_name": country.get("name"),
                "season": season.get("year")
            })

    return transformed_rows


def transform_all_leagues():
    all_rows = []

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Folder ne postoji: {RAW_DIR}")

    for json_file in RAW_DIR.glob("*.json"):
        try:
            rows = transform_league_file(json_file)
            all_rows.extend(rows)
        except Exception as e:
            print(f"Greška u datoteci {json_file.name}: {e}")

    unique = {}
    for row in all_rows:
        key = (row["league_id"], row["season"])
        unique[key] = row

    final_rows = sorted(unique.values(), key=lambda x: (x["league_id"], x["season"]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transform_all_leagues()