

from database import db
from sqlalchemy import func
from models.models import SeasonAggregation, History
from utils.loaders import print_progress_dots  


def seed_season_ag():
    print("BEGIN SEEDING AGGREGATED SEASON DATA")
    print_progress_dots(12)
    
    subquery = (
        db.query(func.min(History.id).label("min_id")).group_by(History.season, History.club_id).subquery())

    unique_rows_by_season = (db.query(History).join(subquery, History.id == subquery.c.min_id).all())

  
    for history_season_row in unique_rows_by_season:
        season = history_season_row.season 
        
        print('unique', history_season_row.offensive_team_plays )

        total_offensive_team_plays = sum(row.offensive_team_plays or 0 for row in unique_rows_by_season if row.season == season)
        total_defensive_team_plays = sum(row.defensive_team_plays or 0 for row in unique_rows_by_season if row.season == season)

        season_aggregation = SeasonAggregation(
            season=season,
            total_team_plays=total_offensive_team_plays + total_defensive_team_plays,
            total_offensive_team_plays=total_offensive_team_plays,
            total_defensive_team_plays=total_defensive_team_plays
        )

        db.add(season_aggregation)

    db.commit()

if __name__ == "__main__":
    seed_season_ag()