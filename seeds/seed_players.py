
import requests
from database import db  
from models import Club, Player
from utils.loaders import print_progress_dots  


SPORTS_API_URL = "https://api.sportsdata.io/v3/nfl/scores/json/PlayersBasic/"
SPORTS_API_KEY = "?key=d8032d128b1a47c9bf299f8061bb41a9"


def fetch_sportsio_player_data(team_abbrv):
    try:
        full_url = SPORTS_API_URL + team_abbrv + SPORTS_API_KEY
        response = requests.get(full_url)

        if response.status_code == 200:
            data = response.json()
            
            return data
        else:
            print(f"API ERROR: {response.status_code}")
            return None
    except Exception as e:
        print(f"API ERROR: {str(e)}")
        return None

    
def maybe_add_player(player_data, club_id):
    existing_player = db.query(Player).filter(
        Player.name == player_data.get("Name"),
        Player.weight == player_data.get("Weight"),
        Player.height == player_data.get("Height"),
        Player.age == player_data.get("Age")
    ).first()
    
    if not existing_player:
        player = Player(
            name=player_data.get("Name"),
            active_club_id=club_id,
            last_name=player_data.get("LastName"),
            first_name=player_data.get("FirstName"),
            birth_date=player_data.get("BirthDate"),
            weight=player_data.get("Weight"),
            height=player_data.get("Height"),
            experience=player_data.get("Experience"),
            age=player_data.get("Age"),
            college=player_data.get("College"),
            position=player_data.get("Position"),
            status=player_data.get("Status"),
            headshot_url=player_data.get("UsaTodayHeadshotUrl"),
        )
        
        db.add(player)

def should_seed():
    return db.query(Player).first() is None

def seed_players():
    print("BEGIN PLAYERS SEEDING")
    print_progress_dots(12)
    
    if should_seed():
        club_data = db.query(Club).all()  
        if club_data:
            for club in club_data:
                team_abbrv = club.abbrv
                club_name = club.name
                club_id = club.id
                data = fetch_sportsio_player_data(team_abbrv)
                
                if data:
                    for player_data in data:
                        maybe_add_player(player_data, club_id)
                    
                    db.commit()
                    print(f"Players data added to database for the {club_name}")
            
            print("All player positions have been seeded. Exiting.")
        else:
            print("No data to seed")
    else:
        print("Players data already exists in the database. Skipping seeding.")

if __name__ == "__main__":
    seed_players()