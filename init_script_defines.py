#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import time
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np

# In[2]:


# Open the files for each dictionary

'''with open('./data/games_trimmed.pkl', 'rb') as f:
    games_trimmed = pickle.load(f)

with open('./data/game_shifts.pkl', 'rb') as f:
    game_shifts = pickle.load(f)

with open('./data/coordinate_shots.pkl', 'rb') as f:
    coordinate_shots = pickle.load(f)

with open('./data/player_teams.pkl', 'rb') as f:
    player_teams = pickle.load(f)

with open('./data/player_id_games.pkl', 'rb') as f:
    player_id_games = pickle.load(f)

with open('./data/team_games.pkl', 'rb') as f:
    team_games = pickle.load(f)

with open('./data/player_bisplreps.pkl', 'rb') as f:
    player_bisplreps = pickle.load(f)

with open('./data/player_coordinates.pkl', 'rb') as f:
    player_coordinates = pickle.load(f)'''

# The dictionaries have been loaded into memory and can now be accessed as usual.


# The following functions are used actively in the analysis work I've been doing. They are mostly focused on hockey data analysis.


def get_game_year(gameID):
    # Divide the gameID by 1,000,000 to retrieve the year in which the game was played
    game_year = gameID // 1000000
    
    # Return the game_year
    return game_year


def time_test(func, args=None, n=100):
    # Initialize an empty list to store the time taken for each iteration
    time_list = []
    # Iterate over a range of values from 1 to n
    for j in range(1, n):
        # Store the start time of the iteration
        start = time.time()
        # Call the function with the given argument
        func(args)
        # Store the end time of the iteration
        end = time.time()

        # Calculate and print the time taken for the iteration
        print(f"Iteration: ", {j}, "Time taken: ", (end-start)*10**3, "ms", end="\r")
        # Append the time taken for the iteration to the time_list
        time_list.append((end-start)*10**3)
    # Initialize variables to store the total and count of time values
    total = 0
    count = 0

    # Iterate over the time_list and calculate the total and count
    for number in time_list:
        total += number
        count += 1
    # Calculate and print the average time taken
    print(f"Average time taken for ", str(func), ": ", total/count, "ms\n")


def get_players_on_ice(gameID, period, periodTime):
    if game_shifts = None:
        global game_shifts
        game_shifts = build_game_shifts()

    # Retrieve the game dataframe corresponding to the gameID
    game_dataframe = game_shifts[gameID]

    # Check that the period is within the range of 1-3. If not, return a null value.
    if period not in range(1,4):
        return None

    # Identify the period of the shot to find the corresponding shifts_n column
    shift_column = "shifts_" + str(period)

    # Initialize an empty list to store the player_ids for players on the ice
    player_ids = []

    # Loop through each row in the game dataframe
    for index, row in game_dataframe.iterrows():
        # Retrieve the shift tuples for the current player
        shift_tuples = row[shift_column]

        # Check which players had a shift time tuple that includes periodTime
        for shift_tuple in shift_tuples:
            if shift_tuple[0] < periodTime <= shift_tuple[1]:
                player_ids.append(row['player_id'])

    return player_ids


def get_player_shots(player_id):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # Initialize an empty list to store the shots taken when the player was on the ice.
    player_shots = []

    # Retrieve the games for the player from the player_id_games dictionary
    games = player_id_games[player_id]

    # Iterate over the keys in the games dictionary
    for year, gameIDs in games.items():
        # Iterate over the gameIDs in the list of gameIDs for the current year
        for gameID in gameIDs:
            # Retrieve the game dictionary for the current gameID
            game_dict = games_trimmed[gameID]

            # Iterate over the shots in the game
            for shot_num, shot in game_dict.items():
                periodTime = shot['about']['periodTime']
                period = shot['about']['period']

                # Check if the player was on the ice at the time of the shot
                players_on_ice = get_players_on_ice(gameID, period, periodTime)
                if players_on_ice is not None and player_id in players_on_ice:
                    # Append a tuple (game_ID, shot_num) to the list of player shots
                    player_shots.append((gameID, shot_num))

    return player_shots


