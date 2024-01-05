# Database Schema Documentation
## Tables


### Table 1: `clubs`
| Column Name              | Data Type   | Nullable | Description                             |
|--------------------------|-------------|----------|-----------------------------------------|
| id                       | Integer     | No       | Primary key                             |
| name                     | String      | No       | Unique club name                        |
| alias                    | String      | Yes      | Club alias                              |
| abbrv                    | String      | Yes      | Abbreviation                            |
| founded                  | Integer     | Yes      | Year founded                            |
| owner                    | String      | Yes      | Owner's name                            |
| general_manager          | String      | Yes      | General manager's name                  |
| president                | String      | Yes      | President's name                        |
| primary_color            | String      | Yes      | Primary team color                      |
| offensive_coordinator    | String      | Yes      | Offensive coordinator's name            |
| defensive_coordinator    | String      | Yes      | Defensive coordinator's name            |
| championships_won        | Integer     | Yes      | Number of championships won             |
| championship_seasons     | String      | Yes      | Seasons of championships                |
| conference_titles        | Integer     | Yes      | Number of conference titles             |
| division_titles          | Integer     | Yes      | Number of division titles               |
| playoff_appearances      | Integer     | Yes      | Number of playoff appearances           |
| created_at               | DateTime    | No       | Timestamp of creation                   |
| updated_at               | DateTime    | Yes      | Timestamp of last update                |


### Table 2: `players`
| Column Name      | Data Type   | Nullable | Description                           |
|------------------|-------------|----------|---------------------------------------|
| id               | Integer     | No       | Primary key                           |
| active_club_id   | Integer     | Yes      | Foreign key to active club            |
| name             | String      | Yes      | Player name                           |
| last_name        | String      | Yes      | Player's last name                    |
| first_name       | String      | Yes      | Player's first name                   |
| birth_date       | DateTime    | Yes      | Player's birth date                   |
| college          | String      | Yes      | College attended                      |
| experience       | Integer     | Yes      | Years of experience                   |
| age              | Integer     | Yes      | Player's age                          |
| weight           | Integer     | Yes      | Player's weight                       |
| height           | String      | Yes      | Player's height                       |
| position         | String      | Yes      | Player's position                     |
| status           | String      | Yes      | Player's status                       |
| headshot_url     | String      | Yes      | URL of player's headshot              |
| created_at       | DateTime    | No       | Timestamp of creation                 |
| updated_at       | DateTime    | Yes      | Timestamp of last update              |
- **Relationships:**
  - `active_team`: Relationship with `clubs`

### Table 3: `player_history`
| Column Name                  | Data Type   | Nullable | Description                               |
|--------------------------    |-------------|----------|-------------------------------------------|
| id                           | Integer     | No       | Primary key                               |
| player_id                    | Integer     | No       | Foreign key to players                    |
| name                         | String      | Yes      | Player name                               |
| season                       | String      | Yes      | Season name                               |
| club_id                      | Integer     | No       | Foreign key to clubs                      |
| started                      | Boolean     |          | Indicates if the player started           |
| played                       | Boolean     |          | Indicates if the player played            |
| position                     | String      | Yes      | Player's position                         |
| team                         | String      | Yes      | Team name                                 |
| opponent_rank                | String      | Yes      | Opponent's rank                           |
| offensive_plays              | Integer     | Yes      | Number of offensive plays                 |
| defensive_plays              | Integer     | Yes      | Number of defensive plays                 |
| offensive_team_plays         | Integer     | Yes      | Number of offensive team plays            |
| defensive_team_plays         | Integer     | Yes      | Number of defensive team plays            |
| offense_play_time_percentage | Float       | Yes      | Offensive play time percentage            |
| defense_play_time_percentage | Float       | Yes      | Defensive play time percentage            |
| week                         | Integer     | Yes      | Week number                               |
| game_date                    | DateTime    | Yes      | Game date                                 |
| created_at                   | DateTime    | No       | Timestamp of creation                     |
| updated_at                   | DateTime    | Yes      | Timestamp of last update                  |
- **Relationships**:
  - `player`: One-to-One relationship with the Player table.
  - `club`: One-to-One relationship with the Club table.


### Table 3: `player_salary`
| Column Name              | Data Type   | Nullable | Description                         |
|--------------------------|-------------|----------|-------------------------------------|
| id                       | Integer     | No       | Primary key                         |
| player_id                | Integer     | Yes      | Foreign key to players              |
| year_signed              | String      | Yes      | Year deal was signed                |
| team                     | String      | Yes      | Team name                           |
| average_per_year         | Integer     | Yes      | Average salary per year             |
| total_value              | Integer     | Yes      | Total contract value                |
| guaranteed               | Integer     | Yes      | Guaranteed amount                   |
| position                 | String      | Yes      | Player's position                   |
| created_at               | DateTime    | No       | Timestamp of creation               |
| updated_at               | DateTime    | Yes      | Timestamp of last update            |
- **Relationships:**
  - `player`: Relationship with `players`


