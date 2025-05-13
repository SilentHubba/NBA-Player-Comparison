# NBA-Player-Comparison
Project Title: NBA Player Comparison

Authors: Jonathan Sy and Daniel Chukhlebov

Description of Program:
This project is an app to help users analyze players, specifically targeted to fantasy basketball players. It comes with three main ways to analyze a player's performance that go beyond the simple averages of their stats. First, it compares how well a player performs when another player is injured or absent for another reason. This is useful for backups, who see more opportunities to accumulate stats when the starter is injured. Next, it shows a graph of every member of the team (who has played a game while the selected player is out) which compares how well they perform when the selected player is in and out of the game. This shows who performs better when a player is injured, and it helps users find potential candidates to perform better. Finally, it shows a graph of a player's performance on a game timeline. This gives context to an average by showing who has improved or regressed throughout the season.

Instructions For Installation:
1. Download main_page.py
2. Ensure the packages are installed in the python environment. This includes numpy, pandas, matplotlib, nba_api, and tkinter.
3. Run the python file with 'python3 main_page.py' in the terminal or some other method of choice. The program will generate the csv files automatically.

Potential Updates:
- Add a year selector to the app, so users could analyze stats from different years. Currently, it only takes stats from the 2024-2025 season.
- Show the basic stats of each player. This information is available on other websites (such as espn), which is why we did not prioritize it. However, having all of the information available in one spot is more convinient.
- Show the number of games each average is based on. It would give more context to these stats.




Pre-completion Information:

Project Description:
The goal of this project is to compare two NBA players. More specifically, it will compare the two player's stats when they are both playing and when each of them is not playing. This will allow users to separate how well each player plays when the other is not on the court for fantasy basketball. One use case of this is when a starting player gets hurt. Using this application, a user can see how well the backup player plays when the starter is not playing to see if they are worth rostering or not. 

Project Outline:

Interface plan:
- We will be using the Tkinter library to create a GUI for the project. It will have a main window to show the application containing multiple dropdowns to search for a given pair of players. THe second window will be a way to edit the points per stat, so it can fit any points scoring system as necessary.

Group Member 1 Plan (Daniel):
- We will use a publicly available API to obtain player info such as names, game statistics, and activity/inactivity.
- The gathered data will be stored and manpulated in .csv format using the pandas data analysis library.
- Data from the API will be fetched on demand and data from the stored files will be loaded upon startup.

Group Member 2 Plan (Jonathan):
- The data analysis will use the numpy module to average and compare the stats of a player when another player is playing and not playing. This will mainly be averages of the stats per game.
- The visualization will be a series of bar graphs to show the increase/decrease in stats a player has when another player is not playing.
