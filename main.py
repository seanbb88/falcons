


from database import initialize_database
from seeds.seed_clubs import seed_clubs
from seeds.seed_history import seed_history
from seeds.seed_players import seed_players
from seeds.seed_transactions import seed_transactions


def main():
    initialize_database()
    seed_clubs()
    seed_players()
    seed_transactions()
    seed_history()

if __name__ == "__main__":
    main()