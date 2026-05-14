import json
from pathlib import Path

RAW_DIR = Path("data/raw/standings")
OUTPUT_DIR = Path("data/transformed/standings")
OUTPUT_FILE = OUTPUT_DIR / "transformed_standings.json"


def transform_standings_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed_rows = []

    for item in data.get("response", []):
        league = item.get("league", {})

        for standings_group in league.get("standings", []):
            for row in standings_group:
                team = row.get("team", {})
                all_stats = row.get("all", {})
                all_goals = all_stats.get("goals", {})

                transformed_rows.append({
                    "league_id": league.get("id"),
                    "season": league.get("season"),
                    "team_id": team.get("id"),
                    "team_rank": row.get("rank"),
                    "points": row.get("points"),
                    "form": row.get("form"),
                    "status": row.get("status"),
                    "description": row.get("description"),
                    "played": all_stats.get("played"),
                    "win": all_stats.get("win"),
                    "draw": all_stats.get("draw"),
                    "lose": all_stats.get("lose"),
                    "goals_for": all_goals.get("for"),
                    "goals_against": all_goals.get("against")
                })

    return transformed_rows


def transform_all_standings():
    all_rows = []

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Folder ne postoji: {RAW_DIR}")

    for json_file in RAW_DIR.glob("*.json"):
        try:
            rows = transform_standings_file(json_file)
            all_rows.extend(rows)
        except Exception as e:
            print(f"Greška u datoteci {json_file.name}: {e}")

    unique = {}
    for row in all_rows:
        key = (row["league_id"], row["season"], row["team_id"])
        unique[key] = row

    final_rows = sorted(unique.values(), key=lambda x: (x["league_id"], x["season"], x["team_rank"]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transform_all_standings()