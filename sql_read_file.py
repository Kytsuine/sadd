import psycopg2
import os
import json

# Define function to insert game data
def insert_game_data(conn, data):
    # Extract values from data dictionary
    game_id = data['gameData']['game']['pk']
    away_team_id = data['gameData']['teams']['away']['id']
    home_team_id = data['gameData']['teams']['home']['id']
    # Insert all data from game to pg
    cur = conn.cursor()
    query = "INSERT INTO games (game_id, away_team_id, home_team_id) VALUES (%s, %s, %s)"
    cur.execute(query, (game_id, away_team_id, home_team_id))
    conn.commit()
    cur.close()

def insert_official(data, official_number, conn):
    # Insert an official's information into the officials table.
    cur = conn.cursor()
    name = data['gameData']['liveData']['boxscore']['officials'][official_number]['official']['fullName']
    official_id = data['gameData']['liveData']['boxscore']['officials'][official_number]['official']['id']
    link = data['gameData']['liveData']['boxscore']['officials'][official_number]['official']['link']
    query = "INSERT INTO officials (official_id, name, link) VALUES (%s, %s, %s)"
    cur.execute(query, (official_id, name, link))
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

# Call the function to insert the data into the games table
insert_game_data(conn, game_data)
for iterable in game_data['liveData']['boxscore']['officials']:
    insert_official(game_data, iterable, conn)
