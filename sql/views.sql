CREATE VIEW football.vw_league_table AS
SELECT
    s.league_id,
    s.season,
    s.team_id,
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
    s.form,
    s.status,
    s.description
FROM football.standings s JOIN football.teams t ON s.team_id = t.team_id;

CREATE VIEW football.vw_match_results AS
SELECT
    f.fixture_id,
    f.league_id,
    f.season,
    f.round,
    f.fixture_date,
    f.status_short,
    ht.team_name AS home_team,
    awt.team_name AS away_team,
    f.home_goals,
    f.away_goals,
    f.venue_name
FROM football.fixtures f JOIN football.teams ht ON f.home_team_id = ht.team_id
                         JOIN football.teams awt ON f.away_team_id = awt.team_id;

CREATE VIEW football.vw_top_players AS
SELECT
    ps.league_id,
    ps.season,
    ps.player_id,
    CONCAT(p.firstname, ' ', p.lastname) AS player_name,
    t.team_name,
    ps.player_position,
    ps.appearances,
    ps.minutes,
    ps.goals_total,
    ps.assists,
    ps.rating
FROM football.player_statistics ps JOIN football.players p ON ps.player_id = p.player_id
                                   JOIN football.teams t ON ps.team_id = t.team_id;