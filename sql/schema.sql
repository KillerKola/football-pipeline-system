CREATE SCHEMA IF NOT EXISTS football;

CREATE TABLE football.leagues (
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    league_name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    has_standings BOOLEAN,
    PRIMARY KEY (league_id, season)
);

CREATE TABLE football.teams (
    team_id INTEGER PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    founded INTEGER,
    logo TEXT,
    venue_name VARCHAR(100),
    venue_city VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE football.fixtures (
    fixture_id INTEGER PRIMARY KEY,
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    round VARCHAR(100),
    fixture_date TIMESTAMPTZ,

    status_short VARCHAR(10),

    venue_name VARCHAR(150),

    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
	
    home_goals INTEGER,
    away_goals INTEGER,

    halftime_home INTEGER,
    halftime_away INTEGER,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_fixtures_league
        FOREIGN KEY (league_id, season)
        REFERENCES football.leagues (league_id, season),

    CONSTRAINT fk_fixtures_home_team
        FOREIGN KEY (home_team_id)
        REFERENCES football.teams (team_id),

    CONSTRAINT fk_fixtures_away_team
        FOREIGN KEY (away_team_id)
        REFERENCES football.teams (team_id)
);

CREATE TABLE football.standings (
    standing_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    team_id INTEGER NOT NULL,

    team_rank INTEGER,
    points INTEGER,
    form VARCHAR(50),
    status VARCHAR(50),
    description VARCHAR(150),

    played INTEGER,
    win INTEGER,
    draw INTEGER,
    lose INTEGER,
    goals_for INTEGER,
    goals_against INTEGER,

    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT unique_standings UNIQUE (league_id, season, team_id),

    CONSTRAINT fk_standings_league
        FOREIGN KEY (league_id, season)
        REFERENCES football.leagues (league_id, season),

    CONSTRAINT fk_standings_team
        FOREIGN KEY (team_id)
        REFERENCES football.teams (team_id)
);

CREATE TABLE football.players (
    player_id INTEGER PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    age INTEGER CHECK (age > 0),
    birth_date DATE,
    birth_place VARCHAR(100),
    birth_country VARCHAR(100),
    nationality VARCHAR(100),
    height_cm INTEGER CHECK (height_cm > 0),
    weight_kg INTEGER CHECK (weight_kg > 0),
    injured BOOLEAN NOT NULL DEFAULT FALSE,
    photo TEXT,

	created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE football.player_statistics (
	player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,

    player_position VARCHAR(50),
    rating NUMERIC(4,2),
    captain BOOLEAN,

    appearances INTEGER,
    lineups INTEGER,
    minutes INTEGER,

    substitute_in INTEGER,
    substitute_out INTEGER,
    substitute_bench INTEGER,

    shots_total INTEGER,
    shots_on INTEGER,

    goals_total INTEGER,
    goals_conceded INTEGER,
    goals_assists INTEGER,
    goals_saves INTEGER,

    passes_total INTEGER,
    passes_key INTEGER,
    passes_accuracy INTEGER,

    tackles_total INTEGER,
    tackles_blocks INTEGER,
    tackles_interceptions INTEGER,

    duels_total INTEGER,
    duels_won INTEGER,

    dribbles_attempts INTEGER,
    dribbles_success INTEGER,
    dribbles_past INTEGER,

    fouls_drawn INTEGER,
    fouls_committed INTEGER,

    cards_yellow INTEGER,
    cards_yellowred INTEGER,
    cards_red INTEGER,

    penalty_won INTEGER,
    penalty_committed INTEGER,
    penalty_scored INTEGER,
    penalty_missed INTEGER,
    penalty_saved INTEGER,

    CONSTRAINT fk_player_statistics_player
        FOREIGN KEY (player_id) REFERENCES football.players(player_id),

    CONSTRAINT fk_player_statistics_team
        FOREIGN KEY (team_id) REFERENCES football.teams(team_id),

    CONSTRAINT fk_player_statistics_league
        FOREIGN KEY (league_id, season) REFERENCES football.leagues(league_id, season),

    CONSTRAINT pk_player_statistics
        PRIMARY KEY (player_id, team_id, league_id, season)
);