def get_shots_by_player(player_id):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # Initialize an empty list to store the shots taken by the player.
    player_shots = []

    # Retrieve the games for the player from the player_id_games dictionary
    games = player_id_games[player_id]

    # Iterate over the keys in the games dictionary
    for year, gameIDs in games.items():
        # Iterate over the gameIDs in the list of gameIDs for the current year
        for gameID in gameIDs:
            # Retrieve the game dictionary for the current gameID
            game_dict = games_trimmed[gameID]

            # Iterate over the shots in the game
            for shot_num, shot in game_dict.items():
                periodTime = shot['about']['periodTime']
                period = shot['about']['period']

                # Check if the shot was taken in periods 1-3
                if period in range(1, 4):
                    # Check if the player took the shot
                    if shot['players'][0]['player']['id'] == player_id:
                        # Append a tuple (game_ID, shot_num) to the list of player shots
                        player_shots.append((gameID, shot_num))

    return player_shots


# In[14]:


def get_player_shots_against(player_id, games_trimmed=games_trimmed, player_id_games=player_id_games, player_teams=player_teams):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if player_teams is None:
        global player_teams
        player_teams = build_player_teams()

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # Initialize an empty list to store the shots taken when the player was on the ice against teams they didn't play for.
    player_shots = []

    # Retrieve the games for the player from the player_id_games dictionary
    games = player_id_games[player_id]

    # Retrieve the teams that playerID played for from the player_teams dictionary
    teams = player_teams[player_id]

    # Iterate over the keys in the games dictionary
    for year, gameIDs in games.items():
        # Retrieve the list of teams playerID played for in the current year
        player_teams_year = teams[year]

        # Iterate over the gameIDs in the list of gameIDs for the current year
        for gameID in gameIDs:
            # Retrieve the list of shots for the current gameID
            shots = games_trimmed[gameID].values()

            # Iterate over the shots in the game
            for shot_location in shots:
                game_id, shot_num = shot_location
                shot = games_trimmed[game_id][shot_num]

                # Retrieve the triCode of the team that took the shot
                shot_triCode = shot['team']['triCode']

                # Check if the triCode of the shot does not match any of the teams playerID played for in that year
                if shot_triCode not in player_teams_year:
                    periodTime = shot['about']['periodTime']
                    period = shot['about']['period']

                    # Check if the player was on the ice at the time of the shot
                    players_on_ice = get_players_on_ice(gameID, period, periodTime)
                    if players_on_ice is not None and player_id in players_on_ice:
                        player_shots.append(shot_location)

    return player_shots


def get_goal_shot_ratio(player_id, player_shots=None, count=False):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # If player_shots is not provided, retrieve them using the get_player_shots function
    if player_shots is None:
        player_shots = get_player_shots(player_id)

    # If the player has never been on the ice for a shot, return 0
    if len(player_shots) == 0:
        return 0

    # Initialize counters for the number of goals and shots
    goal_count = 0
    shot_count = 0

    # Loop through the shot dictionaries in the player_shots list
    for shot_location in player_shots:
        game_id, shot_num = shot_location
        shot = games_trimmed[game_id][shot_num]

        # Check the event type of the shot (either 'Goal' or 'Shot')
        event_type = shot['result']['event']

        # If the event is a goal, increment the goal_count
        if event_type == 'Goal':
            goal_count += 1

        # If the event is a shot, increment the shot_count
        if event_type in ('Goal', 'Shot'):
            shot_count += 1

    # Calculate the proportion of goals to shots by dividing the number of goals by the number of shots
    proportion_of_goals = goal_count / shot_count

    if count:
        return (proportion_of_goals, shot_count)
    else:
        return (proportion_of_goals)


def get_coordinate_goal_shot_ratio_against(player_id, coordinate, games_trimmed=games_trimmed, player_id_games=player_id_games, coordinate_shots=coordinate_shots):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if coordinate_shots is None:
        global coordinate_shots
        coordinate_shots = build_coordinate_shots()

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # Retrieve the player_shots using the get_player_shots function
    player_shots = get_player_shots_against(player_id, player_id_games)

    # Filter the player_shots list to only include shots taken from the given coordinate
    player_shots_at_coordinate = []
    for location in coordinate_shots[coordinate]:
        game_id, shot_num = location
        shot = games_trimmed[game_id][shot_num]
        if shot in player_shots:
            player_shots_at_coordinate.append(shot)

    # Use the get_goal_shot_ratio function to calculate the proportion of goals to shots for the player_shots_at_coordinate list
    proportion_of_goals = get_goal_shot_ratio_against(player_id, player_id_games, player_shots_at_coordinate)

    # Return the proportion_of_goals
    return proportion_of_goals



