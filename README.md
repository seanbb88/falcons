# App README

## Overview

This app is designed to initialize and populate databases, perform data retrieval, and make calculations based on the stored data. It serves as a tool to manage and analyze data related to various entities, such as clubs, players, transactions, history & salary.

## Features
### Database Initialization

Before using the app, you'll need to initialize the database. Follow these steps:

1. Provide your PostgreSQL connection string in the `database.py` file.

   Example connection string: `"postgresql://your_username:your_password@localhost/"`


2. The app will create the necessary database if it doesn't already exist.

### Data Population

The app populates the database with the following data:

- Clubs: Information about sports clubs, including names, aliases, owners, and more.

- Players: Player profiles with details like name, birthdate, college, and current club.

- Transactions: Records of player transactions, including types, descriptions, dates, and clubs involved.

- Player History: Seasonal player performance data, including team, position, and playtime statistics.

- Player Salary: Contract information, including year signed, team, salary details, and position.

### Calculations

The app can perform various calculations and analysis on the stored data:

- **Play Aggregation**: several tables are created that rank the players on play time (by percentile) for several categories (club, season, position)


## Getting Started

1. Ensure you have PostgreSQL & python installed on your system.

2. Clone this repository to your local machine.

3. Navigate to the app's root directory.

4. Update the database connection string in `database.py` to match your PostgreSQL setup.

5. Run `pip install -r requirements.txt` to install external dependencies.

6. Run the app by executing `python main.py`.


## Contributors

- Sean Brown
