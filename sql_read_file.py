import psycopg2
import os
import json

# Define function to insert game data
def insert_game(game_data, conn):
    game_id = game_data['gamePk']
    game_status = game_data['gameData']['status']['codedGameState']
    home_team_id = game_data['gameData']['teams']['home']['id']
    away_team_id = game_data['gameData']['teams']['away']['id']

    cur = conn.cursor()

    # Check if the game exists in the games table
    check_query = "SELECT 1 FROM games WHERE game_id = %s;"
    cur.execute(check_query, (game_id,))

    # If the game doesn't exist and the game status is greater than 5, insert it into the games table
    if cur.rowcount == 0 and int(game_status) > 5:
        insert_query = """INSERT INTO games
                          (game_id, home_team_id, away_team_id)
                          VALUES (%s, %s, %s);"""
        cur.execute(insert_query, (game_id, home_team_id, away_team_id))
        conn.commit()

    cur.close()

def insert_game_extra_data(game_data, conn):
    game_id = game_data['gamePk']
    game_date = game_data['gameData']['datetime']['dateTime']
    game_link = game_data['link']
    game_type = game_data['gameData']['game']['type']
    venue = game_data['gameData']['venue']['name']
    periods = game_data['liveData']['linescore']['currentPeriod']
    home_score = game_data['liveData']['linescore']['teams']['home']['goals']
    away_score = game_data['liveData']['linescore']['teams']['away']['goals']

    cur = conn.cursor()

    # Check if the game exists in the game_extra_data table
    check_query = "SELECT 1 FROM game_extra_data WHERE game_id = %s;"
    cur.execute(check_query, (game_id,))

    # If the game doesn't exist, insert it into the game_extra_data table
    if cur.rowcount == 0:
        insert_query = """INSERT INTO game_extra_data
                          (game_id, date, link, game_type, venue_id, periods, home_score, away_score)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(insert_query, (game_id, game_date, game_link, game_type, venue, periods, home_score, away_score))
        conn.commit()

    cur.close()

def insert_players(data, conn):
    players_data = data['gameData']['players']

    cur = conn.cursor()

    for player_id, player_data in players_data.items():
        # Get the correct player_id and name
        correct_player_id = player_data['person']['id']
        name = player_data['person']['fullName']

        # Check if the player exists in the players table
        check_query = "SELECT 1 FROM players WHERE player_id = %s;"
        cur.execute(check_query, (correct_player_id,))

        # If the player doesn't exist, insert it into the players table
        if cur.rowcount == 0:
            insert_query = """INSERT INTO players
                              (player_id, name)
                              VALUES (%s, %s);"""
            cur.execute(insert_query, (correct_player_id, name))
            conn.commit()

    cur.close()


def insert_officials(data, conn):
    officials_data = data['liveData']['boxscore']['officials']

    cur = conn.cursor()

    for official in officials_data:
        official_id = official['official']['id']
        name = official['official']['fullName']
        link = official['official']['link']

        # Check if the official exists in the officials table
        check_query = "SELECT 1 FROM officials WHERE official_id = %s;"
        cur.execute(check_query, (official_id,))

        # If the official doesn't exist, insert it into the officials table
        if cur.rowcount == 0:
            insert_query = """INSERT INTO officials
                              (official_id, name, link)
                              VALUES (%s, %s, %s);"""
            cur.execute(insert_query, (official_id, name, link))
            conn.commit()

    cur.close()

    
def insert_teams(data, conn):
    # Extract team data from the JSON data
    away_team_data = data['gameData']['teams']['away']
    home_team_data = data['gameData']['teams']['home']

    # Create a list of teams for convenience
    teams = [away_team_data, home_team_data]

    # Iterate through the teams and check if they exist in the database
    for team in teams:
        team_id = team['id']
        name = team['name']
        abbreviation = team['abbreviation']

        # Connect to the database and create a cursor
        cur = conn.cursor()

        # Check if the team exists in the database
        check_query = "SELECT 1 FROM teams WHERE team_id = %s;"
        cur.execute(check_query, (team_id,))

        # If the team doesn't exist, insert it into the teams table
        if cur.rowcount == 0:
            insert_query = "INSERT INTO teams (team_id, name, abbreviation) VALUES (%s, %s, %s);"
            cur.execute(insert_query, (team_id, name, abbreviation))
            conn.commit()

        # Close the cursor
        cur.close()
        
def insert_shifts(shift_data, conn):
    # Connect to the database and create a cursor
    cur = conn.cursor()

    # Iterate through all shifts in the shift_data
    for shift in shift_data:
        game_id = shift['gameId']
        player_id = shift['playerId']
        shift_id = shift['shiftId']
        period = shift['period']
        start_time = shift['startTime']
        end_time = shift['endTime']

        # Check if the shift exists in the shifts table
        check_query = "SELECT 1 FROM shifts WHERE game_id = %s AND shift_id = %s;"
        cur.execute(check_query, (game_id, shift_id))

        # If the shift doesn't exist, insert it into the shifts table
        if cur.rowcount == 0:
            insert_query = """INSERT INTO shifts
                              (game_id, player_id, shift_id, period, start_time, end_time)
                              VALUES (%s, %s, %s, %s, %s, %s);"""
            cur.execute(insert_query, (game_id, player_id, shift_id, period, start_time, end_time))
            conn.commit()

    # Close the cursor
    cur.close()
    
def insert_plays(game_data, conn):
    # Extract necessary game data from the JSON game_data
    game_id = game_data['gameData']['game']['pk']

    # Connect to the database and create a cursor
    cur = conn.cursor()

    # Check if the plays for the game exist in the plays table
    check_query = "SELECT 1 FROM plays WHERE game_id = %s;"
    cur.execute(check_query, (game_id,))

    # If the plays for the game don't exist, insert them into the plays table
    if cur.rowcount == 0:
        # Iterate through all plays in the game_data
        for period in game_data['liveData']['plays']['allPlays']:
            play_id = period['about']['eventId']
            play_period = period['about']['period']
            play_time = period['about']['periodTime']
            play_description = period['result']['description']

            insert_query = """INSERT INTO plays
                              (game_id, play_id, play_period, play_time, play_description)
                              VALUES (%s, %s, %s, %s, %s);"""
            cur.execute(insert_query, (game_id, play_id, play_period, play_time, play_description))
            conn.commit()

    # Close the cursor
    cur.close()

    
def insert_shots(game_data, conn):
    # Extract necessary game data from the JSON game_data
    game_id = game_data['gameData']['game']['pk']

    # Connect to the database and create a cursor
    cur = conn.cursor()

    # Check if the shots for the game exist in the shots table
    check_query = "SELECT 1 FROM shots WHERE game_id = %s;"
    cur.execute(check_query, (game_id,))

    # If the shots for the game don't exist, insert them into the shots table
    if cur.rowcount == 0:
        # Iterate through all plays in the game_data
        for period in game_data['liveData']['plays']['allPlays']:
            play_type = period['result']['eventTypeId']
            
            # Check if the play is a shot type
            if play_type in ['SHOT', 'MISSED_SHOT', 'BLOCKED_SHOT', 'GOAL']:
                play_id = period['about']['eventId']
                play_period = period['about']['period']
                play_time = period['about']['periodTime']
                play_description = period['result']['description']

                insert_query = """INSERT INTO shots
                                  (game_id, play_id, play_period, play_time, play_description)
                                  VALUES (%s, %s, %s, %s, %s);"""
                cur.execute(insert_query, (game_id, play_id, play_period, play_time, play_description))
                conn.commit()

    # Close the cursor
    cur.close()

def insert_goals(game_data, conn):
    # Extract necessary game data from the JSON game_data
    game_id = game_data['gameData']['game']['pk']

    # Connect to the database and create a cursor
    cur = conn.cursor()

    # Check if the goals for the game exist in the goals table
    check_query = "SELECT 1 FROM goals WHERE game_id = %s;"
    cur.execute(check_query, (game_id,))

    # If the goals for the game don't exist, insert them into the goals table
    if cur.rowcount == 0:
        # Iterate through all plays in the game_data
        for period in game_data['liveData']['plays']['allPlays']:
            play_type = period['result']['eventTypeId']
            
            # Check if the play is a goal
            if play_type == 'GOAL':
                play_id = period['about']['eventId']
                play_period = period['about']['period']
                play_time = period['about']['periodTime']
                play_description = period['result']['description']

                insert_query = """INSERT INTO goals
                                  (game_id, play_id, play_period, play_time, play_description)
                                  VALUES (%s, %s, %s, %s, %s);"""
                cur.execute(insert_query, (game_id, play_id, play_period, play_time, play_description))
                conn.commit()

    # Close the cursor
    cur.close()

def insert_venues(data, conn):
    venue_name = data['gameData']['venue']['name']

    cur = conn.cursor()

    # Check if the venue exists in the venues table using string matching
    check_query = "SELECT 1 FROM venues WHERE venue_name = %s;"
    cur.execute(check_query, (venue_name,))

    # If the venue doesn't exist, insert it into the venues table
    if cur.rowcount == 0:
        insert_query = """INSERT INTO venues
                          (venue_name)
                          VALUES (%s);"""
        cur.execute(insert_query, (venue_name,))
        conn.commit()

    cur.close()



# Connect to the database - ADJUST ME BEFORE COMMIT
conn = psycopg2.connect(
    database="your_database_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)

# Open the JSON file and parse the data
with open('path/to/game_data.json', 'r') as f:
    game_data = json.load(f)

# Open the JSON file for the shifts and parse the data
with open('path/to/shift_data.json', 'r') as g:
	shift_data = json.load(g)

# Call the functions to insert the data into the respective tables
insert_game_data(conn, game_data)
insert_teams(game_data, conn)
insert_players(game_data, conn)
insert_officials(game_data, conn)
insert_games_extra_data(game_data, conn)
insert_venues(game_data, conn)
insert_plays(game_data, conn)
insert_shots(game_data, conn)
insert_goals(game_data, conn)
insert_shifts(shift_data, conn)
