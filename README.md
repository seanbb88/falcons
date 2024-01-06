## Overview

This app is designed to initialize and populate databases, perform data retrieval using public information from the internet.Then some calculations are made based on the stored data. It serves as a tool to manage and analyze data related to various entities, such as clubs, players, transactions, history & salary for the nfl.

### Database Initialization

Before using the app, you'll need to initialize the database. Follow these steps:

1. Provide your PostgreSQL connection string in the `database.py` file.

   Example connection string: `"postgresql://your_username:your_password@localhost/"`

2. The app will create the necessary database if it doesn't already exist.


## Getting Started

1. Ensure you have PostgreSQL & python installed on your system.

2. Clone this repository to your local machine.

3. Navigate to the app's root directory.

4. Update the database connection string in `database.py` to match your local connection string.

5. Run `pip install -r requirements.txt` to install external dependencies.

6. Run the app by executing `python main.py`.


### Database Schema
-A more detailed database schema can be found [here](https://github.com/seanbb88/falcons/blob/main/database_schema_doc.md)

### Data Population

The app populates the database with the following data:

- Clubs: Information about sports clubs, including names, aliases, owners, and more.

- Players: Player profiles with details like name, birthdate, college, and current club.

- Player Transactions: Records of player transactions, including types, descriptions, dates, and clubs involved.

- Player History: Seasonal player performance data, including team, position, and playtime statistics.

- Player Salary: Salary information including team, year signed, average per year, salary amount, guarantee, and position

-Club,Position, Season Aggregations:
datasets that consists of the total offensive and defensive team plays per either club, season, or position over the gathered data period (2021 - 2023)

- Player Rankings:
dataset that consists of players player percentile rank compared to the above data for clubs, positions, and seasons


### Calculations

The app can perform various calculations and analysis on the stored data:

- **Play Aggregation**: several tables are created that rank the players on play time (by percentile) for several categories (club, season, position)

- **Salary Rankings**: using the data pulled from a webscrape this application prints out some visual comparisons of players salaries 

### Rankings

Several more tables are created that rank the players on plays played across the three agregated datasets (club, position, & season):

A condenced output of these aggregations are printed in the console as well.

- PlayerRankingSeasonAggregation: A data set that ranks players play percentile per season over the gathered data period (2021 - 2023)

- PlayerRankingPositionAggregation: A data set that ranks players play percentile per position over the gathered data period (2021 - 2023)

- PlayerRankingClubAggregation: A data set that ranks players play percentile per club over the gathered data period (2021 - 2023)

## Data Population
-Sports Radar API - https://sportradar.com/
-Sports Data IO - https://sportsdata.io/


## Contributors

- Sean Brown
