import sqlite3
from database import engine
from sqlalchemy import text

def run_sql_query_and_print_results_for_season():
    try:
        
        sql_query = """
        SELECT
            season,
            name,
            defense_plays_percentile,
            offense_plays_percentile
        FROM
            (
                SELECT
                    prsa.season,
                    prsa.name,
                    prsa.defense_plays_percentile,
                    prsa.offense_plays_percentile,
                    ROW_NUMBER() OVER(PARTITION BY prsa.season ORDER BY prsa.defense_plays_percentile DESC) AS defense_rank,
                    ROW_NUMBER() OVER(PARTITION BY prsa.season ORDER BY prsa.offense_plays_percentile DESC) AS offense_rank
                FROM
                    player_ranking_aggregations_season AS prsa
                WHERE
                    prsa.defense_plays_percentile IS NOT NULL
                    AND prsa.offense_plays_percentile IS NOT NULL
            ) AS ranked_data
        WHERE
            defense_rank <= 5 OR offense_rank <= 5
        ORDER BY
            season ASC,
            defense_plays_percentile DESC,
            offense_plays_percentile DESC;
        """

        # Execute the SQL query using the engine
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        # Fetch all the rows from the result set
        results = result.fetchall()

      # Print the results in a formatted column format
        print("TOP POSITION PLAYERS BY SEASON")
        print("{:<10} {:<20} {:<25} {:<25}".format("Season", "Name", "Offensive Percentile", "Defensive Percentile"))
        for row in results:
            season, name, defense_percentile, offense_percentile = row
            print("{:<10} {:<20} {:<25} {:<25}".format(season, name, offense_percentile, defense_percentile))


    except Exception as e:
        print(f"Error: {e}")

# Usage:
if __name__ == "__main__":
    run_sql_query_and_print_results_for_season()