def get_coordinate_goal_shot_ratio(x, y, count=False):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if coordinate_shots is None:
        global coordinate_shots
        coordinate_shots = build_coordinate_shots()

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # Initialize counters for the number of goals and shots
    goal_count = 0
    shot_count = 0

    # Check if the x, y coordinate exists as a key in the coordinate_shots dictionary
    if (x, y) in coordinate_shots:
        # If the x, y coordinate exists as a key, retrieve the list of locations in games_trimmed where shots were taken from that coordinate
        locations = coordinate_shots[(x, y)]

        # Loop through the locations in the list
        for location in locations:
            # Retrieve the shot dictionary from games_trimmed using the location (game ID and shot number)
            game_id, shot_num = location
            shot = games_trimmed[game_id][shot_num]

            # Check the event type of the shot (either 'Goal' or 'Shot')
            event_type = shot['result']['event']

            # If the event is a goal, increment the goal_count
            if event_type == 'Goal':
                goal_count += 1

            # If the event is a shot, increment the shot_count
            if event_type in ('Goal', 'Shot'):
                shot_count += 1

    # Calculate the proportion of goals to shots by dividing the number of goals by the number of shots
    proportion_of_goals = goal_count / shot_count

    # Return the proportion of goals type as requested by the count argument
    if count:
        return (proportion_of_goals, shot_count)
    else:
        return (proportion_of_goals)


def get_coordinate_goal_shot_ratio_against(player_id, x, y, player_shots=None):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    if coordinate_shots is None:
        global coordinate_shots
        coordinate_shots = build_coordinate_shots()

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # If player_shots is not provided, retrieve the player_shots using the get_shots_by_player function
    if player_shots is None:
        player_shots = get_player_shots_against(player_id, player_id_games)

    # Convert the coordinate_shots and player_shots lists to sets and compute their intersection
    coordinate_player_shots = set(coordinate_shots[(x, y)]) & set(player_shots)

    # Use the get_goal_shot_ratio function to calculate the proportion of goals to shots for the coordinate_player_shots list
    proportion_of_goals = get_goal_shot_ratio(player_id, player_id_games, coordinate_player_shots, games_trimmed=games_trimmed)

    # Return the proportion_of_goals
    return proportion_of_goals


def get_coordinate_goal_shot_ratio_for_player(player_id, x, y, player_shots=None):

    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    # If player_shots is not provided, retrieve the player_shots using the get_shots_by_player function
    if player_shots is None:
        player_shots = get_shots_by_player(player_id, player_id_games)

    if coordinate_shots is None:
        global coordinate_shots
        coordinate_shots = build_coordinate_shots()

    if player_id_games is None:
        global player_id_games
        player_id_games = build_player_id_games()

    # Convert the coordinate_shots and player_shots lists to sets and compute their intersection
    coordinate_player_shots = set(coordinate_shots[(x, y)]) & set(player_shots)

    # Use the get_goal_shot_ratio function to calculate the proportion of goals to shots for the coordinate_player_shots list
    proportion_of_goals = get_goal_shot_ratio(player_id, player_id_games = player_id_games, player_shots = coordinate_player_shots, games_trimmed=games_trimmed, count=1)

    # Return the proportion_of_goals
    return proportion_of_goals


def build_player_coordinate_list():
    if player_id_games = None:
        global player_id_games
        player_id_games = build_player_id_games()
    # Get a list of player IDs from the player_id_games dictionary
    if player_id_list = None:
        global player_id_list
        player_id_list = build_player_id_list()

    # Create an empty dictionary to store player coordinates
    player_coordinates = {}

    # Loop through each player ID in the player_id_list
    for playerID in player_id_list:
        # If the player ID is not in the player_coordinates dictionary, add an empty list for that player
        if playerID not in player_coordinates:
            player_coordinates[playerID] = []

        # Get the shots for the current player
        player_shots = get_shots_by_player(playerID)

        # Loop through each shot for the current player
        for shot in player_shots:
            # Check if the 'x' and 'y' keys are present in the coordinates dictionary
            if 'x' in shot['coordinates'] and 'y' in shot['coordinates']:
                # If the keys are present, create a tuple of the x and y coordinates
                coordinate = (shot['coordinates']['x'], shot['coordinates']['y'])

                # Append the coordinate tuple to the list of coordinates for the current player
                player_coordinates[playerID].append(coordinate)

    # Return the dictionary of player coordinates
    return player_coordinates


