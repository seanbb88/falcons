

from database import db
from sqlalchemy import func
from models.models import SeasonAggregation, History
from utils.loaders import print_progress_dots


def flatten_unique_season_data():
    all_data = []

    db.query(History).all()
    
    subquery = (
    db.query(func.min(History.id).label("min_id")).group_by(History.season, History.club_id, History.week).subquery())

    unique_rows_by_season = (db.query(History).join(subquery, History.id == subquery.c.min_id).all())
  
    for history_season_row in unique_rows_by_season:
        season = history_season_row.season 
        club = history_season_row.team 
        
        flettened_history = History(
            season=season,
            team=club,
            offensive_team_plays=history_season_row.offensive_team_plays,
            defensive_team_plays=history_season_row.defensive_team_plays
        )
        all_data.append(flettened_history)
    return all_data

def calculate_season_totals(data):
    if data is None or len(data) == 0:
        return {}

    season_totals = {}

    for entry in data:
        season = entry.season
        offensive_team_plays = entry.offensive_team_plays
        defensive_team_plays = entry.defensive_team_plays

        if season in season_totals:
            season_totals[season]['offensive_team_plays'] += offensive_team_plays
            season_totals[season]['defensive_team_plays'] += defensive_team_plays
        else:
            season_totals[season] = {
                'offensive_team_plays': offensive_team_plays,
                'defensive_team_plays': defensive_team_plays
            }

    return season_totals

def add_season_aggregations(data):
    for season, stats in data.items():
        offensive_team_plays = stats['offensive_team_plays']
        defensive_team_plays = stats['defensive_team_plays']
        total_team_plays = offensive_team_plays + defensive_team_plays
        
        season_aggregation = SeasonAggregation(
            season=season,
            total_offensive_team_plays=offensive_team_plays,
            total_defensive_team_plays=defensive_team_plays,
            total_team_plays=total_team_plays
        )

        db.add(season_aggregation)

    db.commit()
    
def has_existing_season_aggregations():
    return db.query(SeasonAggregation).count() > 0

def seed_season_ag():
    print("BEGIN SEEDING AGGREGATED SEASON DATA")
    print_progress_dots(12)

    if has_existing_season_aggregations():
        print("Existing data found for season aggregations. Skipping seeding.")
        return

    flattened_data = flatten_unique_season_data()

    if flattened_data:
        season_totals_data = calculate_season_totals(flattened_data)
        
        if season_totals_data:
            add_season_aggregations(season_totals_data)

    else:
        print("No data to seed.")

if __name__ == "__main__":
    seed_season_ag()