
from datetime import datetime
import time
import requests
from database import db 
from models import Transactions, Player, Club
from utils.dates import days_in_month, idx_to_month_str
from utils.loaders import print_progress_dots  
from utils.constants import TRANSACTIONS_SEED_URL_BEGINNING, TRANSACTIONS_SEED_URL_ENDING



year_options = ["2023", "2022", "2021"]

month_options = ['June','July','Aug','Sept']


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


def fetch_player_transaction_data():
    all_data = []  
    for index, _ in enumerate(month_options, start=1):
        total_days = days_in_month(index)
        month_number = idx_to_month_str(index) 
        month_data = [] 
        for day in range(1, total_days + 1): 
            try:
                full_url = TRANSACTIONS_SEED_URL_BEGINNING + month_number + "/" + str(day) + TRANSACTIONS_SEED_URL_ENDING
                
                print(f"Gathering player transaction data for {month_number}/{day}/2023")
                
                response = requests.get(full_url) 
                time.sleep(1)
                if response.status_code == 200:
                    data = response.json()
                    month_data.extend(transform_raw_data(data))  
                else:
                    print(f"API ERROR for {month_number}/{day}/2023: {response.status_code}")
            except requests.Timeout:
                print(f"Request for {month_number}/{day}/2023 timed out.")
            except Exception as e:
                print(f"Error for {month_number}/{day}/2023: {str(e)}")
        
        all_data.extend(month_data) 
    
    return all_data 

def seed_transactions():
    print("BEGIN PLAYER TRANSACTIONS SEEDING")
    print_progress_dots(12)

    existing_records = db.query(Transactions).filter(Transactions.transaction_year == '2023').first()

    if not existing_records:
        data = fetch_player_transaction_data()

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
                    transaction_year='2023'
                )

                db.add(transactions)
                db.commit()
            print(f"Player's transaction data added to the database for 2023")
        else:
            print(f"No data for selected year to seed")
    else:
        print(f"Transactions data for 2023 already exists in the database.")

if __name__ == "__main__":
    seed_transactions()

        