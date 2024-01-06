from database import db
from sqlalchemy import func
from models.models import PositionAggregation, History
from utils.loaders import print_progress_dots


def flatten_unique_position_data():
    all_data = []
    
    subquery = (
        db.query(func.min(History.id).label("min_id")).group_by(History.position, History.week).subquery())

    unique_rows_by_position = (
        db.query(History).join(subquery, History.id == subquery.c.min_id).all())

    for history_position_row in unique_rows_by_position:
        position = history_position_row.position
        club = history_position_row.team

        flattened_history = History(
            position=position,
            team=club,
            offensive_team_plays=history_position_row.offensive_team_plays,
            defensive_team_plays=history_position_row.defensive_team_plays
        )
        all_data.append(flattened_history)
    return all_data

def calculate_position_totals(data):
    if data is None or len(data) == 0:
        return {}

    position_totals = {}

    for entry in data:
        position = entry.position
        offensive_team_plays = entry.offensive_team_plays
        defensive_team_plays = entry.defensive_team_plays

        if position:
            if position in position_totals:
                if offensive_team_plays:
                    position_totals[position]['offensive_team_plays'] += offensive_team_plays
                if defensive_team_plays:
                    position_totals[position]['defensive_team_plays'] += defensive_team_plays
            else:
                position_totals[position] = {
                    'offensive_team_plays': offensive_team_plays or 0,
                    'defensive_team_plays': defensive_team_plays or 0
                }

    return position_totals

def add_position_aggregations(data):
    for position, stats in data.items():
        offensive_team_plays = stats['offensive_team_plays']
        defensive_team_plays = stats['defensive_team_plays']
        total_team_plays = offensive_team_plays + defensive_team_plays

        position_aggregation = PositionAggregation(
            position=position,
            total_offensive_team_plays=offensive_team_plays,
            total_defensive_team_plays=defensive_team_plays,
            total_team_plays=total_team_plays
        )

        db.add(position_aggregation)

    db.commit()

def has_existing_position_aggregations():
    return db.query(PositionAggregation).count() > 0

def seed_position_ag():
    print("BEGIN SEEDING AGGREGATED POSITION DATA")
    print_progress_dots(12)

    if has_existing_position_aggregations():
        print("Existing data found for position aggregations. Skipping seeding.")
        return

    flattened_data = flatten_unique_position_data()

    if flattened_data:
        position_totals_data = calculate_position_totals(flattened_data)

        if position_totals_data:
            add_position_aggregations(position_totals_data)

    else:
        print("No data to seed.")

if __name__ == "__main__":
    seed_position_ag()
