WITH ranked_data AS (
    SELECT
        prsa.season,
        prsa.name,
        prsa.player_id,
        prsa.defense_plays_percentile,
        prsa.offense_plays_percentile,
        ROW_NUMBER() OVER(PARTITION BY prsa.season ORDER BY prsa.defense_plays_percentile DESC) AS defense_rank,
        ROW_NUMBER() OVER(PARTITION BY prsa.season ORDER BY prsa.offense_plays_percentile DESC) AS offense_rank
    FROM
        player_ranking_aggregations_season AS prsa
    WHERE
        prsa.defense_plays_percentile IS NOT NULL
        AND prsa.offense_plays_percentile IS NOT NULL
)
SELECT
    season,
    name,
    player_id,
    defense_plays_percentile,
    offense_plays_percentile
FROM
    ranked_data
WHERE
    defense_rank <= 5 OR offense_rank <= 5
ORDER BY
    season ASC,
    defense_plays_percentile DESC,
    offense_plays_percentile DESC;
