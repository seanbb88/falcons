import requests
from database import SessionLocal
from models import Player, Club, History
from utils.loaders import print_progress_dots
from utils.constants import HISTORY_SEED_URL_BEGINNING, HISTORY_SEED_URL_ENDING


year_options = ["2023", "2022", "2021"]


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
        for week in range(1, 18):
            try:
                full_url = HISTORY_SEED_URL_BEGINNING + selected_year + "/" + str(week) + HISTORY_SEED_URL_ENDING
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


def should_seed_history(session):
    return session.query(History).count() == 0


def seed_history():
    print("BEGIN PLAYER HISTORY SEEDING")
    print_progress_dots(12)

    try:
        with SessionLocal() as session:
            existing_records = should_seed_history(session)

            if existing_records:
                data = fetch_player_history_data()

                if data:
                    for history_entry in data:
                        player_name = history_entry["name"]
                        team_name = history_entry["team"]
                        player_in_db = session.query(Player).filter(Player.name == player_name).first()
                        club_in_db = session.query(Club).filter(Club.abbrv == team_name).first()

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

                        session.add(history)
                    session.commit()
                    print(f"Player's history data added to the database")
                else:
                    print(f"No data for selected year to seed")
            else:
                print(f"History data already exists in the database.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    seed_history()