def build_home_away_teams(directory='.'):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    home_away_teams = {}
    # Loop through the .json files in the directory
    for file_name in json_files:
        # Construct the file path for the current .json file
        file_path = os.path.join(directory, file_name)
        # Open the .json file and load the data into a dictionary
        with open(file_path, encoding='utf-8') as json_file:
            game_data = json.load(json_file)

            # Retrieve the teams data from the game file
            teams = game_data['gameData']['teams']

            # Retrieve the triCodes for the home and away teams
            home_triCode = teams['home']['triCode']
            away_triCode = teams['away']['triCode']

            # Add an entry to the home_away_teams dictionary for the current gameID with the home and away teams as the value
            home_away_teams[gameID] = (home_triCode, away_triCode)

    return home_away_teams


def build_coordinate_shots():
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    # Initialize an empty dictionary to store the new version of coordinate_shots
    coordinate_shots = {}

    # Iterate over the shot dictionaries
    for game_id, shots in games_trimmed.items():
        for shot_num, shot in shots.items():
            # Check if the shot has 'x' and 'y' values in its 'coordinates' key
            if 'x' in shot['coordinates'] and 'y' in shot['coordinates']:
                # Extract the x and y coordinates from the shot dictionary
                x = shot['coordinates']['x']
                y = shot['coordinates']['y']

                # Check if there is an entry in coordinate_shots for the given coordinates
                if (x, y) not in coordinate_shots:
                    # If there is no entry for the given coordinates, create a new entry in coordinate_shots
                    coordinate_shots[(x, y)] = []

                # Add the location (game ID and shot number) for the current shot to the entry in coordinate_shots for the given coordinates
                coordinate_shots[(x, y)].append((game_id, shot_num))
    return coordinate_shots


def build_game_shifts(yearStart, yearEnd):
    # Define the global game_shifts variable
    global game_shifts
    # Initialize an empty dictionary to store data for each game
    game_shifts = {}
    # Loop over the years in the specified range
    for i in range(yearStart, yearEnd):
        # Loop over the games in the relevant year
        for j in range(1, year_match(i)):
            # Calculate NHL GameID
            gameID = i * 1000000 + 20000 + j
            # Create an empty DataFrame for the current game
            game_shifts[gameID] = pd.DataFrame()
            # Add empty columns for player information and shift data
            for k in ['player_id','player_first','player_last','shifts_1','shifts_2','shifts_3']:
                game_shifts[gameID][k] = ''
            # Loop over the shift data for the current game
            for k in shifts[gameID]['data']:
                # Check if the shift is from a period 1, 2, or 3, and if it
                # was played by a non-null player
                if k['period'] <= 3 and k['playerId'] != None:
                    if k['playerId'] in list(game_shifts[gameID]['player_id']):
                        # Find the index of the row where the player_id matches k['playerId']
                        player_index = game_shifts[gameID].index[game_shifts[gameID]['player_id'] == k['playerId']].tolist()[0]
                        # Select the row at the player_index
                        player_row = game_shifts[gameID].iloc[[player_index]]
                        # Select the 'shifts_'+str(k['period']) column from the player_row
                        shift_column = player_row['shifts_'+str(k['period'])]
                        # Append the start and end times to the shift_column
                        shift_column[player_index].append((k['startTime'],k['endTime']))
                    else:
                        game_shifts[gameID].loc[len(game_shifts[gameID])] = [k['playerId'], k['firstName'], k['lastName'], [], [], []]
                        # Find the index of the row where the player_id matches k['playerId']
                        player_index = game_shifts[gameID].index[game_shifts[gameID]['player_id'] == k['playerId']].tolist()[0]
                        # Select the row at the player_index
                        player_row = game_shifts[gameID].iloc[[player_index]]
                        # Select the 'shifts_'+str(k['period']) column from the player_row
                        shift_column = player_row['shifts_'+str(k['period'])]
                        # Append the start and end times to the shift_column
                        shift_column[player_index].append((k['startTime'],k['endTime']))
                else:
                    pass

