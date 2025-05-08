from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import math

class MainPage:
    def __init__(self, root):
        root.title("NBA Player Comparison")

        # Configure the root so that it stretches in all directions
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # change the style
        style = ttk.Style(root)
        style.theme_use('clam')


        self.pages = []
        #classes = [PlayerComparisonPage]
        #self.pages.append(self.create_player_comparison_page(root))
        #self.pages.append(self.create_compare_full_team_page(root))
        self.current_page = None

        #for page in self.pages:
            #page.grid_configure(row=1)

        self.create_top_bar(root=root)
        
        #self.show_page(self.create_player_comparison_page)
        self.create_player_comparison_page(root)

    def clear_page(self):
        #print("running", frame)
        # for page in self.pages:
        #     page.grid_forget()
        if self.current_page:
            self.current_page.grid_forget()

        #frame.tkraise()
        
        #self.pages.append(frame())


    def create_top_bar(self, root):
        self.menu = ttk.Frame(root, relief="raised")
        self.menu.grid(column=0, row=0, sticky=(N, W, E, S))

        home_button = ttk.Button(self.menu, text="Player Comp", command=lambda: self.create_player_comparison_page(root))
        home_button.grid(column=0, row=0)

        team_comp_button = ttk.Button(self.menu, text="Player Comp With Team", command=lambda: self.create_compare_full_team_page(root))
        team_comp_button.grid(column=1, row=0)

        player_season_button = ttk.Button(self.menu, text="Full Player Season", command=lambda: self.create_player_season_page(root))
        player_season_button.grid(column=2, row=0)
        """
        menu = Menu(root)

        page_menu = Menu(menu, tearoff=0)
        page_menu.add_command(label="Home", command=lambda: self.show_page(self.pages[0]))
        menu.add_cascade(label="Navigate", menu=page_menu)
        root.config(menu=menu)
        """

    def create_player_season_page(self, root):
        # Clear Current Page
        self.clear_page()
        # Make frame for GUI
        self.player_season_page = ttk.Frame(root, padding="10 10 10 10")
        self.player_season_page.grid(column=0, row=1, sticky=(N, W, E, S))

        self.current_page = self.player_season_page

        self.player_season_page.columnconfigure(0, weight=1)
        self.player_season_page.columnconfigure(1, weight=1)
        self.player_season_page.columnconfigure(2, weight=1)
        self.player_season_page.columnconfigure(3, weight=1)
        self.player_season_page.rowconfigure(2, weight=1)

        
        # Team Selection
        label = ttk.Label(self.player_season_page,
                          text="Select A Team:",
                          justify="center")
        label.grid(column=0, row=0, sticky=(W, E))
        label.configure(anchor="center")

        team_list = teams.get_teams()
        self.team_id_dict = {}
        self.team_list_dropdown = []
        for team in team_list:
            self.team_id_dict[team['full_name']] = team['id']
            self.team_list_dropdown.append(team['full_name'])

        self.team_list_dropdown.sort()
        self.team_combo_box = ttk.Combobox(self.player_season_page, values=self.team_list_dropdown)
        self.team_combo_box.grid(column=0, row=1, sticky=(W, E))

        self.team_combo_box.bind("<<ComboboxSelected>>", self.select_team)

        # Current Player Selection Field
        # Why does this not work before selecting a team in Player Comp With Team????
        # SOS biggest bug ever
        label = ttk.Label(self.player_season_page,
                          text="Select Player:",
                          justify="center")
        label.grid(column=1, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_combo_box = ttk.Combobox(self.player_season_page)
        self.player_combo_box.grid(column=1, row=1, sticky=(W, E))

        # Ok Button
        generate_button = ttk.Button(self.player_season_page, text="Ok", command=self.generate_season_data)
        generate_button.grid(column=2, row=1, sticky=(N, W, E, S))

        # Graphs
        self.plt_figure = Figure()
        self.min_subplot = self.plt_figure.add_subplot(221)
        self.min_subplot.plot([], [])
        self.min_subplot.set_title("Minutes Per Game")

        self.pts_subplot = self.plt_figure.add_subplot(222)
        self.pts_subplot.plot([], [])
        self.pts_subplot.set_title("Points Per Game")

        self.rebs_subplot = self.plt_figure.add_subplot(223)
        self.rebs_subplot.plot([], [])
        self.rebs_subplot.set_title("Rebounds Per Game")

        self.asi_subplot = self.plt_figure.add_subplot(224)
        self.asi_subplot.plot([], [])
        self.asi_subplot.set_title("Assists Per Game")

        self.canvas = FigureCanvasTkAgg(self.plt_figure, master=self.player_season_page)
        # add spacing
        self.plt_figure.subplots_adjust(wspace=0.5, hspace=0.5)
        # add a title
        self.plt_figure.suptitle("Player Stats", fontsize=16)
        

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=2, columnspan=3, sticky=(N, E, S, W))

        return self.player_season_page


