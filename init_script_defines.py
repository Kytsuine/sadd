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

def get_home_on_ice(gameID, period, periodTime, game_shifts=None, directory='.'):
    """
    This function takes in a gameID, period, and periodTime, and returns a list of player IDs for players who were on the ice for the home team during that period and time.
    If game_shifts is not passed as an argument, it will be built using the game data found in the directory provided.
    If the period is not within the range of 1-3, the function will return None.
    
    Example usage:
    home_players = get_home_on_ice(2017020001, 1, 1234, directory='/data')
    """
    # Check that the period is within the range of 1-3. If not, return a null value.
    if period not in range(1,4):
        return None

    if game_shifts == None:
        game_shifts = build_game_shifts(directory=directory) # Make sure to pass the right directory if you don't pass game_shifts. 
    
    # Retrieve the game dataframe corresponding to the gameID
    game_dict = game_shifts[gameID]['home']

    # Identify the period of the shot to find the corresponding shifts_n column
    period_dict = "period" + str(period)

    # Initialize an empty list to store the player_ids for players on the ice
    player_ids = []

    # Loop through each row in the game dataframe
    for player in game_dict:
        # Retrieve the shift tuples for the current player
        shift_tuples = player[period_dict]

        # Check which players had a shift time tuple that includes periodTime
        for shift_tuple in shift_tuples:
            if shift_tuple[0] < periodTime <= shift_tuple[1]:
                player_ids.append(row['player_id'])
    return player_ids


def get_away_on_ice(gameID, period, periodTime, game_shifts=None, directory='.'):
    """
    Given a game ID, period, and period time, this function returns a list of player IDs for the away team who were on the ice at that time. 
    If game_shifts is not passed, it will use the build_game_shifts function to build it using the directory parameter.

    Parameters:
    gameID (int): the game ID to retrieve the player IDs for
    period (int): the period of the game to retrieve the player IDs for, must be between 1 and 3
    periodTime (int): the time of the period to retrieve the player IDs for
    game_shifts (dict): a dictionary of game shift data, if not passed it will be built using the directory parameter
    directory (str): the directory where the game shift data is located, defaults to the current directory

    Returns:
    list: a list of player IDs for the away team who were on the ice at the given period time. 
    None: if the input period is not between 1 and 3

    Example:
    game_shifts = build_game_shifts()
    away_players_on_ice = get_away_on_ice(2012030221, 2, 599, game_shifts)
    """
    # Check that the period is within the range of 1-3. If not, return a null value.
    if period not in range(1,4):
        return None

    if game_shifts == None:
        game_shifts = build_game_shifts(directory=directory) # Make sure to pass the right directory if you don't pass game_shifts. 
    
    # Retrieve the game dataframe corresponding to the gameID
    game_dict = game_shifts[gameID]['away']

    # Identify the period of the shot to find the corresponding shifts_n column
    period_dict = "period" + str(period)

    # Initialize an empty list to store the player_ids for players on the ice
    player_ids = []

    # Loop through each player in the game dataframe
    for player in game_dict:  
        # Retrieve the shift tuples for the current player
        shift_tuples = player[period_dict]

        # Check which players had a shift time tuple that includes periodTime
        for shift_tuple in shift_tuples:
            if shift_tuple[0] < periodTime <= shift_tuple[1]:
                player_ids.append(row['player_id'])

    return player_ids


def get_players_on_ice(gameID, period, periodTime, game_shifts=None, directory='.'):
    """
    This function retrieves the player_ids of the players that were on the ice during a specific period and time of a game.
    The function first calls get_home_on_ice() and get_away_on_ice() to get the player_ids for the home and away teams respectively.
    These lists are then concatenated and returned.
    :param gameID: The id of the game.
    :param period: The period of the game.
    :param periodTime: The time in seconds into the period.
    :param game_shifts: The game shift data. 
    :param directory: The directory where the game shift data is stored.
    :return: A list of player_ids that were on the ice during the specified period and time. 
    """
    player_ids = []
    player_ids.extend(get_home_on_ice(gameID, period, periodTime, game_shifts=game_shifts, directory=directory))
    player_ids.extend(get_away_on_ice(gameID, period, periodTime, game_shifts=game_shifts, directory=directory))
    return player_ids