def get_single_player_teams(player_id):
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    # Initialize an empty dictionary to store the teams a player has played for in each year
    teams_playerID = {}

    # Iterate over the shot dictionaries in the games_trimmed dictionary
    for gameID, game_dict in games_trimmed.items():
        for shot in game_dict.values():
            # Retrieve the player_id, year, and triCode for the current shot
            shot_player_id = shot['players'][0]['player']['id']
            year = get_game_year(gameID)
            triCode = shot['team']['triCode']

            # Check if the player_id matches the input player_id
            if shot_player_id == player_id:
                # Check if the year already exists as a key in the teams_playerID dictionary
                if year not in teams_playerID:
                    # If the year does not exist as a key, initialize an empty list for that year as the value of the key
                    teams_playerID[year] = []

                # Append the triCode to the list of teams for that year in the teams_playerID dictionary
                if triCode not in teams_playerID[year]:
                    teams_playerID[year].append(triCode)

    # Return the teams_playerID dictionary
    return teams_playerID


def get_single_player_games(player_id):
    if player_teams == None:
        games_playerID = {}
        games_playerID[player_id] = get_single_player_teams(player_id)
    else:
        games_playerID = {}
        games_playerID[player_id] = player_teams[player_id]
    if team_games == None:
        global team_games
        team_games = build_team_games()
    for year, triCodes in player_teams[player_id].items():
        # Iterate over the triCodes in the list of triCodes for that year
        for triCode in triCodes:
            # Check if the year already exists as a key in the player_id_games dictionary for the current player_id
            if year not in games_playerID:
                # If the year does not exist as a key, initialize an empty list for that year as the value of the key
                games_playerID[year] = []

            # Append the gameIDs for the triCode to the list of games for that year in the player_id_games dictionary for the current player_id
            games_playerID[year] += team_games[triCode][year]
    return games_playerID


def build_player_teams():
    if player_id_list == None:
            global player_id_list
            player_id_list = build_player_id_list()
    player_teams = {}
    for player in player_id_list:
            player_teams[player] = get_single_player_teams(player)
    return player_teams


def build_player_id_games():
    if player_teams == None:
        global player_teams
        player_teams = build_player_teams()
    if team_games=None:
        global team_games
        team_games = build_team_games()

    # Initialize an empty dictionary to store the games a player has played in each year
    player_id_games = {}

    # Iterate over the keys in the player_teams dictionary
    for player_id, teams in player_teams.items():
        # Initialize an empty dictionary for the current player_id
        player_id_games[player_id] = get_single_player_games(player_id)

    # Return the player_id_games dictionary
    return player_id_games


def build_player_id_set():
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    player_id_set = set()
    for gameID, shots in games_trimmed.items():
        for shot_num, shot in shots.items():
            player_id_set.add(shot['players'][0]['player']['id'])
    return player_id_set


def build_team_set():
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    triCodes = set()
    for gameID, game_dict in games_trimmed.items():
        for shot in game_dict.values():
            triCodes.add(shot['team']['triCode'])
    return triCodes


def build_team_games():
    if team_set == None:
        team_set = build_team_set()
    team_games = {}
    for team in team_set:
        team_games[triCode] = get_single_team_games(triCode)
    return team_games


def get_single_team_games(triCode):
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    # Initialize an empty dictionary to store the teams a player has played for in each year
    games_teamID = {}

    # Iterate over the shot dictionaries in the games_trimmed dictionary
    for gameID, game_dict in games_trimmed.items():
        for shot in game_dict.values():
            # Retrieve the player_id, year, and triCode for the current shot
            year = get_game_year(gameID)
            game_triCode = shot['team']['triCode']

            # Check if the player_id matches the input player_id
            if game_triCode == triCode:
                # Check if the year already exists as a key in the teams_playerID dictionary
                if year not in games_teamID:
                    # If the year does not exist as a key, initialize an empty list for that year as the value of the key
                    games_teamID[year] = []

                # Append the triCode to the list of teams for that year in the teams_playerID dictionary
                if gameID not in games_teamID[year]:
                    games_teamID[year].append(gameID)

    # Return the teams_playerID dictionary
    return games_teamID


