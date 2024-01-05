SPORTS_IO_API_KEY = "6f1ce3bc195a49ddae34cb0ff638b63c"
SPORTS_RADAR_API_KEY = "shjkk5b842b28jncxxm9dp55"

PLAYER_SEED_URL_BEGINNING = "https://api.sportsdata.io/v3/nfl/scores/json/PlayersBasic/"
PLAYER_SEED_URL_ENDING = f"?key={SPORTS_IO_API_KEY}"

CLUB_SEED_URL_SPORTS_IO =  f"https://api.sportsdata.io/v3/nfl/scores/json/TeamsBasic?key={SPORTS_IO_API_KEY}"
CLUB_SEED_URL_SPORTS_RADAR = f"http://api.sportradar.us/nfl/official/trial/v7/en/league/hierarchy.json?api_key={SPORTS_RADAR_API_KEY}"

TRANSACTIONS_SEED_URL_BEGINNING =  "http://api.sportradar.us/nfl/official/trial/v7/en/league/2023/"
TRANSACTIONS_SEED_URL_ENDING = f"/transactions.json?api_key={SPORTS_RADAR_API_KEY}"

HISTORY_SEED_URL_BEGINNING = "https://api.sportsdata.io/v3/nfl/stats/json/PlayerGameStatsByWeek/"
HISTORY_SEED_URL_ENDING = f"?key={SPORTS_IO_API_KEY}"
