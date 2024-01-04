import sqlite3
from database import engine
from sqlalchemy import text

def run_sql_query_and_print_results_for_club():
    try:
        
        sql_query = """
            WITH top_offense AS (
                SELECT
                    prca.club AS club_name,
                    MAX(prca.offense_plays_percentile) AS max_offensive_percentile
                FROM
                    player_ranking_club_aggregation AS prca
                WHERE
                    prca.offense_plays_percentile IS NOT NULL
                GROUP BY
                    prca.club
            ),
            top_defense AS (
                SELECT
                    prca.club AS club_name,
                    MAX(prca.defense_plays_percentile) AS max_defensive_percentile
                FROM
                    player_ranking_club_aggregation AS prca
                WHERE
                    prca.defense_plays_percentile IS NOT NULL
                GROUP BY
                    prca.club
            )
            SELECT
                tof.club_name,
                pof.name AS top_offensive_player_name,
                tof.max_offensive_percentile AS offensive_percentile,
                pdf.name AS top_defensive_player_name,
                tdf.max_defensive_percentile AS defensive_percentile
            FROM
                top_offense AS tof
            LEFT JOIN
                player_ranking_club_aggregation AS pof
            ON
                tof.club_name = pof.club
                AND tof.max_offensive_percentile = pof.offense_plays_percentile
            LEFT JOIN
                top_defense AS tdf
            ON
                tof.club_name = tdf.club_name
            LEFT JOIN
                player_ranking_club_aggregation AS pdf
            ON
                tdf.club_name = pdf.club
                AND tdf.max_defensive_percentile = pdf.defense_plays_percentile;
        """

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        results = result.fetchall()


        print("------------------------")
        print("TOP PLAYERS BY CLUB")
        print("------------------------")
        print("{:<10} {:<25} {:<25} {:<25} {:<25}".format("Club", "Top Offensive Player", "Offensive Percentile", "Top Defensive Player", "Defensive Percentile"))
        for row in results:
            club_name, top_off_player_name, offensive_percentile, top_def_player_name, defensive_percentile = row
            print("{:<10} {:<25} {:<25} {:<25} {:<25}".format(club_name, top_off_player_name, offensive_percentile, top_def_player_name, defensive_percentile))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_sql_query_and_print_results_for_club()
