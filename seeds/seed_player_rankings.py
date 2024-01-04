from database import db
from sqlalchemy import func
from models.models import History, PlayerRankingClubAggregation, PlayerRankingPositionAggregation, PlayerRankingSeasonAggregation
from utils.loaders import print_progress_dots

def calculate_percentile(data, value):
    sorted_data = sorted(x for x in data if x is not None)

    if not sorted_data:
        return None  # Handle the case when all values are None
    
    if value is None:
        return None  # Handle the case when the target value is None
    
    position = 0
    for i, x in enumerate(sorted_data):
        if x is not None and x >= value:
            position = i
            break

    percentile = (position / (len(sorted_data) - 1)) * 100

    return percentile

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
    return perform_calculations_and_update(results, column_name)

def perform_calculations_and_update(player_data, column_name):
    offensive_plays_array = [result.total_sum_offense for result in player_data]
    defensive_plays_array = [result.total_sum_defense for result in player_data]
    

    if column_name == 'season':
        # Handle updates based on season
        for result in player_data:
            player_id = result.player_id
            player_name = result.name, 
            season = result.season
            off_percentile = calculate_percentile(offensive_plays_array, result.total_sum_offense)
            def_percentile = calculate_percentile(defensive_plays_array, result.total_sum_offense)
            
            player_ranking_aggregation = db.query(PlayerRankingSeasonAggregation).filter_by(player_id=player_id, season=season).first()
            
            if player_ranking_aggregation:
                # If a record exists, update it
                db.query(PlayerRankingSeasonAggregation).filter_by(player_id=player_id, season=season).update({
                    PlayerRankingSeasonAggregation.offense_plays_percentile: off_percentile,
                    PlayerRankingSeasonAggregation.defense_plays_percentile: def_percentile
                })
            else:
                new_player_ranking_aggregation = PlayerRankingSeasonAggregation(
                    player_id=player_id,
                    name=player_name,
                    season=season,
                    offense_plays_percentile=off_percentile,
                    defense_plays_percentile=def_percentile
                )
                db.add(new_player_ranking_aggregation)

    elif column_name == 'position':
        for result in player_data:
            player_id = result.player_id
            player_name = result.name
            position = result.position
            off_percentile = calculate_percentile(offensive_plays_array, result.total_sum_offense)
            def_percentile = calculate_percentile(defensive_plays_array, result.total_sum_offense)
            
    
            player_ranking_aggregation = db.query(PlayerRankingPositionAggregation).filter_by(player_id=player_id).first()
            
            if player_ranking_aggregation:
                db.query(PlayerRankingPositionAggregation).filter_by(player_id=player_id, position=position).update({
                    PlayerRankingPositionAggregation.offense_plays_percentile: off_percentile,
                    PlayerRankingPositionAggregation.defense_plays_percentile: def_percentile
                })
            else:
                new_player_ranking_aggregation = PlayerRankingPositionAggregation(
                    player_id=player_id,
                    name=player_name, 
                    position=position,
                    offense_plays_percentile=off_percentile,
                    defense_plays_percentile=def_percentile
                )
                db.add(new_player_ranking_aggregation)

    elif column_name == 'team':
        for result in player_data:
            player_id = result.player_id
            player_name = result.name, 
            club = result.team,
            off_percentile = calculate_percentile(offensive_plays_array, result.total_sum_offense)
            def_percentile = calculate_percentile(defensive_plays_array, result.total_sum_offense)
            
            player_ranking_aggregation = db.query(PlayerRankingClubAggregation).filter_by(player_id=player_id, club=club).first()
            
            if player_ranking_aggregation:
                db.query(PlayerRankingClubAggregation).filter_by(player_id=player_id).update({
                    PlayerRankingClubAggregation.offense_plays_percentile: off_percentile,
                    PlayerRankingClubAggregation.defense_plays_percentile: def_percentile
                })
            else:
                new_player_ranking_aggregation = PlayerRankingClubAggregation(
                    player_id=player_id,
                    club=club,
                    name=player_name,
                    offense_plays_percentile=off_percentile,
                    defense_plays_percentile=def_percentile
                )
                db.add(new_player_ranking_aggregation)

    else:
        pass

    db.commit()
    
def has_existing_season_aggregations():
    return db.query(PlayerRankingSeasonAggregation).count() > 0

def perform_player_rankings():
    if has_existing_season_aggregations():
        print("Existing data found. You can skip to results.")
        skip_to_results = input("Skip to results? (Answer y or n): ").strip().lower()

        if skip_to_results != 'y':
            player_by_season_query()
            player_by_club_query()
            player_by_position_query()
        else:
            return 




def seed_player_rankings_ag():
    print("BEGIN SEEDING AGGREGATED PLAYER RANKING DATA")
    print_progress_dots(12)
    perform_player_rankings()


if __name__ == "__main__":
    seed_player_rankings_ag()
