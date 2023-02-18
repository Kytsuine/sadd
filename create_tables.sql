CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT,
    abbreviation TEXT
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT,
    personal_shot_ids INTEGER[] -- array of shot IDs the player was the shooter for
    on_ice_shot_for_ids INTEGER[] -- array of shot IDs the player was on the ice for from the player's team
    on_ice_shot_against_ids INTEGER[] -- array of shot IDs the player was on the ice for from the other team
);

CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    away_team_id INTEGER,
    home_team_id INTEGER,
    away_roster INTEGER[],
    home_roster INTEGER[]
);

CREATE TABLE game_extra_data (
    game_id INTEGER PRIMARY KEY,
    season INTEGER,
    game_type INTEGER,
    link TEXT,
    venue_id INTEGER,
    date TIMESTAMP,
    referees INTEGER[],
    linesmen INTEGER[],
    winning_team_id INTEGER,
    losing_team_id INTEGER,
    first_star_id INTEGER,
    second_star_id INTEGER,
    third_star_id INTEGER,
    periods INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    home_coach_id INTEGER,
    away_coach_id INTEGER,
    home_scratches INTEGER[],
    away_scratches INTEGER[],
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
    game_id INTEGER,
    player_ids INTEGER[],
    result TEXT,
    period INTEGER,
    period_time TIME,
    goals_away INTEGER,
    goals_home INTEGER,
    x_coordinate INTEGER,
    y_coordinate INTEGER,
    team_id INTEGER
);

CREATE TABLE shots (
    shot_id SERIAL PRIMARY KEY,
    play_id INTEGER REFERENCES plays (play_id) ON DELETE CASCADE,
    game_id INTEGER REFERENCES games (game_id) ON DELETE SET NULL,
    team_id INTEGER REFERENCES teams (team_id) ON DELETE SET NULL,
    shooter_id INTEGER REFERENCES players (player_id) ON DELETE SET NULL,
    goalie_id INTEGER REFERENCES players (player_id) ON DELETE SET NULL,
    x_coordinate INTEGER,
    y_coordinate INTEGER,
    CONSTRAINT shot_result_check CHECK (result IN ('Shot', 'Goal'))
);

CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    shot_id INTEGER,
    play_id INTEGER,
    game_id INTEGER,
    team_id INTEGER,
    shooter_id INTEGER,
    goalie_id INTEGER,
    x_coordinate INTEGER,
    y_coordinate INTEGER,
    CONSTRAINT goal_result_check CHECK (result = 'Goal')
);


CREATE TABLE shot_locations (
    x_coordinate INTEGER,
    y_coordinate INTEGER,
    shot_ids INTEGER[],
    PRIMARY KEY (x_coordinate, y_coordinate)
);


-- Add foreign key to players
ALTER TABLE players ADD CONSTRAINT personal_shot_ids_fk FOREIGN KEY (personal_shot_ids) REFERENCES shots (shot_id);
ALTER TABLE players ADD CONSTRAINT on_ice_shot_for_ids_fk FOREIGN KEY (on_ice_shot_for_ids) REFERENCES shots (shot_id);
ALTER TABLE players ADD CONSTRAINT on_ice_shot_against_ids_fk FOREIGN KEY (on_ice_shot_against_ids) REFERENCES shots (shot_id);

-- Add foreign key to games
ALTER TABLE games ADD CONSTRAINT away_roster_fk FOREIGN KEY (away_roster) REFERENCES players (player_id);
ALTER TABLE games ADD CONSTRAINT home_roster_fk FOREIGN KEY (home_roster) REFERENCES players (player_id);
ALTER TABLE games ADD CONSTRAINT away_team_id_fk FOREIGN KEY (away_team_id) REFERENCES teams (team_id);
ALTER TABLE games ADD CONSTRAINT home_team_id_fk FOREIGN KEY (home_team_id) REFERENCES teams (team_id);

-- Add foreign key to games_extra_data
ALTER TABLE game_extra_data ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id);
ALTER TABLE game_extra_data ADD CONSTRAINT venue_id_fk FOREIGN KEY (venue_id) REFERENCES venues (venue_id);
ALTER TABLE game_extra_data ADD CONSTRAINT winning_team_id_fk FOREIGN KEY (winning_team_id) REFERENCES teams (team_id);
ALTER TABLE game_extra_data ADD CONSTRAINT losing_team_id_fk FOREIGN KEY (losing_team_id) REFERENCES teams (team_id);
ALTER TABLE game_extra_data ADD CONSTRAINT first_star_id_fk FOREIGN KEY (first_star_id) REFERENCES players (player_id);
ALTER TABLE game_extra_data ADD CONSTRAINT second_star_id_fk FOREIGN KEY (second_star_id) REFERENCES players (player_id);
ALTER TABLE game_extra_data ADD CONSTRAINT third_star_id_fk FOREIGN KEY (third_star_id) REFERENCES players (player_id);
ALTER TABLE game_extra_data ADD CONSTRAINT home_coach_id_fk FOREIGN KEY (home_coach_id) REFERENCES coaches (coach_id);
ALTER TABLE game_extra_data ADD CONSTRAINT away_coach_id_fk FOREIGN KEY (away_coach_id) REFERENCES coaches (coach_id);
ALTER TABLE game_extra_data ADD CONSTRAINT referees_fk FOREIGN KEY (referees) REFERENCES officials (official_id)
ALTER TABLE game_extra_data ADD CONSTRAINT linesmen_fk FOREIGN KEY (linesmen) REFERENCES officials (official_id)
ALTER TABLE game_extra_data ADD CONSTRAINT home_scratches_fk FOREIGN KEY (home_scratches) REFERENCES players (player_id);
ALTER TABLE game_extra_data ADD CONSTRAINT away_scratches_fk FOREIGN KEY (away_scratches) REFERENCES players (player_id);

-- Add foreign key to plays
ALTER TABLE plays ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id);
ALTER TABLE plays ADD CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES teams (team_id);
ALTER TABLE plays ADD CONSTRAINT player_id_fk FOREIGN KEY (player_id) REFERENCES players (player_id);

-- Add foreign key to shots
ALTER TABLE shots ADD CONSTRAINT play_id_fk FOREIGN KEY (play_id) REFERENCES plays (play_id);
ALTER TABLE shots ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id);
ALTER TABLE shots ADD CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES teams (team_id);
ALTER TABLE shots ADD CONSTRAINT shooter_id_fk FOREIGN KEY (shooter_id) REFERENCES players (player_id);
ALTER TABLE shots ADD CONSTRAINT goalie_id_fk FOREIGN KEY (goalie_id) REFERENCES players (player_id);

-- Add foreign key to goals
ALTER TABLE goals ADD CONSTRAINT shot_id_fk FOREIGN KEY (shot_id) REFERENCES shots (shot_id);
ALTER TABLE goals ADD CONSTRAINT play_id_fk FOREIGN KEY (play_id) REFERENCES plays (play_id);
ALTER TABLE goals ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id);
ALTER TABLE goals ADD CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES teams (team_id);
ALTER TABLE goals ADD CONSTRAINT shooter_id_fk FOREIGN KEY (shooter_id) REFERENCES players (player_id);
ALTER TABLE goals ADD CONSTRAINT goalie_id_fk FOREIGN KEY (goalie_id) REFERENCES players (player_id);

-- Add foreign key to shot_locations
ALTER TABLE shot_locations ADD CONSTRAINT shot_ids_fk FOREIGN KEY (shot_ids) REFERENCES shots (shot_id);
