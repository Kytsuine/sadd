CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT,
    abbreviation TEXT
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT
);

CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    away_team_id INTEGER REFERENCES teams (team_id),
    home_team_id INTEGER REFERENCES teams (team_id),
    away_roster INTEGER[] REFERENCES players (player_id),
    home_roster INTEGER[] REFERENCES players (player_id)
);

CREATE TABLE game_extra_data (
    game_id INTEGER PRIMARY KEY,
    season INTEGER,
    game_type INTEGER,
    link TEXT,
    venue_id INTEGER REFERENCES venues (venue_id),
    date TIMESTAMP,
    referees INTEGER[] REFERENCES officials (official_id),
    linesmen INTEGER[] REFERENCES officials (official_id),
    winning_team_id INTEGER REFERENCES teams (team_id),
    losing_team_id INTEGER REFERENCES teams (team_id),
    first_star_id INTEGER REFERENCES players (player_id),
    second_star_id INTEGER REFERENCES players (player_id),
    third_star_id INTEGER REFERENCES players (player_id),
    periods INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    home_coach_id INTEGER REFERENCES coaches (coach_id),
    away_coach_id INTEGER REFERENCES coaches (coach_id),
    home_scratches INTEGER[] REFERENCES players (player_id),
    away_scratches INTEGER[] REFERENCES players (player_id),
    home_penalty_minutes INTEGER,
    away_penalty_minutes INTEGER,
    home_power_play_goals INTEGER,
    away_power_play_goals INTEGER,
    home_power_play_opportunities INTEGER,
    away_power_play_opportunities INTEGER,
    home_blocked_shots INTEGER,
    away_blocked_shots INTEGER,
    home_takeaways INTEGER,
    away_takeaways INTEGER,
    home_giveaways INTEGER,
    away_giveaways INTEGER,
    home_hits INTEGER,
    away_hits INTEGER
);

CREATE TABLE coaches (
    coach_id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE venues (
    venue_id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE officials (
    official_id INTEGER PRIMARY KEY,
    name TEXT,
    link TEXT
);

CREATE TABLE plays (
    play_id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games (game_id) ON DELETE CASCADE,
    player_ids INTEGER[] REFERENCES players (player_id) ON DELETE SET NULL,
    result TEXT,
    period INTEGER,
    period_time TIME,
    goals_away INTEGER,
    goals_home INTEGER,
    x_coordinate INTEGER,
    y_coordinate INTEGER,
    team_id INTEGER REFERENCES teams (team_id) ON DELETE SET NULL
);

CREATE TABLE shots (
    shot_id SERIAL PRIMARY KEY,
    play_id INTEGER REFERENCES plays (play_id) ON DELETE CASCADE,
    game_id INTEGER REFERENCES games (game_id) ON DELETE SET NULL,
    team_id INTEGER REFERENCES teams (team_id) ON DELETE SET NULL,
    shooter_id INTEGER REFERENCES players (player_id) ON DELETE SET NULL,
    goalie_id INTEGER REFERENCES players (player_id) ON DELETE SET NULL,
    CONSTRAINT shot_result_check CHECK (result IN ('Shot', 'Goal'))
);



