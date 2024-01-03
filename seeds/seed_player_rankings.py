from database import db
from sqlalchemy import func
from models.models import PlayerRankingAggregation, History
from utils.loaders import print_progress_dots

def player_by_season_query():
    column_name = 'season' 
    query = (
        db.query(
            History.player_id,
            History.season,
            History.name,
            func.sum(History.offensive_plays).label("total_sum_offense"),
            func.sum(History.defensive_plays).label("total_sum_defense")
        )
        .group_by(History.player_id, History.season, History.name)
    )

    results = query.all()
    return perform_calculations_and_update(results, column_name)

def player_by_position_query(): 
    column_name = 'position' 
    query = (
        db.query(
            History.player_id,
            History.position,
            History.name,
            func.sum(History.offensive_plays).label("total_sum_offense"),
            func.sum(History.defensive_plays).label("total_sum_defense")
        )
        .group_by(History.player_id, History.position, History.name)
    )

    results = query.all()
    return perform_calculations_and_update(results, column_name)

def player_by_club_query(): 
    column_name = 'team' 
    query = (
        db.query(
            History.player_id,
            History.team,
            History.name,
            func.sum(History.offensive_plays).label("total_sum_offense"),
            func.sum(History.defensive_plays).label("total_sum_defense")
        )
        .group_by(History.player_id, History.team, History.name)
    )

    results = query.all()
    return perform_calculations_and_update(results)

def perform_calculations_and_update(player_data, column_name):
    if column_name == 'season':
        
        pass
    elif column_name == 'position':
        
        pass
    elif column_name == 'team':
       
        pass
    else:
        pass

    return
def perform_season_rankings():
    all_data = []

    player_by_season_query()
    player_by_club_query()
    player_by_position_query()
    # total_plays_dict = calculate_total_plays_by_player_season(data)

    # Now you have the total plays for each player and season in total_plays_dict
    # You can use this data to perform your rankings or other aggregations

    return all_data

# ... (rest of your code) ...


def perform_club_rankings():
    all_data = []

    return all_data

def perform_position_rankings():
    all_data = []

    return all_data



def has_existing_player_ranking_aggregations():
    return db.query(PlayerRankingAggregation).count() > 0

def seed_player_rankings_ag():
    print("BEGIN SEEDING AGGREGATED PLAYER RANKING DATA")
    print_progress_dots(12)

    if has_existing_player_ranking_aggregations():
        print("Existing data found for player ranking aggregations. Skipping seeding.")
        return
    
    perform_season_rankings()



if __name__ == "__main__":
    seed_player_rankings_ag()
