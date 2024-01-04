import sqlite3
from database import engine
from sqlalchemy import text

def run_sql_query_and_print_results_for_club():
    try:
        
        sql_query = """
            WITH ranked_offense AS (
                SELECT
                    prca.club,
                    prca.name AS offense_name,
                    prca.offense_plays_percentile,
                    ROW_NUMBER() OVER(PARTITION BY prca.club ORDER BY prca.offense_plays_percentile DESC) AS offense_rank
                FROM
                    player_ranking_aggregations_club AS prca
                WHERE
                    prca.offense_plays_percentile IS NOT NULL
            ),
            ranked_defense AS (
                SELECT
                    prca.club,
                    prca.name AS defense_name,
                    prca.defense_plays_percentile,
                    ROW_NUMBER() OVER(PARTITION BY prca.club ORDER BY prca.defense_plays_percentile DESC) AS defense_rank
                FROM
                    player_ranking_aggregations_club AS prca
                WHERE
                    prca.defense_plays_percentile IS NOT NULL
            )
            SELECT
                ro.club AS club_name,
                ro.offense_name AS top_offensive_performer,
                ro.offense_plays_percentile AS offensive_percentile,
                rd.defense_name AS top_defensive_performer,
                rd.defense_plays_percentile AS defensive_percentile
            FROM
                ranked_offense AS ro
            JOIN
                ranked_defense AS rd
            ON
                ro.club = rd.club
                AND ro.offense_rank = 1
                AND rd.defense_rank = 1;
        """

        # Execute the SQL query using the engine
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        # Fetch all the rows from the result set
        results = result.fetchall()

      # Print the results in a formatted column format
        print("TOP PLAYERS BY CLUB")
        print("{:<10} {:<20} {:<25} {:<25}".format("Season", "Name", "Offensive Percentile", "Defensive Percentile"))
        for row in results:
            season, name, defense_percentile, offense_percentile = row
            print("{:<10} {:<20} {:<25} {:<25}".format(season, name, offense_percentile, defense_percentile))


    except Exception as e:
        print(f"Error: {e}")

# Usage:
if __name__ == "__main__":
    run_sql_query_and_print_results_for_club()
