-- Star schema for the GitHub OSS retention analysis.
--
-- No year dimension: a year has no attributes of its own here — the cohort cutoff
-- is a filter, not a stored property — so the table would be a join returning a
-- value the fact already has. Year lives as created_year.
--
-- FKs are declared but SQLite does not enforce them by default: they document the
-- model and drive relationship detection in Power BI. Integrity is the loader's job.

-- ---------- DIMENSIONS (declared first: the fact references them) ----------

CREATE TABLE languages (
    language TEXT PRIMARY KEY
);

CREATE TABLE owners (
    owner_login TEXT PRIMARY KEY,
    owner_type  TEXT NOT NULL,
    -- No BOOLEAN in SQLite. DEFAULT 0, not nullable: the top-corp list is frozen
    -- and complete, so "not in the list" is a known false, not an unknown.
    is_top_corp INTEGER NOT NULL DEFAULT 0 CHECK (is_top_corp IN (0, 1))
);

-- ---------- FACT ----------

CREATE TABLE repositories (
    repo_id         INTEGER PRIMARY KEY,
    full_name       TEXT NOT NULL,

    owner_login     TEXT,
    -- Nullable by design: ~10% are documentation repos with no language. A NULL FK
    -- drops them from any INNER JOIN on languages, so language cuts exclude them by
    -- construction, not by a filter someone must remember. They stay in the team-size
    -- and owner_type cuts, where the axes apply.
    language        TEXT,

    stars           INTEGER,
    forks           INTEGER,
    open_issues     INTEGER,
    -- Nullable keeps "could not be counted" (5 repos) distinct from a real 0.
    contributors    INTEGER,

    -- ISO-8601 from the API; string ordering matches chronological ordering.
    created_at      TEXT,
    pushed_at       TEXT,

    -- Derived at load time. Measured against a frozen snapshot_date, never now():
    -- with now() the same repo shifts value on every rerun, and retention_class
    -- would drift with the run date instead of the data.
    created_year    INTEGER,
    age_days        INTEGER,
    days_since_push INTEGER,
    retention_class TEXT,

    FOREIGN KEY (owner_login) REFERENCES owners(owner_login),
    FOREIGN KEY (language)    REFERENCES languages(language)
);