# Example usage:
# players_on_ice = get_players_on_ice(gameID=2017020220, period=2, periodTime=6:00, directory='/path/to/directory')
# print(players_on_ice)
# Output: [5,6,7,8,9,10,11,12,13,14,15,16]


def get_player_shots(player_id, games_trimmed=None, game_shifts=None, directory='.'):
	"""
	Returns a list of tuples of the form (gameID, shot_num) of the shots taken by a player when they were on the ice.
	player_id : int
		The player's unique ID.
	games_trimmed : dict
		A dictionary of all game events. If not provided, will be built by calling the function build_games_trimmed().
	game_shifts : dict
		A dictionary of all player shifts for a game. If not provided, will be built by calling the function build_game_shifts().
	directory : str
		The directory where the game .json files are saved. Only necessary if games_trimmed or game_shifts are not provided.
	"""
	if games_trimmed is None:
		games_trimmed = build_games_trimmed(directory)
	if game_shifts is None:
		game_shifts = build_game_shifts(directory)

	# Initialize an empty list to store the shots taken when the player was on the ice.
	player_shots = []

	# Iterate over the keys in the games_trimmed dictionary
	for gameID, game_dict in games_trimmed.items():
		# Iterate over the shots in the game
		for shot_num, shot in game_dict.items():
		    periodTime = shot['about']['periodTime']
		    period = shot['about']['period']

		    # Check if the player was on the ice at the time of the shot
		    players_on_ice = get_players_on_ice(gameID, period, periodTime, game_shifts=game_shifts)
		    if players_on_ice is not None and player_id in players_on_ice:
		        # Append a tuple (game_ID, shot_num) to the list of player shots
		        player_shots.append((gameID, shot_num))

	return player_shots



