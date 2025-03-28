# NBA-Player-Comparison
Project Title: NBA Player Comparison

Authors: Jonathan Sy and Daniel Chukhlebov

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
