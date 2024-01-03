
from datetime import datetime
import time
import requests
from requests.exceptions import Timeout
from database import db 
from models import Transactions, Player, Club
from utils.dates import days_in_month, idx_to_month_str
from utils.loaders import print_progress_dots, print_progress_loader  


BEGINING_API_URL = "http://api.sportradar.us/nfl/official/trial/v7/en/league/"
END_API_URL = "/transactions.json?api_key=36xtbwcx8p72eatag793d75v"

year_options = ["2023", "2022", "2021", "2020"]

month_options = ['May','June','July','Aug','Sept']



def display_year_menu():
    print("Please select an input number corresponding to the year in which to seed player transactions")
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
    
    for player in raw_data.get('players', []):
        for transaction in player.get('transactions', []):
            
            transaction_info = {
                "name": player['name'],
                "position": player['position'],
                "description": transaction['desc'],
                "from_club": transaction['from_team']['name'] if 'from_team' in transaction else 'N/A',
                "to_club": transaction['to_team']['name'] if 'to_team' in transaction else 'N/A', 
                'effective_date': transaction['effective_date'],
                'transaction_type': transaction['transaction_type'],
                'transaction_year': transaction['transaction_year']
            }
            transformed_data.append(transaction_info)  
        
    return transformed_data


def fetch_player_transaction_data(selected_year):
    all_data = []  
    for index, _ in enumerate(month_options, start=1):
        total_days = days_in_month(index)
        month_number = idx_to_month_str(index) 
        month_data = [] 
        for day in range(1, total_days + 1): 
            try:
                full_url = BEGINING_API_URL + selected_year + "/" + month_number + "/" + str(day) + END_API_URL
                
                print(f"Gathering player transaction data for {month_number}/{day}/{selected_year}")
                
                response = requests.get(full_url) 
                time.sleep(1)
                if response.status_code == 200:
                    data = response.json()
                    month_data.extend(transform_raw_data(data))  
                else:
                    print(f"API ERROR for {month_number}/{day}/{selected_year}: {response.status_code}")
            except requests.Timeout:
                print(f"Request for {month_number}/{day}/{selected_year} timed out.")
            except Exception as e:
                print(f"Error for {month_number}/{day}/{selected_year}: {str(e)}")
        
        all_data.extend(month_data) 
    
    return all_data 

def seed_transactions():
    print("BEGIN PLAYER TRANSACTIONS SEEDING")
    print_progress_dots(12)
    selected_year = select_timeframe()

    existing_records = db.query(Transactions).filter(Transactions.transaction_year == selected_year).first()

    if not existing_records:
        data = fetch_player_transaction_data(selected_year)

        if data:
            for transaction in data:
                from_club = transaction["from_club"]
                to_club = transaction["to_club"]
                player_in_db = db.query(Player).filter(Player.name == transaction.get("name")).first()
                sending_club = db.query(Club).filter(Club.alias == from_club).first()
                receiving_club = db.query(Club).filter(Club.alias == to_club).first()

                transactions = Transactions(
                    name=transaction.get("name"),
                    player_id=player_in_db.id if player_in_db is not None else None,
                    type=transaction.get("transaction_type"),
                    date=transaction.get("effective_date"),
                    position=transaction.get("position"),
                    description=transaction.get("description"),
                    sending_club_id=sending_club.id if sending_club is not None else None,
                    receiving_club_id=receiving_club.id if receiving_club is not None else None,
                    transaction_year=selected_year
                )

                db.add(transactions)
                print_progress_loader()
                db.commit()
            print(f"Player's transaction data added to the database for {selected_year}")
        else:
            print(f"No data for selected year to seed")
    else:
        print(f"Transactions data for {selected_year} already exists in the database.")

if __name__ == "__main__":
    seed_transactions()

        