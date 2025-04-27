from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

class Canvas:
    def __init__(self, root):
        root.title("NBA Player Comparison")

        # Configure the root so that it stretches in all directions
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # change the style
        style = ttk.Style(root)
        style.theme_use('clam')

        # make a frame for the GUI
        self.frame = ttk.Frame(root, padding="10 10 10 10")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        # Team Selection
        label = ttk.Label(self.frame,
                          text="Select A Team:",
                          justify="center")
        label.grid(column=0, row=0, sticky=(W, E))
        label.configure(anchor="center")

        team_list = teams.get_teams()
        self.team_id_dict = {}
        team_list_dropdown = []
        for team in team_list:
            self.team_id_dict[team['full_name']] = team['id']
            team_list_dropdown.append(team['full_name'])

        team_list_dropdown.sort()
        self.team_combo_box = ttk.Combobox(self.frame, values=team_list_dropdown)
        self.team_combo_box.grid(column=0, row=1, sticky=(W, E))

        self.team_combo_box.bind("<<ComboboxSelected>>", self.select_team)

        # Player 1 Selection
        label = ttk.Label(self.frame,
                          text="Select Player 1:",
                          justify="center")
        label.grid(column=1, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_1_combo_box = ttk.Combobox(self.frame)
        self.player_1_combo_box.grid(column=1, row=1, sticky=(W, E))

        # Player 2 Selection
        label = ttk.Label(self.frame,
                          text="Select Player 2:",
                          justify="center")
        label.grid(column=2, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_2_combo_box = ttk.Combobox(self.frame)
        self.player_2_combo_box.grid(column=2, row=1, sticky=(W, E))

        generate_button = ttk.Button(self.frame, text="Ok", command=self.generate_data)
        generate_button.grid(column=3, row=1, sticky=(W, E))

    def select_team(self, event):
        """
        Runs when the user selects a combobox dropdown
        """
        print(self.team_combo_box.get())
        team_id = self.team_id_dict[self.team_combo_box.get()]
        season = "2024-25"
        selected_roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
        selected_roster_df = selected_roster.get_data_frames()[0]
        players_list = selected_roster_df["PLAYER"].tolist()
        self.player_1_combo_box.set('')
        self.player_2_combo_box.set('')
        self.player_1_combo_box['values'] = players_list
        self.player_2_combo_box['values'] = players_list

    def get_player_id(self, name):
        matches = players.find_players_by_full_name(name)
        return matches[0]['id'] if matches else None

    def get_game_logs(self, player_id):
        logs = playergamelog.PlayerGameLog(player_id=player_id, season='2024').get_data_frames()[0]
        logs['GAME_DATE'] = pd.to_datetime(logs['GAME_DATE'])
        return logs

    def merge_logs(self, player1_logs, player2_logs):
        player1_logs['with_other_player'] = player1_logs['GAME_DATE'].isin(player2_logs['GAME_DATE'])
        return player1_logs

    def generate_data(self):
        # Getting player names from dropdown menu
        p1_name = self.player_1_combo_box.get()
        p2_name = self.player_2_combo_box.get()
        # Player name input
        p1_id = self.get_player_id(p1_name)
        p2_id = self.get_player_id(p2_name)

        if p1_id == p2_id:
            print("Error: Same Player Selected")
            return
        
        # Fetching logs 
        p1_logs = self.get_game_logs(p1_id)
        p2_logs = self.get_game_logs(p2_id)

        # Merge logs with the other player information
        merged = self.merge_logs(p1_logs, p2_logs)

        # Filter unneeded data
        columns_to_keep = ['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST', 'with_other_player']
        merged = merged[columns_to_keep]

        # Save to CSV
        merged.to_csv(f'player_comparison_data.csv', index=False)
        print("Data generated and saved to player_comparison_data.csv")

# create a root Tk object
root = Tk()

# create a Canvas object with the Tk root object as an argument
canvas = Canvas(root)

# call the mainloop method on the Tk root object
root.mainloop()
