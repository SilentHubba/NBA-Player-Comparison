from tkinter import *
from tkinter import ttk
import numpy as np
from nba_api.stats.static import teams
#from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonteamroster
import pandas as pd

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
        self.frame = ttk.Frame(root, padding = "10 10 10 10")
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
                          text="Select Missing Player:", 
                          justify="center")
        label.grid(column=1, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_1_combo_box = ttk.Combobox(self.frame)
        self.player_1_combo_box.grid(column=1, row=1, sticky=(W, E))

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
        self.player_1_combo_box['values'] = players_list





# create a root Tk object
root = Tk()

# create a HeyThere object with the Tk root object as an argument
Canvas(root)

# call the mainloop method on the Tk root object
root.mainloop()