######################################################################################################
    def create_compare_full_team_page(self, root):
        # Clear previous page
        self.clear_page()


        self.full_team_page = ttk.Frame(root, padding="10 10 10 10")
        self.full_team_page.grid(column=0, row=1, sticky=(N, W, E, S))

        # Set current page so we can remove it
        self.current_page = self.full_team_page

        self.full_team_page.columnconfigure(0, weight=1)
        self.full_team_page.columnconfigure(1, weight=1)
        self.full_team_page.columnconfigure(2, weight=1)
        self.full_team_page.columnconfigure(3, weight=1)
        self.full_team_page.columnconfigure(4, weight=1)

        # Team selection
        # Label
        label = ttk.Label(self.full_team_page,
                          text="Select Team:",
                          justify="center")
        label.grid(column=0, row=0, sticky=(W, E))
        label.configure(anchor="center")

        # Combo box
        self.team_combo_box = ttk.Combobox(self.full_team_page, values=self.team_list_dropdown)
        self.team_combo_box.grid(column=1, row=0, sticky=(W, E))

        self.team_combo_box.bind("<<ComboboxSelected>>", self.select_team)

        # Player Selection Field
        label = ttk.Label(self.full_team_page,
                          text="Select Injured/Absent Player:",
                          justify="center")
        label.grid(column=2, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_3_combo_box = ttk.Combobox(self.full_team_page)
        self.player_3_combo_box.grid(column=3, row=0, sticky=(W, E))

        # Button to search
        generate_button = ttk.Button(self.full_team_page, text="Ok", command=self.generate_full_team_data)
        generate_button.grid(column=4, row=0, sticky=(N, W, E, S))

        # Graph
        self.pts_rebs_ast_graph = Figure()
        self.pts_rebs_ast_plot = self.pts_rebs_ast_graph.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.pts_rebs_ast_graph, master=self.full_team_page)
        # add spacing
        self.plt_figure.subplots_adjust(wspace=0.5, hspace=0.5)
        # add a title
        self.plt_figure.suptitle("Player Stats With/Without A Player", fontsize=16)

        self.pts_rebs_ast_plot.set_xlim(0, 50)
        self.pts_rebs_ast_plot.set_ylim(0, 50)
        self.pts_rebs_ast_plot.plot([0, 50], [0, 50], color='gray', linestyle='--')
        self.pts_rebs_ast_plot.set_aspect('equal')

        self.pts_rebs_ast_plot.set_title("Pts+Rebs+Ast With vs Without Player")
        self.pts_rebs_ast_plot.set_xlabel("Pts+Rebs+Ast With Player")
        self.pts_rebs_ast_plot.set_ylabel("Pts+Rebs+Ast Without Player")

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=1, columnspan=5, sticky=(N, E, S, W))

        # self.min_subplot = self.plt_figure.add_subplot(111)
        # self.min_subplot.bar(categories, values)
        # self.min_subplot.set_title("Minutes Per Game")

        return self.full_team_page

    def create_player_comparison_page(self, root):
        # Clear Current Page
        self.clear_page()
        
        # make a frame for the GUI
        self.frame = ttk.Frame(root, padding="10 10 10 10")
        self.frame.grid(column=0, row=1, sticky=(N, W, E, S))

        # Set current page so we can remove it
        self.current_page = self.frame

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        #self.frame.rowconfigure(0, weight=1)
        #self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # Team Selection
        label = ttk.Label(self.frame,
                          text="Select A Team:",
                          justify="center")
        label.grid(column=0, row=0, sticky=(W, E))
        label.configure(anchor="center")

        team_list = teams.get_teams()
        self.team_id_dict = {}
        self.team_list_dropdown = []
        for team in team_list:
            self.team_id_dict[team['full_name']] = team['id']
            self.team_list_dropdown.append(team['full_name'])

        self.team_list_dropdown.sort()
        self.team_combo_box = ttk.Combobox(self.frame, values=self.team_list_dropdown)
        self.team_combo_box.grid(column=0, row=1, sticky=(W, E))

        self.team_combo_box.bind("<<ComboboxSelected>>", self.select_team)

        # Player 1 Selection
        label = ttk.Label(self.frame,
                          text="Select Active Player:",
                          justify="center")
        label.grid(column=1, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_1_combo_box = ttk.Combobox(self.frame)
        self.player_1_combo_box.grid(column=1, row=1, sticky=(W, E))

        # Player 2 Selection
        label = ttk.Label(self.frame,
                          text="Select Absent Player:",
                          justify="center")
        label.grid(column=2, row=0, sticky=(W, E))
        label.configure(anchor="center")

        self.player_2_combo_box = ttk.Combobox(self.frame)
        self.player_2_combo_box.grid(column=2, row=1, sticky=(W, E))

        # OK Button
        generate_button = ttk.Button(self.frame, text="Ok", command=self.generate_data)
        generate_button.grid(column=3, row=1, sticky=(N, W, E, S))

        # Graphs
        categories = ['With Player', 'Without Player']
        values = [0, 0]

        self.plt_figure = Figure()#figsize=(2, 2))
        self.min_subplot = self.plt_figure.add_subplot(221)
        self.min_subplot.bar(categories, values)
        self.min_subplot.set_title("Minutes Per Game")

        self.pts_subplot = self.plt_figure.add_subplot(222)
        self.pts_subplot.bar(categories, values)
        self.pts_subplot.set_title("Points Per Game")

        self.rebs_subplot = self.plt_figure.add_subplot(223)
        self.rebs_subplot.bar(categories, values)
        self.rebs_subplot.set_title("Rebounds Per Game")

        self.asi_subplot = self.plt_figure.add_subplot(224)
        self.asi_subplot.bar(categories, values)
        self.asi_subplot.set_title("Assists Per Game")

        self.canvas = FigureCanvasTkAgg(self.plt_figure, master=self.frame)
        # add spacing
        self.plt_figure.subplots_adjust(wspace=0.5, hspace=0.5)
        # add a title
        self.plt_figure.suptitle("Player Stats", fontsize=16)
        

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=2, columnspan=4, sticky=(N, E, S, W))

        return self.frame


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
        players_list.sort()

        # Update the frame if player comparison fields is open
        if self.current_page == self.frame:
            self.player_1_combo_box.set('')
            self.player_2_combo_box.set('')
            self.player_1_combo_box['values'] = players_list
            self.player_2_combo_box['values'] = players_list
        elif self.current_page == self.full_team_page:
            self.player_3_combo_box.set('')
            self.player_3_combo_box['values'] = players_list
        elif self.current_page == self.player_season_page:
            self.player_combo_box.set('')
            self.player_combo_box['values'] = players_list

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

        if not p1_name or not p2_name:
            print("missing player")
            return

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

        print(merged.columns.tolist())

        # Filter unneeded data
        columns_to_keep = ['GAME_DATE', 'MATCHUP', 'MIN', 'PTS', 'REB', 'AST', 'with_other_player']
        merged = merged[columns_to_keep]

        # Save to CSV
        merged.to_csv(f'player_comparison_data.csv', index=False)
        print("Data generated and saved to player_comparison_data.csv")

        # ANALYSIS
        self.plt_figure.suptitle(p1_name + "'s Stats", fontsize=16)
        self.calculate_averages(merged, p2_name, self.min_subplot, 'MIN', 'Minutes')
        self.calculate_averages(merged, p2_name, self.pts_subplot, 'PTS', 'Points')
        self.calculate_averages(merged, p2_name, self.rebs_subplot, 'REB', 'Rebounds')
        self.calculate_averages(merged, p2_name, self.asi_subplot, 'AST', 'Assists')

    def generate_full_team_data(self):
        player_name = self.player_3_combo_box.get()
        player_id = self.get_player_id(player_name)
        if not player_name:
            return
        
        #player_team = self.team_combo_box.get()
        player_id = self.get_player_id(player_name)
        #print(self.player_3_combo_box['values'])
        players = list(self.player_3_combo_box['values'])
        players.remove(player_name)
        player_data_dict = {}
        print(players)
        self.pts_rebs_ast_plot.clear()

        max_val = 0

        for player_2 in players:
            player_2_id = self.get_player_id(player_2)
            # Fetching logs 
            p1_logs = self.get_game_logs(player_id)
            p2_logs = self.get_game_logs(player_2_id)

            # Merge logs with the other player information
            merged = self.merge_logs(p2_logs, p1_logs)

            #print(merged.columns.tolist())

            # Filter unneeded data
            columns_to_keep = ['GAME_DATE', 'MATCHUP', 'MIN', 'PTS', 'REB', 'AST', 'with_other_player']
            merged = merged[columns_to_keep]

            print(merged.columns.tolist())
            max_val = max(self.graph_pts_rebs_ast(merged, player_2, self.pts_rebs_ast_plot), max_val)
            print(max_val)
            time.sleep(1)

            # ANALYSIS
            # self.plt_figure.suptitle(p1_name + "'s Stats", fontsize=16)
            # self.calculate_averages(merged, p2_name, self.min_subplot, 'MIN', 'Minutes')
            # self.calculate_averages(merged, p2_name, self.pts_subplot, 'PTS', 'Points')
            # self.calculate_averages(merged, p2_name, self.rebs_subplot, 'REB', 'Rebounds')
            # self.calculate_averages(merged, p2_name, self.asi_subplot, 'AST', 'Assists')
        
        # Configure axes
        self.pts_rebs_ast_plot.axhline(0, color='gray', linewidth=0.5)
        self.pts_rebs_ast_plot.axvline(0, color='gray', linewidth=0.5)

        max_val = math.ceil((max_val + 3) / 10) * 10

        self.pts_rebs_ast_plot.set_xlim(0, max_val)
        self.pts_rebs_ast_plot.set_ylim(0, max_val)
        self.pts_rebs_ast_plot.plot([0, max_val], [0, max_val], color='gray', linestyle='--')
        self.pts_rebs_ast_plot.set_aspect('equal')
        self.pts_rebs_ast_plot.set_title("Pts+Rebs+Ast With vs Without "+player_name)
        self.pts_rebs_ast_plot.set_xlabel("Pts+Rebs+Ast With " + player_name)
        self.pts_rebs_ast_plot.set_ylabel("Pts+Rebs+Ast Without " + player_name)
        self.pts_rebs_ast_plot.grid(True)
        self.canvas.draw()
    
    def generate_season_data(self):
        # Getting player name from dropdown menu
        p4_name = self.player_combo_box.get()

        if not p4_name:
            print("missing player")
            return

        # Player name input
        p4_id = self.get_player_id(p4_name)
        
        # Fetching logs 
        p4_logs = self.get_game_logs(p4_id)

        # Filter unneeded data
        columns_to_keep = ['GAME_DATE', 'MIN', 'PTS', 'REB', 'AST']
        p4_logs = p4_logs[columns_to_keep]

        # Save to CSV
        p4_logs.to_csv(f'player_seasonal_data.csv', index=False)
        print("Data generated and saved to player_seasonal_data.csv")

        # Sort data by date
        p4_logs = p4_logs.sort_values('GAME_DATE')
        dates = p4_logs['GAME_DATE'].dt.strftime('%Y-%m-%d')

        # Update plots
        self.plt_figure.suptitle(f"{p4_name}'s Season Stats", fontsize=16)

        # Minutes plot
        self.min_subplot.clear()
        self.min_subplot.plot(p4_logs['MIN'], marker='o', linestyle='-')
        self.min_subplot.set_title("Minutes Over Games")
        self.min_subplot.set_xlabel("Games")
        self.min_subplot.set_ylabel("Minutes")
        self.min_subplot.tick_params(axis='x', labelrotation=45, labelsize=7)

        # Points plot
        self.pts_subplot.clear()
        self.pts_subplot.plot(p4_logs['PTS'], marker='o', linestyle='-')
        self.pts_subplot.set_title("Points Over Games")
        self.pts_subplot.set_xlabel("Games")
        self.pts_subplot.set_ylabel("Points")
        self.pts_subplot.tick_params(axis='x', labelrotation=45, labelsize=7)

        # Rebounds plot
        self.rebs_subplot.clear()
        self.rebs_subplot.plot(p4_logs['REB'], marker='o', linestyle='-')
        self.rebs_subplot.set_title("Rebounds Over Games")
        self.rebs_subplot.set_xlabel("Games")
        self.rebs_subplot.set_ylabel("Rebounds")
        self.rebs_subplot.tick_params(axis='x', labelrotation=45, labelsize=7)

        # Assists plot
        self.asi_subplot.clear()
        self.asi_subplot.plot(p4_logs['AST'], marker='o', linestyle='-')
        self.asi_subplot.set_title("Assists Over Games")
        self.asi_subplot.set_xlabel("Games")
        self.asi_subplot.set_ylabel("Assists")
        self.asi_subplot.tick_params(axis='x', labelrotation=45, labelsize=7)

        # Adjust layout and redraw
        self.plt_figure.subplots_adjust(wspace=0.5, hspace=0.5)
        self.canvas.draw()




    def graph_pts_rebs_ast(self, dataframe, p1_name, plot):
        stats = ['PTS', 'REB', 'AST']
        with_player_pts_rebs_ast_mean = 0
        without_player_pts_rebs_ast_mean = 0
        for stat in stats:
            with_player_pts_rebs_ast_mean += dataframe.loc[dataframe['with_other_player'], stat].mean()
            without_player_pts_rebs_ast_mean += dataframe.loc[dataframe['with_other_player'] == False, stat].mean()
        
        # Exit if the player doesn't play/has no data
        if not without_player_pts_rebs_ast_mean or math.isnan(without_player_pts_rebs_ast_mean):
            return 0
        elif not with_player_pts_rebs_ast_mean or math.isnan(with_player_pts_rebs_ast_mean):
            with_player_pts_rebs_ast_mean = 0
        
        plot.plot(with_player_pts_rebs_ast_mean, without_player_pts_rebs_ast_mean, 'o', color='blue')
        plot.text(with_player_pts_rebs_ast_mean, without_player_pts_rebs_ast_mean + 1, p1_name, ha='center', va='center', fontsize=6)
        print(max(with_player_pts_rebs_ast_mean, without_player_pts_rebs_ast_mean))

        return max(with_player_pts_rebs_ast_mean, without_player_pts_rebs_ast_mean)

    def calculate_averages(self, dataframe, p2_name, plot, symbol='PTS', stat_name='Points'):
        with_player_mean = dataframe.loc[dataframe['with_other_player'], symbol].mean()
        without_player_mean = dataframe.loc[dataframe['with_other_player'] == False, symbol].mean()

        category_names = [stat_name + " with " + p2_name, stat_name + " without " + p2_name]
        category_values = [with_player_mean, without_player_mean]
        plot.clear()
        plot.bar(category_names, category_values)
        plot.set_title(stat_name + " Per Game")
        plot.tick_params(axis='x', labelrotation=10, labelsize=7)

        self.canvas.draw()

    


# create a root Tk object
#root = Tk()

# create a Canvas object with the Tk root object as an argument
#canvas = PlayerComparisonPage(root)

# call the mainloop method on the Tk root object
#root.mainloop()

root = Tk()
main_page = MainPage(root)
root.mainloop()
