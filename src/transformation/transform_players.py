import json
from pathlib import Path


def transform_players_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    transformed_rows_player = []
    transformed_rows_stats = []

    for item in data.get("response", []):
        player = item.get("player", {})
        birth = player.get("birth", {})

        transformed_rows_player.append({
            "player_id": player.get("id"),
            "firstname": player.get("firstname"),
            "lastname": player.get("lastname"),
            "birth_date": birth.get("date"),
            "birth_place": birth.get("place"),
            "birth_country": birth.get("country"),
            "nationality": player.get("nationality"),
            "height_cm": player.get("height"),
            "weight_kg": player.get("weight"),
            "injured": player.get("injured"),
            "photo": player.get("photo"),
            })

        for stat in item.get("statistics", []):
            team = stat.get("team", {})
            league = stat.get("league", {})
            games = stat.get("games", {})
            substitutes = stat.get("substitutes", {})
            shots = stat.get("shots", {})
            goals = stat.get("goals", {})
            passes = stat.get("passes", {})
            tackles = stat.get("tackles", {})
            duels = stat.get("duels", {})
            dribbles = stat.get("dribbles", {})
            fouls = stat.get("fouls", {})
            cards = stat.get("cards", {})
            penalty = stat.get("penalty", {})

            r = games.get("rating")
            transformed_rows_stats.append({
                "player_id": player.get("id"),
                "team_id": team.get("id"),
                "league_id": league.get("id"),
                "season": league.get("season"),
                "position": games.get("position"),
                "rating": round(float(r), 2) if r is not None else None,
                "appearances": games.get("appearences"),
                "lineups": games.get("lineups"),
                "minutes": games.get("minutes"),

                "sub_in": substitutes.get("in"),
                "sub_out": substitutes.get("out"),
                "sub_bench": substitutes.get("bench"),
                "shots_total": shots.get("total"),
                "shots_on": shots.get("on"),
                "goals_total": goals.get("total"),
                "goals_conceded": goals.get("conceded"),
                "assists": goals.get("assists"),
                "saves": goals.get("saves"),

                "passes_total": passes.get("total"),
                "passes_key": passes.get("key"),
                "passes_accuracy": passes.get("accuracy"),
                "tackles_total": tackles.get("total"),
                "tackles_blocks": tackles.get("blocks"),
                "tackles_interceptions": tackles.get("interceptions"),
                "duels_total": duels.get("total"),
                "duels_won": duels.get("won"),
                "dribbles_attempts": dribbles.get("attempts"),
                "dribbles_success": dribbles.get("success"),
                "dribbles_past": dribbles.get("past"),
                "fouls_drawn": fouls.get("drawn"),
                "fouls_committed": fouls.get("committed"),
                "cards_yellow": cards.get("yellow"),
                "cards_yellowred": cards.get("yellowred"),
                "cards_red": cards.get("red"),
                "penalty_won": penalty.get("won"),
                "penalty_committed": penalty.get("commited"),
                "penalty_scored": penalty.get("scored"),
                "penalty_missed": penalty.get("missed"),
                "penalty_saved": penalty.get("saved")
            })

    return transformed_rows_player, transformed_rows_stats


def transform_all_players():
    all_players = []
    all_stats = []

    RAW_DIR = Path("data/raw/players")

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Folder ne postoji: {RAW_DIR}")

    for json_file in RAW_DIR.glob("*.json"):
        try:
            players, stats = transform_players_file(json_file)
            all_players.extend(players)
            all_stats.extend(stats)
        except Exception as e:
            print(f"Greška u datoteci {json_file.name}: {e}")

    unique_players = {}
    for row in all_players:
        key = (row["player_id"])
        unique_players[key] = row

    final_players = sorted(
        unique_players.values(),
        key=lambda x: (x["player_id"])
    )

    OUTPUT_DIR = Path("data/transformed/players")
    OUTPUT_FILE = OUTPUT_DIR / "transformed_players.json"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_players, f, ensure_ascii=False, indent=2)

    unique_stats = {}
    for row in all_stats:
        key = (row["player_id"], row["team_id"], row["league_id"], row["season"])
        unique_stats[key] = row

    final_stats = sorted(
        unique_stats.values(),
        key=lambda x: (x["team_id"], x["league_id"], x["season"], x["player_id"])
    )

    OUTPUT_DIR = Path("data/transformed/stats")
    OUTPUT_FILE = OUTPUT_DIR / "transformed_stats.json"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_stats, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transform_all_players()