def get_shots_by_player(player_id, games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None):
    """
    This function retrieves all the shots taken by a player from a given set of game data.
    Inputs:
        player_id: integer, unique identifier for a player
        games_trimmed: dictionary, containing game information
        player_id_set: set, containing player_ids
        player_teams: dictionary, containing player_id as key and team_name as value
        team_set: set, containing team_name
        team_games: dictionary, containing team_name as key and game_id as value
        player_id_games: dictionary, containing player_id as key and games as value
    Outputs:
        player_shots: list, containing tuples of (game_id, shot_num)
    """
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
    """
    This function takes in a player_id and returns a list of shots taken against that player when they were on the ice.
    The games_trimmed, player_id_set, player_teams, team_set, team_games, and player_id_games parameters are used to optimize performance by avoiding redundant computations.
    If any of these parameters are not provided, they will be generated using the corresponding build_*() function.
    
    Parameters:
    player_id (int): The ID of the player for which to retrieve shots against
    games_trimmed (dict, optional): A dictionary of games with the format {game_id: {shot_num: {shot_data}}}
    player_id_set (set, optional): A set of player IDs
    player_teams (dict, optional): A dictionary of player teams with the format {player_id: {year: [team_codes]}}
    team_set (set, optional): A set of team codes
    team_games (dict, optional): A dictionary of team games with the format {team_code: {year: [game_ids]}}
    player_id_games (dict, optional): A dictionary of player games with the format {player_id: {year: [game_ids]}}
    
    Returns:
    List of shots taken against player_id in the format [ (game_id, shot_num), ... ] 
    """
    
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
    """
    This function calculates the ratio of goals to shots for a given player.
    It also has the option to return the count of shots taken by the player.
    
    player_id: ID of the player for which the ratio is to be calculated
    player_shots: List of shot dictionaries for the player (default None)
    count: A boolean that indicates if the number of shots taken by the player should be returned (default False)
    games_trimmed: A dictionary containing the game data (default None)
    player_id_set: A set of player IDs (default None)
    player_teams: A dictionary that maps player IDs to teams (default None)
    team_set: A set of team names (default None)
    team_games: A dictionary that maps team names to the games they played (default None)
    player_id_games: A dictionary that maps player IDs to the games they played (default None)
    """
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
    """
    This function calculates the proportion of goals scored to shots taken against a defensive player at a specific coordinate on the ice.
    """
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

    # Retrieve the player_shots using the get_player_shots_against function
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
    """
    Given the x and y coordinates of a shot location on the ice, this function calculates the proportion of goals to shots taken from that location.
    Optionally, it also returns the total number of shots taken from that location.
    
    Parameters:
    x (int): The x-coordinate of the shot location on the ice.
    y (int): The y-coordinate of the shot location on the ice.
    count (bool): If True, returns a tuple containing the proportion of goals to shots and the total number of shots taken from that location.
                  If False, returns only the proportion of goals to shots. (default: False)
    games_trimmed (dict): A dictionary containing the game data, with games indexed by game ID and shots indexed by shot number.
                          If None, the function will try to build it using the `build_games_trimmed()` function.
    coordinate_shots (dict): A dictionary containing the locations (game IDs and shot numbers) where shots were taken from a given x, y coordinate on the ice.
                             If None, the function will try to build it using the `build_coordinate_shots()` function.
    player_id_set (set): A set of player IDs that appeared in the games_trimmed.
                         If None, the function will try to build it using the `build_player_id_set()` function.
    player_teams (dict): A dictionary mapping player IDs to teams.
                         If None, the function will try to build it using the `build_player_teams()` function.
    team_set (set): A set of team names that appeared in the games_trimmed.
                     If None, the function will try to build it using the `build_team_set()` function.
    team_games (dict): A dictionary mapping team names to a list of game IDs in which the team played.
                       If None, the function will try to build it using the `build_team_games()` function.
    player_id_games (dict): A dictionary mapping player IDs to a list of game IDs in which the player appeared.
                            If None, the function will try to build it using the `build_player_id_games()` function.
    
    Returns:
    tuple or float: If `count` is True, returns a tuple containing the proportion of goals to shots and the total number of shots taken from that location.
                    If `count` is False, returns only the proportion of goals to shots.
                    If the x, y coordinate is not found in the coordinate_shots dictionary, returns None.
	"""
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
	"""
	Given a player ID, x and y coordinates, and optional pre-built data, this function calculates the proportion of shots taken by the player at the specified coordinates that resulted in goals.
	Parameters:
	- player_id (int): The player ID for which the proportion of goals to shots is calculated
	- x (int): The x-coordinate of the shot location
	- y (int): The y-coordinate of the shot location
	- games_trimmed (list, optional): A list of game events, as returned by the build_games_trimmed() function. If not provided, the function will call build_games_trimmed()
	- coordinate_shots (dict, optional): A dictionary of shots taken at a specific location, as returned by the build_coordinate_shots() function. If not provided, the function will call build_coordinate_shots()
	- player_id_set (set, optional): A set of player IDs, as returned by the build_player_id_set() function. If not provided, the function will call build_player_id_set()
	- player_teams (dict, optional): A dictionary of player IDs and their corresponding teams, as returned by the build_player_teams() function. If not provided, the function will call build_player_teams()
	- team_set (set, optional): A set of team IDs, as returned by the build_team_set() function. If not provided, the function will call build_team_set()
	- team_games (dict, optional): A dictionary of teams and the games they played, as returned by the build_team_games() function. If not provided, the function will call build_team_games()
	- player_id_games (dict, optional): A dictionary of player IDs and the games they played, as returned by the build_player_id_games() function. If not provided, the function will call build_player_id_games()
	- player_shots (list, optional): A list of shots taken by the player, as returned by the get_player_shots_against() function. If not provided, the function will call get_player_shots_against()

	Returns:
	- The proportion of shots taken by the player at the specified coordinates that resulted in goals, as a float between 0 and 1.

	Example usage:
	proportion_of_goals = get_coordinate_goal_shot_ratio_against(player_id=8471214, x=25, y=50)
	"""
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
    """
    This function returns the proportion of goals to shots for a given player at a specific coordinate (x, y) on the ice.
    If the games_trimmed, player_id_set, player_teams, team_set, team_games, player_id_games, player_shots and coordinate_shots arguments are not provided, the function will build them using the appropriate helper functions.
    """
    print("get_coordinate_goal_shot_ratio_for_player()", end="\r")
    if games_trimmed is None:
        games_trimmed = build_games_trimmed(games_directory)
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
    """
    This function is used to build a dictionary of all the coordinates of shots made by each player. 
    The dictionary is keyed by player ID and contains a list of tuples, where each tuple is a pair of x, y coordinates.
    """
    # Initialize the player_id_set, player_teams, team_set, team_games and player_id_games if they are not passed in
    if player_id_set is None:
        player_id_set = build_player_id_set()
    if player_teams is None:
        player_teams = build_player_teams(player_id_set=player_id_set)
    if team_set is None:
        team_set = build_team_set()
    if team_games is None:
        team_games = build_team_games(team_set=team_set)
    if player_id_games is None:
        player_id_games = build_player_id_games(player_id_set=player_id_set, player_teams=player_teams, team_games=team_games)

    # Create an empty dictionary to store player coordinates
    player_coordinates = {}

    # Loop through each player ID in the player_id_set
    for playerID in player_id_set:
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
    """
    This function will parse through all the .json files in a specified directory,
    read the json file, extract the home and away team's triCode and store it in a dictionary with key as gameID
    and value as tuple of home and away team's triCode.
    If no directory is specified, it will take the current directory as default.
    """
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

            # Extracting the gameID from the file name
            gameID = file_name.split(".")[0]
            
            # Retrieve the teams data from the game file
            teams = game_data['gameData']['teams']

            # Retrieve the triCodes for the home and away teams
            home_triCode = teams['home']['triCode']
            away_triCode = teams['away']['triCode']

            # Add an entry to the home_away_teams dictionary for the current gameID with the home and away teams as the value
            home_away_teams[gameID] = (home_triCode, away_triCode)

    return home_away_teams


