-- Root schema for social psychology experiment and survey metadata.

CREATE TABLE IF NOT EXISTS participants (
    participant_id TEXT PRIMARY KEY,
    age_years INTEGER,
    language_background TEXT,
    group_identity TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS studies (
    study_id TEXT PRIMARY KEY,
    study_name TEXT NOT NULL,
    article_slug TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS trials (
    trial_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    study_id TEXT NOT NULL,
    trial_index INTEGER NOT NULL,
    condition TEXT,
    target_group TEXT,
    schema_consistent INTEGER,
    attribution_internal REAL,
    attribution_external REAL,
    trust_rating REAL,
    warmth_rating REAL,
    competence_rating REAL,
    response_time_ms REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
