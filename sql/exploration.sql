-- Queries behind data/FINDINGS.md Run after load.py and derive.py.


-- Silence by year, with organisation share as a composition control.
-- age_days > X is required: a repo cannot be silent longer than it has existed.
SELECT r.created_year,
       COUNT(*) AS total,
       SUM(CASE WHEN r.days_since_push > 700 THEN 1 ELSE 0 END) AS silent,
       ROUND(1.0 * SUM(CASE WHEN r.days_since_push > 700 THEN 1 ELSE 0 END) / COUNT(*), 3) AS share,
       ROUND(1.0 * SUM(CASE WHEN o.owner_type = 'Organization' THEN 1 ELSE 0 END) / COUNT(*), 3) AS org
FROM repositories r
JOIN owners o ON r.owner_login = o.owner_login
WHERE r.age_days > 700
GROUP BY r.created_year
ORDER BY r.created_year DESC;


-- Cohort composition: entry bar per year, and a check on the 2017 anomaly.
SELECT created_year,
       COUNT(*) AS total,
       MIN(stars) AS min_stars,
       ROUND(AVG(stars)) AS avg_stars,
       MAX(stars) AS max_stars,
       SUM(CASE WHEN language IS NULL THEN 1 ELSE 0 END) AS no_lang
FROM repositories
GROUP BY created_year
ORDER BY created_year DESC;


-- How the lower edge of the team axis thins out with age.
SELECT created_year,
       COUNT(*) AS total,
       SUM(CASE WHEN contributors <= 2 THEN 1 ELSE 0 END) AS small_teams
FROM repositories
GROUP BY created_year
ORDER BY created_year DESC;


-- Team size distribution — read per value, not per bucket: bucket widths differ.
SELECT CASE
         WHEN contributors = 1 THEN '1'
         WHEN contributors = 2 THEN '2'
         WHEN contributors <= 5 THEN '3-5'
         WHEN contributors <= 10 THEN '6-10'
         WHEN contributors <= 50 THEN '11-50'
         ELSE '51+'
       END AS bucket,
       COUNT(*) AS n
FROM repositories
WHERE created_year <= 2020
GROUP BY bucket
-- Alphabetical order would put '11-50' before '2'.
ORDER BY MIN(contributors);


-- Core result. Rerun at cohort 2019 and ruler 400 — the gap holds at 31-36 pp.
SELECT CASE WHEN contributors <= 2 THEN 'small (1-2)' ELSE 'rest (3+)' END AS team,
       COUNT(*) AS total,
       SUM(CASE WHEN days_since_push < 700 THEN 1 ELSE 0 END) AS active,
       ROUND(1.0 * SUM(CASE WHEN days_since_push < 700 THEN 1 ELSE 0 END) / COUNT(*), 3) AS share
FROM repositories
WHERE created_year <= 2020
GROUP BY team;

-- Signal cross-tab: which of the four cells are genuinely conflicting.
SELECT CASE WHEN contributors <= 2 THEN 'small' ELSE 'big' END AS team,
       CASE WHEN days_since_push < 400 THEN 'active' ELSE 'silent' END AS activity,
       COUNT(*) AS n
FROM repositories
WHERE created_year <= 2020
GROUP BY team, activity;

-- Repos with no code in the class: pushed_at there means list upkeep, not development.
SELECT full_name FROM repositories
WHERE retention_class = 'active_small_team' AND language IS NULL;


-- Organisations by repo count: tested as a data-driven basis for is_top_corp.
SELECT o.owner_login, COUNT(*) AS repos
FROM repositories r
JOIN owners o ON r.owner_login = o.owner_login
WHERE o.owner_type = 'Organization'
GROUP BY o.owner_login
ORDER BY repos DESC
LIMIT 30;