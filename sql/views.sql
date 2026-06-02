CREATE OR REPLACE VIEW football.vw_league_table AS
SELECT
    l.league_name,
    l.country,
    s.season,
    t.team_name,
    s.team_rank,
    s.points,
    s.played,
    s.win,
    s.draw,
    s.lose,
    s.goals_for,
    s.goals_against,
    (s.goals_for - s.goals_against) AS goal_difference,
    ROUND(s.goals_for::numeric / NULLIF(s.played, 0), 2) AS goals_scored_per_match,
    ROUND(s.goals_against::numeric / NULLIF(s.played, 0), 2) AS goals_conceded_per_match,
    ROUND((s.win::numeric * 100) / NULLIF(s.played, 0), 2) AS win_percentage,
    s.form,
    s.status,
    s.description
FROM football.standings s JOIN football.teams t ON s.team_id = t.team_id
                          JOIN football.leagues l ON s.league_id = l.league_id AND s.season = l.season;


CREATE OR REPLACE VIEW football.vw_match_results AS
SELECT
    f.fixture_id,
    l.league_id,
    l.league_name,
    l.country,
    f.season,
    f.round,
    f.fixture_date,
    f.status_short,
    ht.team_id AS home_id,
    awt.team_id AS away_id,
    ht.team_name AS home_team,
    awt.team_name AS away_team,
    f.home_goals,
    f.away_goals,
    f.ht_home_goals,
    f.ht_away_goals,
    CASE WHEN f.home_goals > f.away_goals THEN ht.team_name
         WHEN f.home_goals < f.away_goals THEN awt.team_name
         ELSE 'Draw'
    END AS result,
    f.venue_name
FROM football.fixtures f JOIN football.teams ht ON f.home_team_id = ht.team_id
                         JOIN football.teams awt ON f.away_team_id = awt.team_id
                         JOIN football.leagues l ON f.league_id = l.league_id AND f.season = l.season;


CREATE OR REPLACE VIEW football.vw_top_players AS
SELECT
    p.player_id,
    l.league_name,
    l.country,
    ps.season,
    p.firstname || ' ' || p.lastname AS player_name,
    p.nationality,
    t.team_name,
    ps.player_position,
    ps.appearances,
    ps.lineups AS starts,
    ps.minutes,
    ps.goals_total,
    ps.assists,
    ps.shots_total,
    ps.shots_on,
    ps.passes_total,
    ps.passes_key,
    ps.passes_accuracy,
    ps.tackles_total,
    ps.duels_total,
    ps.duels_won,
    ps.dribbles_attempts,
    ps.dribbles_success,
    ps.cards_yellow,
    ps.cards_red,
    ps.rating,
    ps.saves
FROM football.player_statistics ps JOIN football.players p ON ps.player_id = p.player_id
                                   JOIN football.teams t ON ps.team_id = t.team_id
                                   JOIN football.leagues l ON ps.league_id = l.league_id AND ps.season = l.season;
