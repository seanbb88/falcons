import sqlite3
from database import engine
from sqlalchemy import text

def run_sql_query_and_print_results_for_salary():
    try:
        
        sql_query = """
            WITH RankedSalaries AS (
                SELECT
                    ps.year_signed,
                    ps.average_per_year,
                    p.name,
                    ps.team, 
                    ps.position, 
                    ROW_NUMBER() OVER (PARTITION BY ps.year_signed ORDER BY ps.average_per_year DESC) AS rn
                FROM
                    player_salary ps
                LEFT JOIN
                    players p ON ps.player_id = p.id 
                WHERE
                    ps.player_id IS NOT NULL  -- Filter out rows with NULL player_id
            )
            SELECT
                year_signed,
                average_per_year, 
                name, 
                team, 
                position
            FROM
                RankedSalaries
            WHERE
                rn = 1;
        """

        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        results = result.fetchall()

        print("------------------------")
        print("TOP AVERAGE PER YEAR BY YEAR")
        print("------------------------")
        print("{:<10} {:<20} {:<25} {:<20} {:<20}".format("Season", "Player Name", "Average Per Year", "Team", "Position"))

        for row in results:
            season, average_per_year, name, team, position = row
            print("{:<10} {:<20} {:<25} {:<20} {:<20}".format(season, name, average_per_year, team, position))


    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_sql_query_and_print_results_for_salary()
