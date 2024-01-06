SPORTS_IO_API_KEY = "21741b49743544a3abce2c126423ba55"
SPORTS_RADAR_API_KEY = "xbz8caeccxd5wwdrsyt5mt8q"

PLAYER_SEED_URL_BEGINNING = "https://api.sportsdata.io/v3/nfl/scores/json/PlayersBasic/"
PLAYER_SEED_URL_ENDING = f"?key={SPORTS_IO_API_KEY}"

CLUB_SEED_URL_SPORTS_IO =  f"https://api.sportsdata.io/v3/nfl/scores/json/TeamsBasic?key={SPORTS_IO_API_KEY}"
CLUB_SEED_URL_SPORTS_RADAR = f"http://api.sportradar.us/nfl/official/trial/v7/en/league/hierarchy.json?api_key={SPORTS_RADAR_API_KEY}"

TRANSACTIONS_SEED_URL_BEGINNING =  "http://api.sportradar.us/nfl/official/trial/v7/en/league/2023/"
TRANSACTIONS_SEED_URL_ENDING = f"/transactions.json?api_key={SPORTS_RADAR_API_KEY}"

HISTORY_SEED_URL_BEGINNING = "https://api.sportsdata.io/v3/nfl/stats/json/PlayerGameStatsByWeek/"
HISTORY_SEED_URL_ENDING = f"?key={SPORTS_IO_API_KEY}"
