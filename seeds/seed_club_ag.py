

from database import db
from models.models import Club, ClubAggregation, History
from utils.loaders import print_progress_dots 


def has_existing_club_aggregations():
    return db.query(ClubAggregation).count() > 0 


def seed_club_ag():
    print("BEGIN SEEDING AGGREGATED CLUB DATA")
    print_progress_dots(12)
    
    if has_existing_club_aggregations():
        print("Existing data found for club aggregations. Skipping seeding.")
        return
    
    clubs = db.query(Club).all()
    unique_rows = db.query(History).distinct(History.club_id, History.season, History.week).all()

  
    for club in clubs:
        club_name = club.name 

        total_offensive_team_plays = sum(row.offensive_team_plays or 0 for row in unique_rows if row.team == club.abbrv)
        total_defensive_team_plays = sum(row.defensive_team_plays or 0 for row in unique_rows if row.team == club.abbrv)

        club_aggregation = ClubAggregation(
            club_name=club_name,
            total_team_plays=total_offensive_team_plays + total_defensive_team_plays,
            total_offensive_team_plays=total_offensive_team_plays,
            total_defensive_team_plays=total_defensive_team_plays
        )

        db.add(club_aggregation)

    db.commit()

if __name__ == "__main__":
    seed_club_ag()