def build_coordinate_shots(games_trimmed=None):
    """
    Build a dictionary of shots grouped by their x,y coordinate location from a games_trimmed dictionary
    :param games_trimmed: A dictionary containing the shots for each game_id, as returned by the build_games_trimmed() function
    :return: A dictionary of shots grouped by their x,y coordinate location, where the key is a tuple of (x, y) and the value is a list of tuples containing (game_id, shot_num)
    """
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
    """
    The function build_game_shifts() reads in .json files from the specified directory, extracts shift data from them, and organizes the data into a nested dictionary.
    The nested dictionary has the following structure:
    {
        game_id: {
            home: {
                triCode: 'XXX',
                players: {
                    player_id: {
                        playerName: 'Firstname Lastname',
                        period1: set([(start_time, end_time), ...]),
                        period2: set([(start_time, end_time), ...]),
                        period3: set([(start_time, end_time), ...]),
                    },
                    ...
                },
            },
            away: {
                triCode: 'XXX',
                players: {
                    player_id: {
                        playerName: 'Firstname Lastname',
                        period1: set([(start_time, end_time), ...]),
                        period2: set([(start_time, end_time), ...]),
                        period3: set([(start_time, end_time), ...]),
                    },
                    ...
                },
            },
        },
        ...
    }
    """
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
                # Check if the current shift is in the first 3 periods and the player is not None
                if data[k][i]['period'] <= 3 and data[k][i]['playerId'] != None:
                    playerID = data[k][i]['playerId']
                    # Check if the shift is played by home team or away team
                    if data[k][i]['teamAbbrev'] = game_shifts[gameID][home][triCode]:
                        # Check if the player already exists in the home team's shift data
                        if playerID in game_shifts[gameID][home][players]:
                            player_dict = game_shifts[gameID][home][players][playerID]
                        else:
                            # Create new entry for the player if he does not exist
                            game_shifts[gameID][home][players][playerID] = {}
                            player_dict = game_shifts[gameID][home][players][playerID]
                            player_dict[playerName] = str(data[k][i][firstName] + " " + data[k][i][lastName])
                            player_dict[period1] = set()
                            player_dict[period2] = set()
                            player_dict[period3] = set()
                    else:
                        # Check if the player already exists in the away team's shift data
                        if playerID in game_shifts[gameID][away][players]:
                            player_dict = game_shifts[gameID][away][players][playerID]
                        else:
                            # Create new entry for the player if he does not exist
                            game_shifts[gameID][away][players][playerID] = {}
                            player_dict = game_shifts[gameID][away][players][playerID]
                            player_dict[playerName] = str(data[k][i][firstName] + " " + data[k][i][lastName])
                            player_dict[period1] = set()
                            player_dict[period2] = set()
                            player_dict[period3] = set()
                    shift_period = data[k][i]['period']
                    # Assign the shift to the corresponding period
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
    """
    This function takes in a player ID and a dictionary of trimmed game data and returns a dictionary of the teams 
    the player has played for in each year. 
    If games_trimmed is not provided, the function will return None and prompt the user to build the dictionary 
    with the build_games_trimmed() function.
    """
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
    """
    This function takes in a player_id and optionally games_trimmed, player_id_set, player_teams, team_set and team_games as input.
    If games_trimmed is not provided, the function first builds player_id_set, player_teams, team_set and team_games using the appropriate helper functions.
    The function then uses the player_teams and team_games to find all the gameIDs for the given player_id and returns a dictionary with the year as key and a list of gameIDs as value.
    """
    print("get_single_player_games()", end="\r")
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    if player_teams is None:
        player_teams = build_player_teams(games_trimmed=games_trimmed, player_id_set=player_id_set)
    if player_id not in player_id_set:
        print(f"Player ID {player_id} not found in player_id_set.")
        return None
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
    """
    This function builds a dictionary containing the teams that each player in the player_id_set has played for in each year.
    The dictionary is in the format of {player_id: {year: [triCodes]}}
    
    games_trimmed: A dictionary containing all of the shot data for all games, in the format returned by the build_games_trimmed() function. 
                   If not provided, an error message is printed and the function returns None.
    player_id_set: A set containing player IDs for all players that have taken shots in the provided games_trimmed.
                   If not provided, it will be built by calling the build_player_id_set() function on games_trimmed
    """
    print("build_player_teams()")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if player_id_set is None:
        player_id_set = build_player_id_set(games_trimmed=games_trimmed)
    player_teams = {}
    # Iterate over the set of player IDs
    for player in player_id_set:
        # Get the teams for each player by calling the get_single_player_teams() function
        player_teams[player] = get_single_player_teams(player, games_trimmed=games_trimmed)
    return player_teams



