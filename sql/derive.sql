-- CAST truncates rather than rounds: these are counters of completed days, not
-- measurements. A repo pushed 20 hours ago is 0 days silent, not 1.
UPDATE repositories
SET created_year = CAST(strftime('%Y',created_at) AS INTEGER),
    age_days = CAST(julianday(?) - julianday(created_at) AS INTEGER),
    days_since_push  = CAST(julianday(?) - julianday(pushed_at) AS INTEGER);
     