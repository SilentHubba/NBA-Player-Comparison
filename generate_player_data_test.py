# this file contains a short script which fetches data for a p1 and generates filtered game data as a pandas dataframe.
# p1's games in which p2 participated are denoted as true in with_other_player column
# the player_comparison_data.csv file on the repo provides an example generated file for Terry Rozier and Bam Adebayo for 2024 season
# data is generated and written to same file to avoid overhead and file bloat
# run 'pip install nba_api' in conda console if api is not installed

import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog


def get_player_id(name):
    matches = players.find_players_by_full_name(name)
    return matches[0]['id'] if matches else None

def get_game_logs(player_id):
    logs = playergamelog.PlayerGameLog(player_id=player_id, season='2024').get_data_frames()[0]
    logs['GAME_DATE'] = pd.to_datetime(logs['GAME_DATE'])
    return logs

def merge_logs(player1_logs, player2_logs):
    player1_logs['with_other_player'] = player1_logs['GAME_DATE'].isin(player2_logs['GAME_DATE'])
    return player1_logs

# Player Name Input
p1_name, p2_name = "Terry Rozier", "Bam Adebayo" #input player names here
p1_id, p2_id = get_player_id(p1_name), get_player_id(p2_name)

# Fetching logs 
p1_logs = get_game_logs(p1_id)
p2_logs = get_game_logs(p2_id)

# with_other_player column
merged = merge_logs(p1_logs, p2_logs)

# Filter unneeded data
columns_to_keep = ['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST', 'with_other_player']
merged = merged[columns_to_keep]

merged.to_csv(f'player_comparison_data.csv', index=False)

