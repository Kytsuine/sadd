CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY, -- unique identifier for the team
    name TEXT, -- name of the team
    abbreviation TEXT -- abbreviated name of the team
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT, -- full name of the player
    personal_shot_ids INTEGER[] -- array of shot IDs the player was the shooter for
    on_ice_shot_for_ids INTEGER[] -- array of shot IDs the player was on the ice for from the player's team
    on_ice_shot_against_ids INTEGER[] -- array of shot IDs the player was on the ice for from the other team
);

CREATE TABLE games (
    game_id INTEGER PRIMARY KEY, -- unique identifier for each game
    away_team_id INTEGER, -- foreign key referencing the away team in the teams table
    home_team_id INTEGER, -- foreign key referencing the home team in the teams table
    away_roster INTEGER[], -- an array of integers representing the player IDs for the away team roster
    home_roster INTEGER[] -- an array of integers representing the player IDs for the home team roster
);


CREATE TABLE game_extra_data (
    game_id INTEGER PRIMARY KEY, -- unique identifier for the game
    season INTEGER, -- season in which the game was played
    game_type INTEGER, -- type of the game (e.g. regular season, playoffs, etc.)
    link TEXT, -- link to the game summary on the NHL website
    venue_id INTEGER, -- unique identifier for the arena where the game was played
    date TIMESTAMP, -- date and time when the game was played
    referees INTEGER[], -- array of unique identifiers for the referees officiating the game
    linesmen INTEGER[], -- array of unique identifiers for the linesmen officiating the game
    winning_team_id INTEGER, -- unique identifier for the winning team
    losing_team_id INTEGER, -- unique identifier for the losing team
    first_star_id INTEGER, -- unique identifier for the first star of the game
    second_star_id INTEGER, -- unique identifier for the second star of the game
    third_star_id INTEGER, -- unique identifier for the third star of the game
    periods INTEGER, -- number of periods played in the game
    home_score INTEGER, -- number of goals scored by the home team
    away_score INTEGER, -- number of goals scored by the away team
    home_coach_id INTEGER, -- unique identifier for the coach of the home team
    away_coach_id INTEGER, -- unique identifier for the coach of the away team
    home_scratches INTEGER[], -- array of unique identifiers for the scratched players on the home team
    away_scratches INTEGER[], -- array of unique identifiers for the scratched players on the away team
    home_penalty_minutes INTEGER, -- total number of penalty minutes for the home team
    away_penalty_minutes INTEGER, -- total number of penalty minutes for the away team
    home_power_play_goals INTEGER, -- number of power play goals scored by the home team
    away_power_play_goals INTEGER, -- number of power play goals scored by the away team
    home_power_play_opportunities INTEGER, -- number of power play opportunities for the home team
    away_power_play_opportunities INTEGER, -- number of power play opportunities for the away team
    home_blocked_shots INTEGER, -- number of blocked shots by the home team
    away_blocked_shots INTEGER, -- number of blocked shots by the away team
    home_takeaways INTEGER, -- number of takeaways by the home team
    away_takeaways INTEGER, -- number of takeaways by the away team
    home_giveaways INTEGER, -- number of giveaways by the home team
    away_giveaways INTEGER, -- number of giveaways by the away team
    home_hits INTEGER, -- number of hits by the home team
    away_hits INTEGER -- number of hits by the away team
);



CREATE TABLE coaches (
    coach_id SERIAL PRIMARY KEY, -- Unique identifier for the coach.
    name TEXT -- The name of the coach.
);


CREATE TABLE venues (
    venue_id SERIAL PRIMARY KEY, -- Unique identifier for the venue.
    name TEXT -- The name of the venue.
);

CREATE TABLE officials (
    official_id INTEGER PRIMARY KEY, -- Unique identifier for the official.
    name TEXT, -- The name of the official.
    link TEXT -- A link to the official's profile on the NHL's website.
);


CREATE TABLE plays (
    play_id SERIAL PRIMARY KEY, -- Unique ID for each play
    game_id INTEGER, -- ID of the game in which the play occurred
    player_ids INTEGER[], -- Array of player IDs involved in the play
    result TEXT, -- Description of the play's outcome
    period INTEGER, -- Period in which the play occurred (1-3, OT)
    period_time TIME, -- Time on the game clock when the play occurred
    goals_away INTEGER, -- Number of goals scored by the away team before the play
    goals_home INTEGER, -- Number of goals scored by the home team before the play
    x_coordinate INTEGER, -- X-coordinate of the location on the rink where the play occurred
    y_coordinate INTEGER, -- Y-coordinate of the location on the rink where the play occurred
    team_id INTEGER -- ID of the team involved in the play
);


CREATE TABLE shots (
    shot_id SERIAL PRIMARY KEY, -- unique identifier for each shot
    play_id INTEGER, -- the play that led to the shot
    game_id INTEGER, -- the game in which the shot occurred
    team_id INTEGER, -- the team that took the shot
    shooter_id INTEGER, -- the player who took the shot
    goalie_id INTEGER, -- the goalie who faced the shot
    x_coordinate INTEGER, -- the x-coordinate of the shot location on the rink
    y_coordinate INTEGER, -- the y-coordinate of the shot location on the rink
    CONSTRAINT shot_result_check CHECK (result IN ('Shot', 'Goal')) -- ensures that the result of the shot is either a shot or a goal
);

CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY, -- unique identifier for each goal
    shot_id INTEGER, -- the shot that resulted in the goal
    play_id INTEGER, -- the play that led to the goal
    game_id INTEGER, -- the game in which the goal occurred
    team_id INTEGER, -- the team that scored the goal
    shooter_id INTEGER, -- the player who scored the goal
    goalie_id INTEGER, -- the goalie who allowed the goal
    x_coordinate INTEGER, -- the x-coordinate of the goal location on the rink
    y_coordinate INTEGER, -- the y-coordinate of the goal location on the rink
    CONSTRAINT goal_result_check CHECK (result = 'Goal') -- ensures that the result of the goal is a goal
);


CREATE TABLE shot_locations (
    x_coordinate INTEGER, -- the x-coordinate of the shot location on the rink
    y_coordinate INTEGER, -- the y-coordinate of the shot location on the rink
    shot_ids INTEGER[], -- the IDs of the shots that occurred at this location
    PRIMARY KEY (x_coordinate, y_coordinate) -- primary key to ensure uniqueness of coordinates
);



-- Add foreign key to players
ALTER TABLE players 
ADD CONSTRAINT personal_shot_ids_fk FOREIGN KEY (personal_shot_ids) REFERENCES shots (shot_id),
ADD CONSTRAINT on_ice_shot_for_ids_fk FOREIGN KEY (on_ice_shot_for_ids) REFERENCES shots (shot_id),
ADD CONSTRAINT on_ice_shot_against_ids_fk FOREIGN KEY (on_ice_shot_against_ids) REFERENCES shots (shot_id);

-- Add foreign key to games
ALTER TABLE games 
  ADD CONSTRAINT away_roster_fk FOREIGN KEY (away_roster) REFERENCES players (player_id),
  ADD CONSTRAINT home_roster_fk FOREIGN KEY (home_roster) REFERENCES players (player_id),
  ADD CONSTRAINT away_team_id_fk FOREIGN KEY (away_team_id) REFERENCES teams (team_id) ON DELETE SET NULL,
  ADD CONSTRAINT home_team_id_fk FOREIGN KEY (home_team_id) REFERENCES teams (team_id) ON DELETE SET NULL;


-- Add foreign key to games_extra_data
ALTER TABLE game_extra_data
ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE CASCADE,
ADD CONSTRAINT venue_id_fk FOREIGN KEY (venue_id) REFERENCES venues (venue_id) ON DELETE SET NULL,
ADD CONSTRAINT winning_team_id_fk FOREIGN KEY (winning_team_id) REFERENCES teams (team_id) ON DELETE SET NULL,
ADD CONSTRAINT losing_team_id_fk FOREIGN KEY (losing_team_id) REFERENCES teams (team_id) ON DELETE SET NULL,
ADD CONSTRAINT first_star_id_fk FOREIGN KEY (first_star_id) REFERENCES players (player_id) ON DELETE SET NULL,
ADD CONSTRAINT second_star_id_fk FOREIGN KEY (second_star_id) REFERENCES players (player_id) ON DELETE SET NULL,
ADD CONSTRAINT third_star_id_fk FOREIGN KEY (third_star_id) REFERENCES players (player_id) ON DELETE SET NULL,
ADD CONSTRAINT home_coach_id_fk FOREIGN KEY (home_coach_id) REFERENCES coaches (coach_id) ON DELETE SET NULL,
ADD CONSTRAINT away_coach_id_fk FOREIGN KEY (away_coach_id) REFERENCES coaches (coach_id) ON DELETE SET NULL,
ADD CONSTRAINT referees_fk FOREIGN KEY (referees) REFERENCES officials (official_id) ON DELETE SET NULL,
ADD CONSTRAINT linesmen_fk FOREIGN KEY (linesmen) REFERENCES officials (official_id) ON DELETE SET NULL,
ADD CONSTRAINT home_scratches_fk FOREIGN KEY (home_scratches) REFERENCES players (player_id),
ADD CONSTRAINT away_scratches_fk FOREIGN KEY (away_scratches) REFERENCES players (player_id);

-- Add foreign key to plays
ALTER TABLE plays
ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE SET NULL,
ADD CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE SET NULL,
ADD CONSTRAINT player_ids_fk FOREIGN KEY (player_ids) REFERENCES players (player_id);


-- Add foreign key to shots
ALTER TABLE shots 
ADD CONSTRAINT play_id_fk FOREIGN KEY (play_id) REFERENCES plays (play_id) ON DELETE CASCADE,
ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE SET NULL,
ADD CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE SET NULL,
ADD CONSTRAINT shooter_id_fk FOREIGN KEY (shooter_id) REFERENCES players (player_id) ON DELETE SET NULL,
ADD CONSTRAINT goalie_id_fk FOREIGN KEY (goalie_id) REFERENCES players (player_id) ON DELETE SET NULL;


-- Add foreign key to goals
ALTER TABLE goals
ADD CONSTRAINT shot_id_fk FOREIGN KEY (shot_id) REFERENCES shots (shot_id) ON DELETE CASCADE,
ADD CONSTRAINT play_id_fk FOREIGN KEY (play_id) REFERENCES plays (play_id) ON DELETE CASCADE,
ADD CONSTRAINT game_id_fk FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE SET NULL,
ADD CONSTRAINT team_id_fk FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE SET NULL,
ADD CONSTRAINT shooter_id_fk FOREIGN KEY (shooter_id) REFERENCES players (player_id) ON DELETE SET NULL,
ADD CONSTRAINT goalie_id_fk FOREIGN KEY (goalie_id) REFERENCES players (player_id) ON DELETE SET NULL;


-- Add foreign key to shot_locations
ALTER TABLE shot_locations ADD CONSTRAINT shot_ids_fk FOREIGN KEY (shot_ids) REFERENCES shots (shot_id);
