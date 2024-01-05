import sqlite3
from database import engine
from sqlalchemy import text

def run_sql_query_and_print_results_for_season():
    try:
        
        sql_query = """
        SELECT
            season,
            name,
            play_percentile
        FROM
            (
                SELECT
                    prsa.season,
                    prsa.name,
                    COALESCE(prsa.defense_plays_percentile, prsa.offense_plays_percentile) AS play_percentile,
                    ROW_NUMBER() OVER(PARTITION BY prsa.season ORDER BY COALESCE(prsa.defense_plays_percentile, prsa.offense_plays_percentile) DESC) AS play_rank
                FROM
                    player_ranking_season_aggregation AS prsa
                WHERE
                    COALESCE(prsa.defense_plays_percentile, prsa.offense_plays_percentile) IS NOT NULL
            ) AS ranked_data
        WHERE
            play_rank <= 25
        ORDER BY
            season ASC,
            play_percentile DESC;
        """

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        results = result.fetchall()

        print("------------------------")
        print("TOP 25 PLAYERS BY PERCENTILE PER SEASON (2021-2023)")
        print("------------------------")
        print("{:<10} {:<20} {:<25}".format("Season", "Name", "Play Percentile"))
        for row in results:
            season, name, play_percentile = row
            print("{:<10} {:<20} {:<25}".format(season, name, play_percentile))

        print("------------------------------------------------------------------")
        print("------------------------------------------------------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_sql_query_and_print_results_for_season()
