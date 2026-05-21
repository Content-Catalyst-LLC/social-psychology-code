DROP TABLE IF EXISTS social_loafing_trials;

CREATE TABLE social_loafing_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    task_type TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    group_size INTEGER NOT NULL CHECK (group_size >= 1),
    solo_effort REAL NOT NULL CHECK (solo_effort >= 0 AND solo_effort <= 100),
    group_effort REAL NOT NULL CHECK (group_effort >= 0 AND group_effort <= 100),
    effort_loss REAL NOT NULL CHECK (effort_loss >= -100 AND effort_loss <= 100),
    output_score REAL NOT NULL CHECK (output_score >= 0 AND output_score <= 100),
    coordination_loss REAL NOT NULL CHECK (coordination_loss >= 0 AND coordination_loss <= 100),
    motivation_loss REAL NOT NULL CHECK (motivation_loss >= 0 AND motivation_loss <= 100),
    identifiability REAL NOT NULL CHECK (identifiability >= 0 AND identifiability <= 10),
    accountability REAL NOT NULL CHECK (accountability >= 0 AND accountability <= 10),
    task_value REAL NOT NULL CHECK (task_value >= 0 AND task_value <= 10),
    task_uniqueness REAL NOT NULL CHECK (task_uniqueness >= 0 AND task_uniqueness <= 10),
    task_visibility REAL NOT NULL CHECK (task_visibility >= 0 AND task_visibility <= 10),
    perceived_dispensability REAL NOT NULL CHECK (perceived_dispensability >= 0 AND perceived_dispensability <= 10),
    perceived_instrumentality REAL NOT NULL CHECK (perceived_instrumentality >= 0 AND perceived_instrumentality <= 10),
    free_rider_expectation REAL NOT NULL CHECK (free_rider_expectation >= 0 AND free_rider_expectation <= 10),
    sucker_effect_concern REAL NOT NULL CHECK (sucker_effect_concern >= 0 AND sucker_effect_concern <= 10),
    social_compensation_tendency REAL NOT NULL CHECK (social_compensation_tendency >= 0 AND social_compensation_tendency <= 10),
    group_cohesion REAL NOT NULL CHECK (group_cohesion >= 0 AND group_cohesion <= 10),
    group_identity_salience REAL NOT NULL CHECK (group_identity_salience >= 0 AND group_identity_salience <= 10),
    evaluation_potential REAL NOT NULL CHECK (evaluation_potential >= 0 AND evaluation_potential <= 10),
    digital_traceability REAL NOT NULL CHECK (digital_traceability >= 0 AND digital_traceability <= 10),
    remote_status TEXT NOT NULL,
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    log_group_size REAL GENERATED ALWAYS AS (log(group_size + 1)) VIRTUAL,
    accountability_index REAL GENERATED ALWAYS AS ((identifiability + accountability + task_visibility + evaluation_potential + digital_traceability) / 5.0) VIRTUAL,
    collective_effort_index REAL GENERATED ALWAYS AS ((perceived_instrumentality + task_value + task_uniqueness + group_identity_salience + group_cohesion - perceived_dispensability) / 5.0) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial)
);

CREATE INDEX idx_sl_condition ON social_loafing_trials(condition);
CREATE INDEX idx_sl_team ON social_loafing_trials(team_id);
CREATE INDEX idx_sl_group_size ON social_loafing_trials(group_size);

DROP VIEW IF EXISTS social_loafing_summary;
CREATE VIEW social_loafing_summary AS
SELECT
    condition,
    task_type,
    remote_status,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT team_id) AS n_teams,
    AVG(group_size) AS mean_group_size,
    AVG(solo_effort) AS mean_solo_effort,
    AVG(group_effort) AS mean_group_effort,
    AVG(effort_loss) AS mean_effort_loss,
    AVG(output_score) AS mean_output_score,
    AVG(coordination_loss) AS mean_coordination_loss,
    AVG(motivation_loss) AS mean_motivation_loss,
    AVG(accountability_index) AS mean_accountability_index,
    AVG(collective_effort_index) AS mean_collective_effort_index
FROM social_loafing_trials
GROUP BY condition, task_type, remote_status;
