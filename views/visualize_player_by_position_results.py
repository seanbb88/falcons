import sqlite3
from database import engine
from sqlalchemy import text

def run_sql_query_and_print_results_for_position():
    try:
        sql_query = """
            WITH top_percentiles AS (
                SELECT
                    name AS player_name,
                    player_id,
                    position,
                    offense_plays_percentile AS play_percentile
                FROM
                    player_ranking_position_aggregation
                WHERE
                    offense_plays_percentile IS NOT NULL
                UNION ALL
                SELECT
                    name AS player_name,
                    player_id,
                    position,
                    defense_plays_percentile AS play_percentile
                FROM
                    player_ranking_position_aggregation
                WHERE
                    defense_plays_percentile IS NOT NULL
            )
            SELECT
                player_name,
                play_percentile,
                player_id,
                position
            FROM
                top_percentiles
            ORDER BY
                play_percentile DESC
            LIMIT 100
        """

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        results = result.fetchall()
        
        print("--------------------------------------")
        print("TOP 100 PLAYERS BY PERCENTILE/POSITION")
        print("--------------------------------------")
        print("{:<25} {:<10} {:<25} {:<15}".format("Player Name", "Player ID", "Play Percentile", "Position"))
        for row in results:
            player_name, play_percentile, player_id, position = row
            print("{:<25} {:<10} {:<25} {:<15}".format(player_name, player_id, play_percentile, position))

        print("------------------------------------------------------------------")
        print("------------------------------------------------------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_sql_query_and_print_results_for_position()
