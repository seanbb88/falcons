import requests
from database import SessionLocal
from models import Club
from utils.loaders import print_progress_dots
from utils.constants import CLUB_SEED_URL_SPORTS_IO, CLUB_SEED_URL_SPORTS_RADAR


def fetch_sportsio_club_data():
    try:
        response = requests.get(CLUB_SEED_URL_SPORTS_IO)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API ERROR: {response.status_code}")
            return None
    except Exception as e:
        print(f"API ERROR: {str(e)}")
        return None

def fetch_radar_club_data():
    try:
        nfl_teams = []
        response = requests.get(CLUB_SEED_URL_SPORTS_RADAR)

        if response.status_code == 200:
            data = response.json()

            for conference in data["conferences"]:
                for division in conference["divisions"]:
                    for team in division["teams"]:
                        nfl_teams.append(team)

            return nfl_teams
        else:
            print(f"API ERROR: {response.status_code}")
            return None
    except Exception as e:
        print(f"API ERROR: {str(e)}")
        return None

def check_if_clubs_need_seeded(session):
    seed_clubs = False
    num_teams = session.query(Club).count()

    if num_teams < 32:
        seed_clubs = True
    return seed_clubs

def seed_clubs():
    print("BEGIN CLUBS SEEDING")
    print_progress_dots(12)

    try:
        with SessionLocal() as session:
            should_seed = check_if_clubs_need_seeded(session)
            if should_seed:
                sportsio_data = fetch_sportsio_club_data()
                radar_data = fetch_radar_club_data()
                if sportsio_data and radar_data:
                    for sportsio_club in sportsio_data:
                        club_name = sportsio_club["Name"]
                        radar_club = None

                        for radar_obj in radar_data:
                            if radar_obj["name"] == club_name:
                                radar_club = radar_obj

                        club = Club(
                            name=sportsio_club.get("FullName"),
                            alias=sportsio_club.get("Name"),
                            abbrv=sportsio_club.get("Key"),
                            primary_color=sportsio_club.get("PrimaryColor"),
                            offensive_coordinator=sportsio_club.get("OffensiveCoordinator"),
                            defensive_coordinator=sportsio_club.get("DefensiveCoordinator"),
                            founded=radar_club.get("founded"),
                            owner=radar_club.get("owner"),
                            general_manager=radar_club.get("general_manager"),
                            president=radar_club.get("president"),
                            championships_won=radar_club.get("championships_won"),
                            championship_seasons=radar_club.get("championship_seasons"),
                            conference_titles=radar_club.get("conference_titles"),
                            division_titles=radar_club.get("division_titles"),
                            playoff_appearances=radar_club.get("playoff_appearances"),
                        )

                        session.add(club)

                    session.commit()
                    print("Club data added to database")
                else:
                    print("No data to seed")
            else:
                print("Club data already seeded - skipping seeding")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    seed_clubs()