def build_player_id_games(games_trimmed=None, player_id_set=None, player_teams=None, team_set=None, team_games=None):
    """
    This function takes games_trimmed and the output of the following functions as arguments:
    build_player_id_set(games_trimmed), build_player_teams(games_trimmed, player_id_set),
    build_team_set(games_trimmed), build_team_games(games_trimmed, team_set)
    The function returns a dictionary with player_ids as keys, and nested dictionaries with years as keys, and lists of game ids as values
    """
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
    """
    This function takes in the games_trimmed dictionary, which should be created by the build_games_trimmed() function.
    It returns a set of player IDs that have played in the games represented in games_trimmed.
    """
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
    """
    This function extracts the unique team tri-codes from the games_trimmed dictionary and returns a set containing those tri-codes.
    games_trimmed : dict
        A dictionary containing the game data, where the keys are game ids and the values are dictionaries containing the shot data for that game.
    """
    print("build_team_set()")
    # check if games_trimmed is None
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    
    # initialize empty set
    triCodes = set()
    
    # iterate over games_trimmed
    for gameID, game_dict in games_trimmed.items():
        #iterate over shots in each game
        for shot in game_dict.values():
            # add team tri-code to set
            triCodes.add(shot['team']['triCode'])
    # return the set
    return triCodes