def build_games_trimmed(directory='.'):
    # Get a list of all .json files in the specified directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    games_trimmed = {}
    # Loop through the .json files in the directory
    for file_name in json_files:
        # Construct the file path for the current .json file
        file_path = os.path.join(directory, file_name)
        # Open the .json file and load the data into a dictionary
        with open(file_path, encoding='utf-8') as json_file:
            game_data = json.load(json_file)
        # Initialize an empty dictionary to store information about the current game
        game_dict = {}
        game_id = game_data.get('gamePk', None)
        if game_id == None:
            continue
        # Initialize counter variables for the play index and the period number
        k = 0
        n = 0
        away = game_data['gameData']['teams']['away']['triCode']
        # Loop through the plays in the game
        for m in range(1, len(game_data['liveData']['plays']['allPlays'])):
            # Check if the current play is a period end event
            play = game_data['liveData']['plays']['allPlays'][m]
            if play['result']['event'] == "Period End":
                # If it is, increment the period number
                n = n+1
            # If there have been 4 period end events, break out of the loop
            if n >= 3:
                n = 0
                break
            # Check if the current play is a shot or a goal
            if play['result']['event'] in ["Shot", "Goal"]:
                # If a shot does not have coordinate data, ignore the play and continue on with the loop.
                if 'x' not in play['coordinates'] or 'y' not in play['coordinates']:
                    continue
                # If a goal was scored on an empty net, ignore the play and continue on with the loop.
                if play['result'].get('emptyNet', False) == True:
                    continue
                # Retrieve the shooting team code and the period number from the play dictionary
                shooting_team = play['team']['triCode']
                period = play['about']['period']
                # Check if the shooting team is the away team or the period is even (while we don't consider overtime,
                # this would correct shots if this code were to be adjusted to include overtime shots.)
                # If either condition is true, but not both, multiply the x value of the coordinates by -1
                if ((away == play['team']['triCode']) ^ (n % 2 == 0)):
                    play['coordinates']['x'] *= -1
                # Add the play dictionary to the game dictionary
                game_dict[k] = play
                # Increment the play index counter
                k = k+1
        xlist = getGameExes(game_dict)
        if np.mean(xlist) <= 0:
            switchGameExes(game_dict)
        # Add the game dictionary to the games_trimmed global variable, using the game ID as the key
        games_trimmed[game_id] = game_dict
    return games_trimmed


def getGameExes(gameDict):
    gameExes = []
    for i in range(1, len(gameDict)):
        gameExes.append(gameDict[i]['coordinates']['x'])
    return gameExes


def switchGameExes(gameDict):
    for i in range(1, len(gameDict)):
        gameDict[i]['coordinates']['x'] *= -1


def avg_spline(spline1, spline2, weight1=None, weight2=None):
    # Assume that bisplrep_test and bisplrep_8470600[8470600] are lists with five elements each
    # as described above
    tx_1, ty_1, c_1, kx, ky = spline1[0], spline1[1], spline1[2], spline1[3], spline1[4]
    tx_2, ty_2, c_2 = spline2[0], spline2[1], spline2[2]

    if weight1 is not None and weight2 is not None:
        weight_total = weight_test + weight_player
        # Average the knots, coefficients, and degree
        tx_avg = ((tx_1*weight1)/weight_total + (tx_2*weight2)/weight_total) / 2
        ty_avg = ((ty_1*weight1)/weight_total + (ty_2*weight2)/weight_total) / 2
        c_avg = ((c_1*weight1)/weight_total + (c_2*weight2)/weight_total) / 2
    else:
        # Average the knots, coefficients, and degree
        tx_avg = (tx_1 + tx_2) / 2
        ty_avg = (ty_1 + ty_2) / 2
        c_avg = (c_1 + c_2) / 2

    # Create the average spline by combining the averaged knots, coefficients, and degree
    average_spline = [tx_avg, ty_avg, c_avg, kx, ky]
    return average_spline