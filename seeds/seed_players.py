import requests
from database import SessionLocal
from models import Club, Player
from utils.loaders import print_progress_dots
from utils.constants import PLAYER_SEED_URL_BEGINNING, PLAYER_SEED_URL_ENDING


def fetch_sportsio_player_data(team_abbrv):
    try:
        full_url = PLAYER_SEED_URL_BEGINNING + team_abbrv + PLAYER_SEED_URL_ENDING
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

def maybe_add_player(session, player_data, club_id):
    existing_player = session.query(Player).filter(
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

        session.add(player)

def should_seed(session):
    return session.query(Player).first() is None

def seed_players():
    print("BEGIN PLAYERS SEEDING")
    print_progress_dots(12)

    try:
        with SessionLocal() as session:
            if should_seed(session):
                club_data = session.query(Club).all()
                if club_data:
                    for club in club_data:
                        team_abbrv = club.abbrv
                        club_name = club.name
                        club_id = club.id
                        data = fetch_sportsio_player_data(team_abbrv)

                        if data:
                            for player_data in data:
                                maybe_add_player(session, player_data, club_id)

                            session.commit()
                            print(f"Players data added to database for {club_name}")

                    print("All player positions have been seeded. Exiting.")
                else:
                    print("No data to seed")
            else:
                print("Players data already exists in the database. Skipping seeding.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    seed_players()