### Table 3: `player_transactions`
| Column Name          | Data Type   | Nullable | Description                          |
|----------------------|-------------|----------|--------------------------------------|
| id                   | Integer     | No       | Primary key                          |
| player_id            | Integer     | Yes      | Foreign key to players               |
| type                 | String      | Yes      | Transaction type                     |
| name                 | String      | Yes      | Transaction name                     |
| description          | String      | Yes      | Transaction description              |
| position             | String      | Yes      | Player's position at the time        |
| date                 | DateTime    | Yes      | Transaction date (indexed)           |
| sending_club_id      | Integer     | Yes      | Foreign key to clubs (sending club)  |
| receiving_club_id    | Integer     | Yes      | Foreign key to clubs (receiving club)|
| transaction_year     | String      | Yes      | Year of the transaction              |
| created_at           | DateTime    | No       | Timestamp of creation                |
| updated_at           | DateTime    | Yes      | Timestamp of last update             |

- **Relationships**:
  - `player`: One-to-One relationship with the Player table.
  - `sending_club`: One-to-One relationship with the Club table (foreign key to sending_club_id).
  - `receiving_club`: One-to-One relationship with the Club table (foreign key to receiving_club_id).


### Table 3: `position_aggregations`
| Column Name                | Data Type   | Nullable | Description                         |
|----------------------------|-------------|----------|-------------------------------------|
| id                         | Integer     | No       | Primary key                         |
| position                   | String      | No       | Player's position                   |
| total_team_plays           | Integer     | No       | Total team plays                    |
| total_offensive_team_plays | Integer     | No       | Total offensive team plays          |
| total_defensive_team_plays | Integer     | No       | Total defensive team plays          |
| created_at                 | DateTime    | No       | Timestamp of creation               |
| updated_at                 | DateTime    | Yes      | Timestamp of last update            |


### Table 3: `club_aggregations`
| Column Name                | Data Type   | Nullable | Description                         |
|----------------------------|-------------|----------|-------------------------------------|
| id                         | Integer     | No       | Primary key                         |
| club_name                  | String      | No       | Club name                           |
| total_team_plays           | Integer     | No       | Total team plays                    |
| total_offensive_team_plays | Integer     | No       | Total offensive team plays          |
| total_defensive_team_plays | Integer     | No       | Total defensive team plays          |
| created_at                 | DateTime    | No       | Timestamp of creation               |
| updated_at                 | DateTime    | Yes      | Timestamp of last update            |


### Table 3: `season_aggregations`
| Column Name                | Data Type   | Nullable | Description                         |
|----------------------------|-------------|----------|-------------------------------------|
| id                         | Integer     | No       | Primary key                         |
| season                     | String      | No       | Season name                         |
| total_team_plays           | Integer     | No       | Total team plays                    |
| total_offensive_team_plays | Integer     | No       | Total offensive team plays          |
| total_defensive_team_plays | Integer     | No       | Total defensive team plays          |
| created_at                 | DateTime    | No       | Timestamp of creation               |
| updated_at                 | DateTime    | Yes      | Timestamp of last update            |


### Table 3: `player_ranking_season_aggregation`
| Column Name              | Data Type   | Nullable | Description                         |
|--------------------------|-------------|----------|-------------------------------------|
| id                       | Integer     | No       | Primary key                         |
| name                     | String      | Yes      | Player name                         |
| player_id                | Integer     | No       | Foreign key to players              |
| season                   | String      | Yes      | Season name                         |
| defense_plays_percentile | Float       | Yes      | Percentile of defensive plays       |
| offense_plays_percentile | Float       | Yes      | Percentile of offensive plays       |
| created_at               | DateTime    | No       | Timestamp of creation               |
| updated_at               | DateTime    | Yes      | Timestamp of last update            |

- **Relationships**:
  - `player`: One-to-One relationship with the Player table.


### Table 3: `player_ranking_position_aggregation`
| Column Name              | Data Type   | Nullable | Description                         |
|--------------------------|-------------|----------|-------------------------------------|
| id                       | Integer     | No       | Primary key                         |
| name                     | String      | Yes      | Player name                         |
| player_id                | Integer     | No       | Foreign key to players              |
| position                 | String      | Yes      | Player's position                   |
| defense_plays_percentile | Float       | Yes      | Percentile of defensive plays       |
| offense_plays_percentile | Float       | Yes      | Percentile of offensive plays       |
| created_at               | DateTime    | No       | Timestamp of creation               |
| updated_at               | DateTime    | Yes      | Timestamp of last update            |

- **Relationships**:
  - `player`: One-to-One relationship with the Player table.


### Table 3: `player_ranking_club_aggregation`
| Column Name              | Data Type   | Nullable | Description                         |
|--------------------------|-------------|----------|-------------------------------------|
| id                       | Integer     | No       | Primary key                         |
| name                     | String      | Yes      | Player name                         |
| player_id                | Integer     | No       | Foreign key to players              |
| club                     | String      | Yes      | Club name                           |
| defense_plays_percentile | Float       | Yes      | Percentile of defensive plays       |
| created_at               | DateTime    | No       | Timestamp of creation               |
| updated_at               | DateTime    | Yes      | Timestamp of last update            |

- **Relationships**:
  - `player`: One-to-One relationship with the Player table.


