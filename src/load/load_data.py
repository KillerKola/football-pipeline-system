import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv

import psycopg2

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

BASE_DIR = Path("data/transformed")

def load_json(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def league_exists(cur, league_id, season):
    cur.execute("""
        SELECT 1
        FROM football.leagues
        WHERE league_id = %s AND season = %s
    """, (league_id, season))
    return cur.fetchone() is not None

def to_int(value):
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        digits = re.findall(r"\d+", value)
        if digits:
            return int(digits[0])
    return None


def load_leagues(cur):
    leagues = load_json(BASE_DIR / "leagues" / "transformed_leagues.json")

    for row in leagues:
        cur.execute("""
            INSERT INTO football.leagues (
                league_id, season, league_name, country
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (league_id, season) DO UPDATE SET
                league_name = EXCLUDED.league_name,
                country = EXCLUDED.country
        """, (
            row.get("league_id"),
            row.get("season"),
            row.get("league_name"),
            row.get("country_name"),
        ))


def load_teams(cur):
    teams = load_json(BASE_DIR / "teams" / "transformed_teams.json")

    for row in teams:
        cur.execute("""
            INSERT INTO football.teams (
                team_id, team_name, country, founded, logo, venue_name, venue_city
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (team_id) DO UPDATE SET
                team_name = EXCLUDED.team_name,
                country = EXCLUDED.country,
                founded = EXCLUDED.founded,
                logo = EXCLUDED.logo,
                venue_name = EXCLUDED.venue_name,
                venue_city = EXCLUDED.venue_city
        """, (
            row.get("team_id"),
            row.get("team_name"),
            row.get("country"),
            to_int(row.get("founded")),
            row.get("logo"),
            row.get("venue_name"),
            row.get("venue_city"),
        ))

def load_players(cur):
    file_path = BASE_DIR / "players" / "transformed_players.json"
    players = load_json(file_path)

    for row in players:
        cur.execute("""
            INSERT INTO football.players (
                player_id, firstname, lastname, birth_date, birth_place,
                birth_country, nationality, height_cm, weight_kg, injured, photo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_id) DO UPDATE SET
                firstname = EXCLUDED.firstname,
                lastname = EXCLUDED.lastname,
                birth_date = EXCLUDED.birth_date,
                birth_place = EXCLUDED.birth_place,
                birth_country = EXCLUDED.birth_country,
                nationality = EXCLUDED.nationality,
                height_cm = EXCLUDED.height_cm,
                weight_kg = EXCLUDED.weight_kg,
                injured = EXCLUDED.injured,
                photo = EXCLUDED.photo
        """, (
            row.get("player_id"),
            row.get("firstname"),
            row.get("lastname"),
            row.get("birth_date"),
            row.get("birth_place"),
            row.get("birth_country"),
            row.get("nationality"),
            to_int(row.get("height_cm")),
            to_int(row.get("weight_kg")),
            row.get("injured", False),
            row.get("photo"),
        ))


def load_fixtures(cur):
    file_path = BASE_DIR / "fixtures" / "transformed_fixtures.json"
    fixtures = load_json(file_path)

    for row in fixtures:
        cur.execute("""
            INSERT INTO football.fixtures (
                fixture_id, league_id, season, round, fixture_date, status_short,
                venue_name, home_team_id, away_team_id, home_goals, away_goals, ht_home_goals, ht_away_goals
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (fixture_id) DO UPDATE SET
                league_id = EXCLUDED.league_id,
                season = EXCLUDED.season,
                round = EXCLUDED.round,
                fixture_date = EXCLUDED.fixture_date,
                status_short = EXCLUDED.status_short,
                venue_name = EXCLUDED.venue_name,
                home_team_id = EXCLUDED.home_team_id,
                away_team_id = EXCLUDED.away_team_id,
                home_goals = EXCLUDED.home_goals,
                away_goals = EXCLUDED.away_goals,
                ht_home_goals = EXCLUDED.ht_home_goals,
                ht_away_goals = EXCLUDED.ht_away_goals
        """, (
            row["fixture_id"],
            row["league_id"],
            row["season"],
            to_int(row.get("round")),
            row.get("fixture_date"),
            row.get("status_short"),
            row.get("venue"),
            row["home_team_id"],
            row["away_team_id"],
            to_int(row.get("home_goals")),
            to_int(row.get("away_goals")),
            to_int(row.get("ht_home_goals")),
            to_int(row.get("ht_away_goals")),
        ))


def load_standings(cur):
    file_path = BASE_DIR / "standings" / "transformed_standings.json"
    standings = load_json(file_path)

    for row in standings:
        cur.execute("""
            INSERT INTO football.standings (
                league_id, season, team_id, team_rank, points, form, status,
                description, played, win, draw, lose, goals_for, goals_against
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (league_id, season, team_id) DO UPDATE SET
                team_rank = EXCLUDED.team_rank,
                points = EXCLUDED.points,
                form = EXCLUDED.form,
                status = EXCLUDED.status,
                description = EXCLUDED.description,
                played = EXCLUDED.played,
                win = EXCLUDED.win,
                draw = EXCLUDED.draw,
                lose = EXCLUDED.lose,
                goals_for = EXCLUDED.goals_for,
                goals_against = EXCLUDED.goals_against,
                updated_at = NOW()
        """, (
            row["league_id"],
            row["season"],
            row["team_id"],
            to_int(row.get("team_rank")),
            to_int(row.get("points")),
            row.get("form"),
            row.get("status"),
            row.get("description"),
            to_int(row.get("played")),
            to_int(row.get("win")),
            to_int(row.get("draw")),
            to_int(row.get("lose")),
            to_int(row.get("goals_for")),
            to_int(row.get("goals_against")),
        ))


def load_player_statistics(cur):
    file_path = BASE_DIR / "stats" / "transformed_stats.json"
    stats = load_json(file_path)

    for row in stats:
        league_id = row.get("league_id")
        season = row.get("season")

        if not league_exists(cur, league_id, season):
            continue

        cur.execute("""
            INSERT INTO football.player_statistics (
                player_id, team_id, league_id, season, player_position, rating,
                appearances, lineups, minutes,
                substitute_in, substitute_out, substitute_bench,
                shots_total, shots_on,
                goals_total, goals_conceded, assists, saves,
                passes_total, passes_key, passes_accuracy,
                tackles_total, tackles_blocks, tackles_interceptions,
                duels_total, duels_won,
                dribbles_attempts, dribbles_success, dribbles_past,
                fouls_drawn, fouls_committed,
                cards_yellow, cards_yellowred, cards_red,
                penalty_won, penalty_committed, penalty_scored, penalty_missed, penalty_saved
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (player_id, team_id, league_id, season) DO UPDATE SET
                player_position = EXCLUDED.player_position,
                rating = EXCLUDED.rating,
                appearances = EXCLUDED.appearances,
                lineups = EXCLUDED.lineups,
                minutes = EXCLUDED.minutes,
                substitute_in = EXCLUDED.substitute_in,
                substitute_out = EXCLUDED.substitute_out,
                substitute_bench = EXCLUDED.substitute_bench,
                shots_total = EXCLUDED.shots_total,
                shots_on = EXCLUDED.shots_on,
                goals_total = EXCLUDED.goals_total,
                goals_conceded = EXCLUDED.goals_conceded,
                assists = EXCLUDED.assists,
                saves = EXCLUDED.saves,
                passes_total = EXCLUDED.passes_total,
                passes_key = EXCLUDED.passes_key,
                passes_accuracy = EXCLUDED.passes_accuracy,
                tackles_total = EXCLUDED.tackles_total,
                tackles_blocks = EXCLUDED.tackles_blocks,
                tackles_interceptions = EXCLUDED.tackles_interceptions,
                duels_total = EXCLUDED.duels_total,
                duels_won = EXCLUDED.duels_won,
                dribbles_attempts = EXCLUDED.dribbles_attempts,
                dribbles_success = EXCLUDED.dribbles_success,
                dribbles_past = EXCLUDED.dribbles_past,
                fouls_drawn = EXCLUDED.fouls_drawn,
                fouls_committed = EXCLUDED.fouls_committed,
                cards_yellow = EXCLUDED.cards_yellow,
                cards_yellowred = EXCLUDED.cards_yellowred,
                cards_red = EXCLUDED.cards_red,
                penalty_won = EXCLUDED.penalty_won,
                penalty_committed = EXCLUDED.penalty_committed,
                penalty_scored = EXCLUDED.penalty_scored,
                penalty_missed = EXCLUDED.penalty_missed,
                penalty_saved = EXCLUDED.penalty_saved
        """, (
            row["player_id"],
            row["team_id"],
            league_id,
            season,
            row.get("position"),
            row.get("rating"),
            to_int(row.get("appearances")),
            to_int(row.get("lineups")),
            to_int(row.get("minutes")),
            to_int(row.get("sub_in")),
            to_int(row.get("sub_out")),
            to_int(row.get("sub_bench")),
            to_int(row.get("shots_total")),
            to_int(row.get("shots_on")),
            to_int(row.get("goals_total")),
            to_int(row.get("goals_conceded")),
            to_int(row.get("assists")),
            to_int(row.get("saves")),
            to_int(row.get("passes_total")),
            to_int(row.get("passes_key")),
            to_int(row.get("passes_accuracy")),
            to_int(row.get("tackles_total")),
            to_int(row.get("tackles_blocks")),
            to_int(row.get("tackles_interceptions")),
            to_int(row.get("duels_total")),
            to_int(row.get("duels_won")),
            to_int(row.get("dribbles_attempts")),
            to_int(row.get("dribbles_success")),
            to_int(row.get("dribbles_past")),
            to_int(row.get("fouls_drawn")),
            to_int(row.get("fouls_committed")),
            to_int(row.get("cards_yellow")),
            to_int(row.get("cards_yellowred")),
            to_int(row.get("cards_red")),
            to_int(row.get("penalty_won")),
            to_int(row.get("penalty_committed")),
            to_int(row.get("penalty_scored")),
            to_int(row.get("penalty_missed")),
            to_int(row.get("penalty_saved")),
        ))


def main():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        load_leagues(cur)
        load_teams(cur)
        load_players(cur)
        load_fixtures(cur)
        load_standings(cur)
        load_player_statistics(cur)

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Greška tijekom učitavanja podataka: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()