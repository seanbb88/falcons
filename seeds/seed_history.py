
from datetime import datetime
import time
import requests
from database import db 
from models import  Player, Club, History
from utils.dates import days_in_month, idx_to_month_str
from utils.loaders import print_progress_dots  
from .constants import SPORTS_IO_API_KEY


BEGINING_API_URL = "https://api.sportsdata.io/v3/nfl/stats/json/PlayerGameStatsByWeek/"
END_API_URL = f"?key={SPORTS_IO_API_KEY}"

year_options = ["2023", "2022", "2021"]


def display_year_menu():
    print("Please select an input number corresponding to the year in which to seed player history")
    print("---------------------------------")
    for idx, year in enumerate(year_options, start=1):
        print(f"{idx}. {year}")

    
def select_timeframe():
    while True:
        display_year_menu()

        try:
            selected_year = int(input("Select a year (enter the corresponding number): ").strip())
            
            if 1 <= selected_year <= len(year_options):
                selected_year = year_options[selected_year - 1]
                return selected_year
            else:
                print("Invalid year selection. Please choose a valid year.")
        except ValueError:
            print("Invalid input for year. Please enter a valid number.")
            

def transform_raw_data(raw_data):
    transformed_data = []
        
    for game_data in raw_data:
        
        offensive_plays = game_data["OffensiveSnapsPlayed"]
        offensive_team_plays = game_data["OffensiveTeamSnaps"]
        defensive_plays = game_data["DefensiveSnapsPlayed"]
        defensive_team_plays = game_data["DefensiveTeamSnaps"]

        if offensive_team_plays is not None and offensive_team_plays > 0:
            offense_play_time_percentage = (offensive_plays / offensive_team_plays) * 100
        else:
            offense_play_time_percentage = 0

        if defensive_team_plays is not None and defensive_team_plays > 0:
            defense_play_time_percentage = (defensive_plays / defensive_team_plays) * 100
        else:
            defense_play_time_percentage = 0
        
        entry = {
            "name": game_data["Name"],
            "season": game_data["Season"],
            "game_date": game_data["GameDate"],
            "week": game_data["Week"],
            "team": game_data["Team"],
            "position": game_data["Position"],
            "played": game_data["Played"],
            "started": game_data["Started"],
            "offensive_plays": offensive_plays,
            "defensive_plays": defensive_plays,
            "offensive_team_plays": offensive_team_plays,
            "defensive_team_plays": defensive_team_plays,
            "opponent_rank": game_data["OpponentRank"], 
            "offense_play_time_percentage": offense_play_time_percentage, 
            "defense_play_time_percentage": defense_play_time_percentage
        }
        transformed_data.append(entry)
        
    return transformed_data


def fetch_player_history_data():
    all_data = []

    for selected_year in year_options:
        for week in range(1, 17):
            try:
                full_url = BEGINING_API_URL + selected_year + "/" + str(week) + END_API_URL
                print(f"Gathering player history data for {selected_year} week - {week}")

                response = requests.get(full_url)

                if response.status_code == 200:
                    data = response.json()
                    transformed_data = transform_raw_data(data)
                    all_data.extend(transformed_data) 
                else:
                    print(f"API ERROR for {selected_year} week - {week}: {response.status_code}")
            except requests.Timeout:
                print(f"Request for {selected_year} timed out.")
            except Exception as e:
                print(f"Error for {selected_year}: {str(e)}")

    return all_data

def should_seed_history():
    return db.query(History).count() == 0

def seed_history():
    print("BEGIN PLAYER HISTORY SEEDING")
    print_progress_dots(12)

    existing_records = should_seed_history() 
    
    if existing_records: 
        data = fetch_player_history_data()
        
        if data:
            for history_entry in data:
                player_name = history_entry["name"]
                team_name = history_entry["team"]
                player_in_db = db.query(Player).filter(Player.name == player_name).first()
                club_in_db = db.query(Club).filter(Club.abbrv == team_name).first()
                
                history = History(
                    player_id=player_in_db.id if player_in_db is not None else None,
                    club_id=club_in_db.id if club_in_db is not None else None,
                    name=player_name,
                    season=history_entry.get("season"),
                    game_date=history_entry.get("game_date"),
                    week=history_entry.get("week"),
                    team=team_name,
                    position=history_entry.get("position"),
                    played=history_entry.get("played"),
                    started=history_entry.get("started"),
                    offensive_plays=history_entry.get("offensive_plays"),
                    defensive_plays=history_entry.get("defensive_plays"),
                    offensive_team_plays=history_entry.get("offensive_team_plays"),
                    defensive_team_plays=history_entry.get("defensive_team_plays"),
                    opponent_rank=history_entry.get("opponent_rank"),
                    offense_play_time_percentage=history_entry.get("offense_play_time_percentage"),
                    defense_play_time_percentage=history_entry.get("defense_play_time_percentage"),
                )

                db.add(history)
                db.commit()
            print(f"Player's history data added to the database")
        else:
            print(f"No data for selected year to seed")
    else:
        print(f"History dat already exists in the database.")

if __name__ == "__main__":
    seed_history()