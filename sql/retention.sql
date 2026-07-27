-- Two signals only. A support signal (open_issues) was dropped: every available
-- denominator is either popularity, which the sample is selected on, or one of
-- the two signals already used.
UPDATE repositories
SET retention_class = CASE
        -- A label, not NULL: the exclusion stays visible in the legend.
        WHEN created_year > 2020 THEN 'too_young'
        WHEN days_since_push >= 400 THEN 'faded'
        -- The mirror case (silent, large team) is not a conflict: the contributor
        -- count is cumulative, so a dead project keeps a high one.
        WHEN contributors <= 2 THEN 'active_small_team'
        ELSE 'retained'
    END;