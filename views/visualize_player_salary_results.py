import sqlite3
from database import engine
from sqlalchemy import text


def run_sql_query_and_print_results_for_players_compared_to_total_values(total_values):
    try: 
        sql_query = """
            SELECT
                ps.year_signed,
                ps.total_value,
                p.name AS player_name
            FROM
                player_salary ps
            LEFT JOIN
                players p ON ps.player_id = p.id
            WHERE
                ps.player_id IS NOT NULL
            ORDER BY
                ps.total_value DESC
            LIMIT
                250;
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))

        results = result.fetchall()
        
        print("------------------------------------------------------------------------------------------------------------------------")
        print("TOTAL VALUE PERCENTAGES - (top 250 players total value percentages compared to the top, middle, and lower paid players)")
        print("------------------------------------------------------------------------------------------------------------------------")
        print("{:<10} {:<20} {:<15} {:<20} {:<20} {:<20}".format("Season", "Player Name", "Total Value", "Percentage/bottom", "Percentage/middle", "Percentage/top"))

        for row in results:
            year_signed, total_value, name = row
      
            # Calculate percentages here
            percentage_from_bottom = ((total_value - total_values[0][1]) / total_values[0][1]) * 100
            percentage_from_median = ((total_value - total_values[1][1]) / total_values[1][1]) * 100
            percentage_from_top = ((total_value - total_values[2][1]) / total_values[2][1]) * 100
            print("{:<10} {:<20} {:<15} {:<20}% {:<20}% {:<20}%".format(year_signed, name, total_value,
                                                                                 percentage_from_bottom,
                                                                                 percentage_from_median,
                                                                                 percentage_from_top))
            
    except Exception as e:
        print(f"Error: {e}")
        
def run_sql_query_and_print_results_for_salary_by_year():
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
                    ps.player_id IS NOT NULL
                    AND ps.year_signed != '0'  -- Use single quotes for string comparison
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

        print("-------------------------------------")
        print("TOP AVERAGE PER YEAR SALARY BY YEAR")
        print("-------------------------------------")
        print("{:<10} {:<20} {:<25} {:<20} {:<20}".format("Season", "Player Name", "Average Per Year", "Club", "Position"))

        for row in results:
            season, average_per_year, name, team, position = row
            print("{:<10} {:<20} {:<25} {:<20} {:<20}".format(season, name, average_per_year, team, position))

        print("------------------------------------------------------------------")
        print("------------------------------------------------------------------")
    except Exception as e:
        print(f"Error: {e}")
        
def run_sql_query_and_print_results_for_salary_by_club():
    try:
        
        sql_query = """
            WITH RankedSalaries AS (
                SELECT
                    ps.year_signed,
                    ps.average_per_year,
                    p.name,
                    ps.team, 
                    ps.position, 
                    ROW_NUMBER() OVER (PARTITION BY ps.team ORDER BY ps.average_per_year DESC) AS rn
                FROM
                    player_salary ps
                LEFT JOIN
                    players p ON ps.player_id = p.id 
                WHERE
                    ps.player_id IS NOT NULL
                        AND ps.year_signed IN ('2020', '2021', '2022', '2023')
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

        print("------------------------------------------------")
        print("TOP AVERAGE PER YEAR SALARY BY CLUB (2020-2023)")
        print("------------------------------------------------")
        print("{:<15} {:<25} {:<25} {:<10} {:<20}".format("Club", "Player Name", "Average Per Year", "Season", "Position"))

        for row in results:
            season, average_per_year, name, team, position = row
            print("{:<15} {:<25} {:<25} {:<10} {:<20}".format(team, name, average_per_year, season, position))

        print("------------------------------------------------------------------")
        print("------------------------------------------------------------------")
    except Exception as e:
        print(f"Error: {e}")
        
def run_sql_query_for_total_value():
    try: 
        sql_query_total_values = """
            WITH TotalValues AS (
                SELECT
                    PERCENTILE_DISC(0) WITHIN GROUP (ORDER BY total_value) AS bottom,
                    PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY total_value) AS median,
                    PERCENTILE_DISC(1) WITHIN GROUP (ORDER BY total_value) AS top
                FROM
                    player_salary
                WHERE
                    total_value != 0
                    AND player_id IS NOT NULL
            )
            SELECT 'bottom' AS status, bottom AS total_value
            FROM TotalValues
            UNION ALL
            SELECT 'median' AS status, median AS total_value
            FROM TotalValues
            UNION ALL
            SELECT 'top' AS status, top AS total_value
            FROM TotalValues;
        """ 

        with engine.connect() as connection:
            result = connection.execute(text(sql_query_total_values))

        total_values = result.fetchall()
    
        run_sql_query_and_print_results_for_players_compared_to_total_values(total_values)
    
    except Exception as e:
        print(f"Error: {e}")
    
        
def run_salary_queries():
    run_sql_query_and_print_results_for_salary_by_year()
    run_sql_query_and_print_results_for_salary_by_club()
    run_sql_query_for_total_value()

if __name__ == "__main__":
    run_salary_queries()
