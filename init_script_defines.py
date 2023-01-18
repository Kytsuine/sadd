#!/usr/bin/env python


import json
import time
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np


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


def get_players_on_ice(gameID, period, periodTime, game_shifts=None, directory='.'):
    if game_shifts == None:
        game_shifts = build_game_shifts(directory=directory) # Change those numbers to your relevant years! Working on a way to do that automagically...

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


def get_player_shots(player_id, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("get_player_shots()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

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


def get_shots_by_player(player_id, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("get_shots_by_player()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

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


def get_player_shots_against(player_id, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("get_player_shots_against()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)


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


def get_goal_shot_ratio(player_id, player_shots=None, count=False, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("get_goal_shot_ratio()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)


    # If player_shots is not provided, retrieve them using the get_player_shots function
    if player_shots is None:
        player_shots = get_player_shots(player_id, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)

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


def get_coordinate_goal_shot_ratio_against(player_id, coordinate, games_trimmed=None, coordinate_shots=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("get_coordinate_goal_shot_ratio_against()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

    # Retrieve the player_shots using the get_player_shots function
    player_shots = get_player_shots_against(player_id,  games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)

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



def get_coordinate_goal_shot_ratio(x, y, count=False, games_trimmed=None, coordinate_shots=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("get_coordinate_goal_shot_ratio()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

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


def get_coordinate_goal_shot_ratio_against(player_id, x, y, games_trimmed=None, coordinate_shots=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, player_shots=None):
    print("get_coordinate_goal_shot_ratio_against()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

    # If player_shots is not provided, retrieve the player_shots using the get_shots_by_player function
    if player_shots is None:
        player_shots = get_player_shots_against(player_id, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)

    # Convert the coordinate_shots and player_shots lists to sets and compute their intersection
    coordinate_player_shots = set(coordinate_shots[(x, y)]) & set(player_shots)

    # Use the get_goal_shot_ratio function to calculate the proportion of goals to shots for the coordinate_player_shots list
    proportion_of_goals = get_goal_shot_ratio(player_id, player_shots=player_shots, count=1, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)

    # Return the proportion_of_goals
    return proportion_of_goals


def get_coordinate_goal_shot_ratio_for_player(player_id, x, y, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, player_shots=None, coordinate_shots=None):
    print("get_coordinate_goal_shot_ratio_for_player()", end="\r")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None

    # If player_shots is not provided, retrieve the player_shots using the get_shots_by_player function
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)
    if player_shots is None:
        player_shots = get_shots_by_player(player_id, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)

    # Convert the coordinate_shots and player_shots lists to sets and compute their intersection
    coordinate_player_shots = set(coordinate_shots[(x, y)]) & set(player_shots)

    # Use the get_goal_shot_ratio function to calculate the proportion of goals to shots for the coordinate_player_shots list
    proportion_of_goals = get_goal_shot_ratio(player_id, player_shots=None, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, count=1)

    # Return the proportion_of_goals
    return proportion_of_goals


def build_player_coordinate_list(player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    print("build_player_coordinate_list()")
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

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
    print("build_home_away_teams()")
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


def build_coordinate_shots(games_trimmed=None):
    print("build_coordinate_shots()")
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


def build_game_shifts(directory='.', home_away_teams=None):
    print("build_game_shifts()")
    if home_away_teams == None:
        print("Please build home_away_teams with the build_home_away_teams() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    # Initialize an empty dictionary to store data for each game
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    game_shifts = {}
    progress = 0
    length = 80
    jflength = len(json_files)
    # Iterate over the files in the directory
    for file in json_files:
        # Extract the gameID from the file name
        gameID = int(file.split('_')[1].split('.')[0])
        progress += 1
        print("[", "="*((progress*length)//jflength), " "*(length-((progress*length)//jflength)), "] Current gamefile:", file_name, end="\r", flush=True)
        # Create an empty DataFrame for the current game
        game_shifts[gameID] = {}
        game_shifts[gameID][home] = {}
        game_shifts[gameID][away] = {}
        game_shifts[gameID][home][triCode] = home_away_teams[gameID][0]
        game_shifts[gameID][away][triCode] = home_away_teams[gameID][1]
        game_shifts[gameID][home][players] = {}
        game_shifts[gameID][away][players] = {}
        # Read in the data from the .json file
        with open(os.path.join(directory, file), 'r') as f:
            data = json.loads(f.read())
        # Loop over the data list and add each shift to the DataFrame
        for k in data:
            # Check if the shift is from a period 1, 2, or 3, and if it
            # was played by a non-null player
            if type(data[k]) != list:
                continue
            for i in range(0, len(data[k])-1):
                if data[k][i]['period'] <= 3 and data[k][i]['playerId'] != None:
                    playerID = data[k][i]['playerId']
                    if data[k][i]['teamAbbrev'] = game_shifts[gameID][home][triCode]:
                        if playerID in game_shifts[gameID][home][players]:
                            player_dict = game_shifts[gameID][home][players][playerID]
                        else:
                            game_shifts[gameID][home][players][playerID] = {}
                            player_dict = game_shifts[gameID][home][players][playerID]
                            player_dict[playerName] = str(data[k][i][firstName] + " " + data[k][i][lastName])
                            player_dict[period1] = set()
                            player_dict[period2] = set()
                            player_dict[period3] = set()
                    else:
                        if playerID in game_shifts[gameID][away][players]:
                            player_dict = game_shifts[gameID][away][players][playerID]
                        else:
                            game_shifts[gameID][away][players][playerID] = {}
                            player_dict = game_shifts[gameID][away][players][playerID]
                            player_dict[playerName] = str(data[k][i][firstName] + " " + data[k][i][lastName])
                            player_dict[period1] = set()
                            player_dict[period2] = set()
                            player_dict[period3] = set()
                    shift_period = data[k][i]['period']
                    if shift_period == 1:
                        player_dict[period1].add((data[k][i]['startTime'], data[k][i]['endTime']))
                    elif shift_period == 2:
                        player_dict[period2].add((data[k][i]['startTime'], data[k][i]['endTime']))
                    else:
                        player_dict[period3].add((data[k][i]['startTime'], data[k][i]['endTime']))
                        shift_column[player_index].append((data[k][i]['startTime'],data[k][i]['endTime']))
                else:
                    pass
    return game_shifts

def get_single_player_teams(player_id, games_trimmed=None):
    print("get_single_player_teams()", end="\r")
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


def get_single_player_games(player_id, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None):
    print("get_single_player_games()", end="\r")
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    games_playerID = {}
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
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


def build_player_teams(games_trimmed=None, player_id_set=None):
    print("build_player_teams()")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    player_teams = {}
    for player in player_id_set:
        player_teams[player] = get_single_player_teams(player, games_trimmed=games_trimmed)
    return player_teams


def build_player_id_games(games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None):
    print("build_player_id_games()")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)

    # Initialize an empty dictionary to store the games a player has played in each year
    player_id_games = {}

    # Iterate over the keys in the player_teams dictionary
    for player_id, teams in player_teams.items():
        # Initialize an empty dictionary for the current player_id
        player_id_games[player_id] = get_single_player_games(player_id, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games)

    # Return the player_id_games dictionary
    return player_id_games


def build_player_id_set(games_trimmed=None):
    print("build_player_id_set()")
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    player_id_set = set()
    for gameID, shots in games_trimmed.items():
        for shot_num, shot in shots.items():
            player_id_set.add(shot['players'][0]['player']['id'])
    return player_id_set


def build_team_set(games_trimmed=None):
    print("build_team_set()")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    triCodes = set()
    for gameID, game_dict in games_trimmed.items():
        for shot in game_dict.values():
            triCodes.add(shot['team']['triCode'])
    return triCodes


def build_team_games(games_trimmed=None, team_set=None):
    print("build_team_games()")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    if team_set == None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    team_games = {}
    for team in team_set:
        team_games[team] = get_single_team_games(team, games_trimmed=games_trimmed)
    return team_games


def get_single_team_games(triCode, games_trimmed=None):
    print("get_single_team_games()", end="\r", flush=True)
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    # Initialize an empty dictionary to store the teams a player has played for in each year
    games_teamID = {}
    progress = 0
    length = 80
    gtlength = len(games_trimmed)
    # Iterate over the shot dictionaries in the games_trimmed dictionary
    for gameID, game_dict in games_trimmed.items():
        progress += 1
        print("[", "="*((progress*length)//gtlength), " "*(length-((progress*length)//gtlength)), "] Current game:", gameID, end="\r", flush=True)
        for shot in game_dict.values():
            # Retrieve the player_id, year, and triCode for the current shot
            game_triCode = shot['team']['triCode']

            # Check if the player_id matches the input player_id
            if game_triCode == triCode:
                year = get_game_year(gameID)
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
    print("build_games_trimmed()", flush=True)
    # Get a list of all .json files in the specified directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    games_trimmed = {}
    progress = 0
    length = 80
    jflength = len(json_files)
    # Loop through the .json files in the directory
    for file_name in json_files:
        progress += 1
        print("[", "="*((progress*length)//jflength), " "*(length-((progress*length)//jflength)), "] Current gamefile:", file_name, end="\r", flush=True)
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


def build_grouped_data(games_trimmed=None, coordinate_shots=None):
    # Initialize the new dictionary
    grouped_data = {}
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    # Loop through the data points in the original dictionary
    for (x, y) in coordinate_shots.keys():
      # Use integer division to map the x and y values to the coarser grid
      x_group = x // 5
      y_group = y // 3
      
      # Use a tuple of the x and y group as the key in the new dictionary
      key = (x_group, y_group)
      
      # If the key doesn't exist in the dictionary yet, initialize it with an empty list
      if key not in grouped_data:
        grouped_data[key] = []
      
      # Append the data point to the list for this grid cell
      grouped_data[key].extend(coordinate_shots[(x,y)])
    return grouped_data


def get_player_avg_pct_counts_and_groups(playerID, games_trimmed=None, coordinate_shots=None, grouped_data=None):
    print("get_player_avg_pct_counts_and_groups()", end="\r", flush=True)
    if grouped_data is None:
        grouped_data = build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    player_shots = get_shots_by_player(playerID)
    weighted_shots = grouped_data
    group_dict = {}
    total_ratio = 0
    total_weight = 0
    progress = 0
    length = 60
    for gameID, shot in player_shots:
        x, y = get_shot_grouped_coordinates(gameID, shot, games_trimmed=games_trimmed)
        for _ in range(1, 850):
            weighted_shots[(x, y)].append((gameID, shot))
    wslength = len(weighted_shots)
    for (x, y) in weighted_shots:
        progress += 1
        print("[", "="*((progress*length)//wslength), " "*(length-((progress*length)//wslength)), "] - Current coordinate:", x, y, "Current player:", playerID, end="\r", flush=True)
        group_ratio = get_goal_shot_ratio(playerID, player_shots=weighted_shots[(x, y)], count=1)
        total_ratio += group_ratio[0] * len(weighted_shots[(x, y)])
        total_weight += len(weighted_shots[(x, y)])
        group_dict[(x, y)] = group_ratio
    return (total_ratio / total_weight, group_dict)



def get_player_avg_pct_and_groups(playerID, games_trimmed=None, coordinate_shots=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, grouped_data=None, player_shots=None):
    print("get_player_avg_pct_and_groups()", end="\r", flush=True)
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if grouped_data is None:
        grouped_data = build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    # If player_shots is not provided, retrieve the player_shots using the get_shots_by_player function
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)
    if player_shots is None:
        player_shots = get_shots_by_player(playerID, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)
    weighted_shots = grouped_data
    group_dict = {}
    total_ratio = 0
    total_weight = 0
    for gameID, shot in player_shots:
        x, y = get_shot_grouped_coordinates(gameID, shot, games_trimmed=games_trimmed)
        for _ in range(1, 850):
            weighted_shots[(x, y)].append((gameID, shot))
    for (x, y) in weighted_shots:
        group_ratio = get_goal_shot_ratio(playerID, player_shots=weighted_shots[(x, y)], count=False, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)
        total_ratio += group_ratio * len(weighted_shots[(x, y)])
        total_weight += len(weighted_shots[(x, y)])
        group_dict[(x, y)] = group_ratio
    return (total_ratio / total_weight, group_dict)


def get_shot_coordinates(gameID, shotID, games_trimmed=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    return (games_trimmed[gameID][shotID]['coordinates']['x'], games_trimmed[gameID][shotID]['coordinates']['y'])


def get_shot_grouped_coordinates(gameID, shotID, games_trimmed=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    return (games_trimmed[gameID][shotID]['coordinates']['x']//5, games_trimmed[gameID][shotID]['coordinates']['y']//3)


def build_player_pcts_and_groups(games_trimmed=None, player_id_set = None, player_teams=None, team_set=None, team_games=None, player_id_games=None, coordinate_shots=None, grouped_data=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if grouped_data is None:
        grouped_data=build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    player_pcts = {}
    length = 80
    progress = 0
    psetlength = len(player_id_set)
    print("build_player_pcts_and_groups(): Building dictionary for players")
    for player in player_id_set:
        progress += 1
        print("[", "="*((progress*length)//psetlength), " "*(length-((progress*length)//psetlength)), "] - Current player:", player, end="\r")
        player_pcts[player] = get_player_avg_pct_and_groups(player, games_trimmed=games_trimmed, coordinate_shots=coordinate_shots, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games, grouped_data=grouped_data)
    return player_pcts


def get_shot_shooter(gameID, shotID, games_trimmed=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    return games_trimmed[gameID][shotID]['players'][0]['player']['id']


def get_shot_pct(gameID, shotID, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, coordinate_shots=None, grouped_data=None, player_pcts_and_groups=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if grouped_data is None:
        grouped_data=build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    if player_pcts_and_groups is None:
        player_pcts_and_groups=build_player_pcts_and_groups(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games, coordinate_shots=coordinate_shots, grouped_data=grouped_data)
    shooter = get_shot_shooter(gameID, shotID, games_trimmed=games_trimmed)
    x, y = get_shot_grouped_coordinates(gameID, shotID, games_trimmed=games_trimmed)
    return player_pcts_and_groups[shooter][1][(x, y)]


def get_shooter_pct(gameID, shotID, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, coordinate_shots=None, grouped_data=None, player_pcts_and_groups=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if grouped_data is None:
        grouped_data=build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    if player_pcts_and_groups is None:
        player_pcts_and_groups=build_player_pcts_and_groups(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games, coordinate_shots=coordinate_shots, grouped_data=grouped_data)
    shooter = get_shot_shooter(gameID, shotID, games_trimmed=games_trimmed)
    return player_pcts_and_groups[shooter][0]


def get_shot_time(gameID, shotID, games_trimmed=None):
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    return (games_trimmed[gameID][shotID]['about']['period'], games_trimmed[gameID][shotID]['about']['periodTime'])


def build_sadd(games_trimmed=None, directory='.', game_shifts=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, coordinate_shots=None, grouped_data=None, player_pcts_and_groups=None):
    print("build_sadd(): Checking definitions of initial dictionaries", flush=True)
    if games_trimmed is None:
        print("Caution! Assuming game data is stored in the games subdirectory of the current working directory.\nIf this is not accurate, please call build_games_trimmed() with the correct diretory.")
        games_trimmed = build_games_trimmed('./games/')
    if game_shifts is None:
        game_shifts=build_game_shifts(directory=directory)
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    if team_games is None:
        team_games = build_team_games(games_trimmed=games_trimmed, team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)
    if coordinate_shots is None:
        coordinate_shots = build_coordinate_shots(games_trimmed=games_trimmed)
    if grouped_data is None:
        grouped_data=build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    if player_pcts_and_groups is None:
        player_pcts_and_groups=build_player_pcts_and_groups(games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games, coordinate_shots=coordinate_shots, grouped_data=grouped_data)
    sadd = {}
    progress = 0
    gtlength = len(games_trimmed)
    length = 80
    print("build_sadd(): Building SADD initial dictionary", end="\r", flush=True)
    for player in player_id_set:
        sadd[player] = {}
        sadd[player]['pct_diff_total'] = 0
        sadd[player]['sadd_events'] = 0
        sadd[player]['sadd'] = 0
    print("build_sadd(): Building SADD dictionary for games.", flush=True)
    for gameID, gameDict in games_trimmed.items():
        progress += 1
        print("[", "="*((progress*length)//gtlength), " "*(length-((progress*length)//gtlength)), "] - Current game:", gameID, end="\r")
        for shotID in gameDict.keys():
            period, time = get_shot_time(gameID, shotID, games_trimmed=games_trimmed)
            playerList = get_players_on_ice(gameID, period, time, game_shifts=game_shifts)
            shooter = get_shot_shooter(gameID, shotID, games_trimmed=games_trimmed)
            shotYear = get_game_year(gameID)
            defenseSet = get_opposing_players(shooter, playerList, shotYear, player_teams=player_teams, games_trimmed=games_trimmed, player_id_set=player_id_set)
            shotPct = get_shot_pct(gameID, shotID, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games, coordinate_shots=coordinate_shots, grouped_data=grouped_data, player_pcts_and_groups=player_pcts_and_groups)
            shooterPct = get_shooter_pct(gameID, shotID, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games, coordinate_shots=coordinate_shots, grouped_data=grouped_data, player_pcts_and_groups=player_pcts_and_groups)
            for player in defenseSet:
                if player not in sadd:
                    sadd[player] = {}
                    sadd[player]['pct_diff_total'] = 0
                    sadd[player]['sadd_events'] = 0
                    sadd[player]['sadd'] = 0
                sadd[player]['pct_diff_total'] += (shooterPct - shotPct)
                sadd[player]['sadd_events'] += 1
                sadd[player]['sadd'] = sadd[player]['pct_diff_total']/sadd[player]['sadd_events']
    return sadd

def get_opposing_players(player, playerList, year, player_teams=None, games_trimmed=None, player_id_set=None):
    if games_trimmed is None:
        print("Caution! Assuming game data is stored in the games subdirectory of the current working directory.\nIf this is not accurate, please call build_games_trimmed() with the correct diretory.")
        games_trimmed = build_games_trimmed('./games/')
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams=build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    defenseSet = set()
    teams = set(player_teams[player][year])
    for item in playerList:
        if item not in player_teams:
            continue
        if year not in player_teams[item]:
            continue
        if len(set(player_teams[item][year]).intersection(teams)) == 0:
            defenseSet.add(item)
    return defenseSet




# You can use these to build dictionaries!

#games_trimmed = build_games_trimmed('../Capstone/api/games')
#player_id_set = build_player_id_set()
#coordinate_shots = build_coordinate_shots()
#grouped_data = build_grouped_data()
#player_teams = build_player_teams()
#team_set = build_team_set()
#team_games = build_team_games()
#player_id_games = build_player_id_games()
#game_shifts = build_game_shifts('../Capstone/api/shifts')
#player_pcts_and_groups = build_player_pcts_and_groups()
