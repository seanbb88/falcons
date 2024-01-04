


from database import initialize_database
from seeds.seed_club_ag import seed_club_ag
from seeds.seed_player_rankings import seed_player_rankings_ag
from seeds.seed_position_ag import seed_position_ag
from seeds.seed_season_ag import seed_season_ag
from seeds.seed_clubs import seed_clubs
from seeds.seed_history import seed_history
from seeds.seed_players import seed_players
from seeds.seed_transactions import seed_transactions
from views.visualize_player_by_season_results import run_sql_query_and_print_results_for_season


def main():
    initialize_database()
    seed_clubs()
    seed_players()
    seed_transactions()
    seed_history()
    seed_club_ag()
    seed_season_ag()
    seed_position_ag()
    seed_player_rankings_ag()
    run_sql_query_and_print_results_for_season()

if __name__ == "__main__":
    main()