def build_team_games(games_trimmed=None, team_set=None):
    """
    Function to build a dictionary containing all games played by each team in the dataset.
    If games_trimmed is not provided, the function will call the build_games_trimmed() function to create it.
    If team_set is not provided, the function will call the build_team_set() function to create it.
    
    :param games_trimmed: (optional) a dictionary containing all the games in the dataset in the format {game_id: {shot_num: shot_data}}
    :type games_trimmed: dict
    :param team_set: (optional) a set containing the 3-letter team codes of all teams in the dataset
    :type team_set: set
    :return: a dictionary containing all games played by each team in the dataset in the format {team: [list of game ids]}
    :rtype: dict
    """
    print("build_team_games()")
    if games_trimmed is None:
        print("Please build games_trimmed with the build_games_trimmed() function. \nPass the directory your game .json files are saved in as its argument.")
        return None
    if team_set == None:
        team_set = build_team_set(games_trimmed=games_trimmed)
    team_games = {}
    for team in team_set:
        team_games[team] = get_single_team_games(team, games_trimmed=games_trimmed)
    return team_games


def get_single_team_games(triCode, games_trimmed=None):
    """
    This function takes in a team's tricode and a dictionary of games_trimmed, which is a dictionary containing 
    information about each shot in each game, as its inputs. It returns a dictionary containing the game ids for
    each year that the input team has played in.
    """
    print("get_single_team_games()", end="\r", flush=True)
    if games_trimmed == None:
        print("Please build games_trimmed with the build_games_trimmed() function.\nPass the directory your game .json files are saved in as its argument.")
        return None
    # Initialize an empty dictionary to store the games a team has played in each year
    games_teamID = {}
    progress = 0
    length = 80
    gtlength = len(games_trimmed)
    # Iterate over the shot dictionaries in the games_trimmed dictionary
    for gameID, game_dict in games_trimmed.items():
        progress += 1
        print("[", "="*((progress*length)//gtlength), " "*(length-((progress*length)//gtlength)), "] Current game:", gameID, end="\r", flush=True)
        for shot in game_dict.values():
            # Retrieve the triCode, year, and gameID for the current shot
            game_triCode = shot['team']['triCode']

            # Check if the triCode matches the input triCode
            if game_triCode == triCode:
                year = get_game_year(gameID)
                # Check if the year already exists as a key in the games_teamID dictionary
                if year not in games_teamID:
                    # If the year does not exist as a key, initialize an empty list for that year as the value of the key
                    games_teamID[year] = []

                # Append the gameID to the list of games for that year in the games_teamID dictionary
                if gameID not in games_teamID[year]:
                    games_teamID[year].append(gameID)

    # Return the games_teamID dictionary
    return games_teamID



def build_games_trimmed(directory='.'):
    """ 
    This function is used to process json files in the specified directory, and extract certain game-related data from them.
    The extracted data is then stored in a dictionary and returned.
    """
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
    # Initialize an empty list to store the x-coordinates of the shots in the game
    gameExes = []
    # Loop through the shots in the game
    for i in range(1, len(gameDict)):
        # Append the x-coordinate of the current shot to the list
        gameExes.append(gameDict[i]['coordinates']['x'])
    # Return the list of x-coordinates
    return gameExes



def switchGameExes(gameDict):
    """
    This function receives a game dictionary and multiplies the x coordinate of each shot by -1.
    This allows the shots to be directly comparable.
    """
    # Loop through the shots in the gameDict
    for i in range(1, len(gameDict)):
        # Multiply the x coordinate of the shot by -1
        gameDict[i]['coordinates']['x'] *= -1


def build_grouped_data(games_trimmed=None, coordinate_shots=None):
    """
    This function takes in a dictionary of games_trimmed, which contains the data for each game, 
    and optionally a dictionary of coordinate_shots, which contains the shots data. 
    The function groups the shots data into a new dictionary, grouped_data, based on their coordinates.
    The x and y coordinates of each shot are divided by 5 and 3 respectively, and then the quotient is used as the key in the new dictionary.
    The value in the new dictionary is a list of shots that fall within that grid cell.
    """
    # Initialize the new dictionary
    grouped_data = {}
    
    # if the coordinate_shots are not provided, use the function build_coordinate_shots to get the data
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
    """
    This function returns the average goal-to-shot ratio of a given player, and the ratio of each group of shots.
    It takes in the player's ID, the trimmed game data, the coordinate shots data, and the grouped data.
    """
    # Print message to show the function is running
    print("get_player_avg_pct_counts_and_groups()", end="\r", flush=True)
    # If grouped data is not passed, then build it using the provided game data and coordinate shots data
    if grouped_data is None:
        grouped_data = build_grouped_data(games_trimmed=games_trimmed, coordinate_shots=coordinate_shots)
    # Get the shots made by the player
    player_shots = get_shots_by_player(playerID)
    # Make a copy of the grouped shots data
    weighted_shots = grouped_data.copy()
    # Initialize a dictionary to store the ratio of each group
    group_dict = {}
    # Initialize the total ratio and weight
    total_ratio = 0
    total_weight = 0
    # Initialize the progress indicator
    progress = 0
    length = 60
    # Add the player's shots to the weighted shots
    for gameID, shot in player_shots:
        x, y = get_shot_grouped_coordinates(gameID, shot, games_trimmed=games_trimmed)
        for _ in range(1, 850):
            weighted_shots[(x, y)].append((gameID, shot))
    # Get the length of the weighted shots
    wslength = len(weighted_shots)
    # Iterate through each group of shots
    for (x, y) in weighted_shots:
        # Update the progress indicator
        progress += 1
        # Print the progress indicator
        print("[", "="*((progress*length)//wslength), " "*(length-((progress*length)//wslength)), "] - Current coordinate:", x, y, "Current player:", playerID, end="\r", flush=True)
        # Get the ratio of goals to shots for the current group
        group_ratio = get_goal_shot_ratio(playerID, player_shots=weighted_shots[(x, y)], count=1)
        # Add the ratio of the current group to the total ratio
        total_ratio += group_ratio[0] * len(weighted_shots[(x, y)])
        # Add the weight of the current group to the total weight
        total_weight += len(weighted_shots[(x, y)])
        # Add the ratio of the current group to the group dictionary
        group_dict[(x, y)] = group_ratio
    # Return the average ratio and the group ratios
    return (total_ratio / total_weight, group_dict)


def get_player_avg_pct_and_groups(playerID, games_trimmed=None, coordinate_shots=None, player_id_set=None, player_teams=None, team_set=None, team_games=None, player_id_games=None, grouped_data=None, player_shots=None):
    """
    This function takes in a player ID and returns the average shooting percentage 
    and a dictionary of shooting percentages for each (x, y) coordinate group.
    """
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
    
    # weight the shots by adding them to the corresponding coordinate group in the weighted_shots dictionary
    for gameID, shot in player_shots:
        x, y = get_shot_grouped_coordinates(gameID, shot, games_trimmed=games_trimmed)
        for _ in range(1, 850):
            weighted_shots[(x, y)].append((gameID, shot))
            
    # calculate the goal shot ratio for each coordinate group
    for (x, y) in weighted_shots:
        group_ratio = get_goal_shot_ratio(playerID, player_shots=weighted_shots[(x, y)], count=False, games_trimmed=games_trimmed, player_id_set=player_id_set, player_teams=player_teams, team_set=team_set, team_games=team_games, player_id_games=player_id_games)
        # add the group ratio to the total ratio, weighted by the number of shots in the group
        total_ratio += group_ratio * len(weighted_shots[(x, y)])
        total_weight += len(weighted_shots[(x, y)])
        group_dict[(x, y)] = group_ratio
    # calculate the overall average goal shot ratio by dividing the total ratio by the total weight
    return (total_ratio / total_weight, group_dict)


def get_shot_coordinates(gameID, shotID, games_trimmed=None):
    """
    This function takes in the gameID and shotID for a specific shot, as well as the games_trimmed dictionary, which is a dictionary where each key is a gameID and each value is a list of shots for that game.
    The function returns a tuple of the x and y coordinates for that shot.
    """
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
