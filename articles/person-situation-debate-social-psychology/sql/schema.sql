-- Article-level synthetic social psychology schema.

CREATE TABLE IF NOT EXISTS social_trials (
    trial_id INTEGER PRIMARY KEY,
    participant_id TEXT NOT NULL,
    trial_index INTEGER NOT NULL,
    condition TEXT,
    target_group TEXT,
    schema_consistent INTEGER,
    attribution_internal REAL,
    attribution_external REAL,
    trust_rating REAL,
    warmth_rating REAL,
    competence_rating REAL,
    response_time_ms REAL
);

CREATE INDEX IF NOT EXISTS idx_social_trials_participant
ON social_trials(participant_id);

CREATE INDEX IF NOT EXISTS idx_social_trials_group
ON social_trials(target_group);

CREATE INDEX IF NOT EXISTS idx_social_trials_condition
ON social_trials(condition);
