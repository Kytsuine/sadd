CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY, -- unique identifier for the team
    name TEXT, -- name of the team
    abbreviation TEXT -- abbreviated name of the team
);

CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT, -- full name of the player
    personal_shot_ids INTEGER[] -- array of shot IDs the player was the shooter for
    personal_goal_ids INTEGER[] -- array of goal IDs the player was the shooter for
    on_ice_shot_for_ids INTEGER[] -- array of shot IDs the player was on the ice for from the player's team
    on_ice_goal_for_ids INTEGER[] -- array of goal IDs the player was on the ice for from the player's team
    on_ice_shot_against_ids INTEGER[] -- array of shot IDs the player was on the ice for from the other team
    on_ice_goal_against_ids INTEGER[] -- array of goal IDs the player was on the ice for from the other team
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
    game_type INTEGER, -- type of the game (e.g. regular season, playoffs, etc.)
    link TEXT, -- link to the game summary on the NHL website
    venue_id INTEGER, -- unique identifier for the arena where the game was played
    date TIMESTAMP, -- date and time when the game was played
    referees INTEGER[], -- array of unique identifiers for the referees officiating the game
    linesmen INTEGER[], -- array of unique identifiers for the linesmen officiating the game
    winning_team_id INTEGER, -- unique identifier for the winning team
    losing_team_id INTEGER, -- unique identifier for the losing team
    periods INTEGER, -- number of periods played in the game
    home_score INTEGER, -- number of goals scored by the home team
    away_score INTEGER, -- number of goals scored by the away team
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
    game_play_idx INTEGER -- Index number of the play within the game
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

);


CREATE TABLE shot_locations (
    x_coordinate INTEGER, -- the x-coordinate of the shot location on the rink
    y_coordinate INTEGER, -- the y-coordinate of the shot location on the rink
    shot_ids INTEGER[], -- the IDs of the shots that occurred at this location
    goal_ids INTEGER[], -- the IDs of the goals that occurred at this location
    PRIMARY KEY (x_coordinate, y_coordinate) -- primary key to ensure uniqueness of coordinates
);

CREATE TABLE player_shot_locations (
    player_id INTEGER,
    x_coordinate INTEGER,
    y_coordinate INTEGER,
    shots INTEGER,
    goals INTEGER,
    shooting_pct NUMERIC,
    PRIMARY KEY (player_id, x_coordinate, y_coordinate)
);

-- Create functions to check values for shots and goals tables
CREATE OR REPLACE FUNCTION validate_shot()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM plays WHERE play_id = NEW.play_id AND result IN ('Shot', 'Goal')
  ) THEN
    RAISE EXCEPTION 'Not a shot', NEW.play_id;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION validate_goal()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM plays WHERE play_id = NEW.play_id AND result = 'Goal'
  ) THEN
    RAISE EXCEPTION 'Not a goal', NEW.play_id;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Create triggers to implement above functions
CREATE TRIGGER validate_shot_trigger
BEFORE INSERT OR UPDATE ON shots
FOR EACH ROW
EXECUTE FUNCTION validate_shot();

CREATE TRIGGER validate_goal_trigger
BEFORE INSERT OR UPDATE ON goals
FOR EACH ROW
EXECUTE FUNCTION validate_goal();


-- Add foreign key to players
ALTER TABLE players 
ADD CONSTRAINT personal_shot_ids_fk FOREIGN KEY (personal_shot_ids) REFERENCES shots (shot_id),
ADD CONSTRAINT personal_goal_ids_fk FOREIGN KEY (personal_goal_ids) REFERENCES goals (goal_id),
ADD CONSTRAINT on_ice_shot_for_ids_fk FOREIGN KEY (on_ice_shot_for_ids) REFERENCES shots (shot_id),
ADD CONSTRAINT on_ice_goal_for_ids_fk FOREIGN KEY (on_ice_goal_for_ids) REFERENCES goals (goal_id),
ADD CONSTRAINT on_ice_shot_against_ids_fk FOREIGN KEY (on_ice_shot_against_ids) REFERENCES shots (shot_id);
ADD CONSTRAINT on_ice_goal_against_ids_fk FOREIGN KEY (on_ice_goal_against_ids) REFERENCES goals (goal_id);

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
ADD CONSTRAINT referees_fk FOREIGN KEY (referees) REFERENCES officials (official_id) ON DELETE SET NULL,
ADD CONSTRAINT linesmen_fk FOREIGN KEY (linesmen) REFERENCES officials (official_id) ON DELETE SET NULL;


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
ALTER TABLE shot_locations 
ADD CONSTRAINT shot_ids_fk FOREIGN KEY (shot_ids) REFERENCES shots (shot_id)
ADD CONSTRAINT goal_ids_fk FOREIGN KEY (goal_ids) REFERENCES goals (goal_id);

-- Add foreign key to player_shot_locations
ALTER TABLE player_shot_locations
ADD CONSTRAINT player_id_fk FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE;


/* This code should be run after the tables are populated, and populates shot_locations with a shooting_pct column. Should probably be amended to return 0 for locations with less than n shots, but idk what n should be yet.
-- Compute shooting percentage for each shot location
UPDATE shot_locations
SET shooting_pct = (
    CASE
        WHEN array_length(goal_ids, 1) > 0 THEN array_length(shot_ids, 1)::float / array_length(goal_ids, 1)::float
        ELSE 0
    END
);
*/

/* This code should be run after the tables are populated, and populated player_shot_locations.
INSERT INTO player_shot_locations (player_id, x_coordinate, y_coordinate, num_shots, num_goals, shooting_pct)
SELECT 
    p.player_id, 
    sl.x_coordinate, 
    sl.y_coordinate, 
    COUNT(s.shot_id), 
    COUNT(g.goal_id),
    COUNT(g.goal_id)::FLOAT / COUNT(s.shot_id) AS shooting_pct
FROM 
    players p 
    JOIN shots s ON p.personal_shot_ids @> ARRAY[s.shot_id] 
    JOIN shot_locations sl ON s.x_coordinate = sl.x_coordinate AND s.y_coordinate = sl.y_coordinate
    JOIN goals g ON s.shot_id = g.shot_id AND p.personal_goal_ids @> ARRAY[g.goal_id]
GROUP BY 
    p.player_id, 
    sl.x_coordinate, 
    sl.y_coordinate;
*/


