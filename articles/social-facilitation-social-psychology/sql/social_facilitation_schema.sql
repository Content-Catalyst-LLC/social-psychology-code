-- Social Facilitation in Social Psychology
-- Relational schema for audience effects, coaction, evaluation apprehension, task difficulty, arousal, and performance research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS social_facilitation_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_sites (
    site_id TEXT PRIMARY KEY,
    site_type TEXT,
    location_code TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    session_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE social_facilitation_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    task_domain TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    audience_present INTEGER NOT NULL CHECK (audience_present IN (0, 1)),
    coaction_present INTEGER NOT NULL CHECK (coaction_present IN (0, 1)),
    evaluation_pressure REAL NOT NULL CHECK (evaluation_pressure >= 0 AND evaluation_pressure <= 10),
    observer_expertise REAL NOT NULL CHECK (observer_expertise >= 0 AND observer_expertise <= 10),
    audience_size INTEGER NOT NULL CHECK (audience_size >= 0),
    audience_valence REAL NOT NULL CHECK (audience_valence >= -5 AND audience_valence <= 5),
    task_difficulty REAL NOT NULL CHECK (task_difficulty >= 0 AND task_difficulty <= 10),
    task_mastery REAL NOT NULL CHECK (task_mastery >= 0 AND task_mastery <= 10),
    dominant_response_correct INTEGER NOT NULL CHECK (dominant_response_correct IN (0, 1)),
    baseline_skill REAL NOT NULL CHECK (baseline_skill >= 0 AND baseline_skill <= 10),
    arousal_index REAL NOT NULL CHECK (arousal_index >= 0 AND arousal_index <= 10),
    distraction_index REAL NOT NULL CHECK (distraction_index >= 0 AND distraction_index <= 10),
    attentional_conflict REAL NOT NULL CHECK (attentional_conflict >= 0 AND attentional_conflict <= 10),
    perceived_scrutiny REAL NOT NULL CHECK (perceived_scrutiny >= 0 AND perceived_scrutiny <= 10),
    performance_score REAL NOT NULL CHECK (performance_score >= 0 AND performance_score <= 100),
    accuracy REAL NOT NULL CHECK (accuracy >= 0 AND accuracy <= 1),
    error_rate REAL NOT NULL CHECK (error_rate >= 0 AND error_rate <= 1),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    digital_monitoring INTEGER NOT NULL CHECK (digital_monitoring IN (0, 1)),
    social_anxiety REAL NOT NULL CHECK (social_anxiety >= 0 AND social_anxiety <= 10),
    social_presence_intensity REAL GENERATED ALWAYS AS (
        audience_present + 0.65 * coaction_present + 0.50 * digital_monitoring
    ) VIRTUAL,
    mastery_advantage REAL GENERATED ALWAYS AS (
        task_mastery - task_difficulty
    ) VIRTUAL,
    evaluation_apprehension_index REAL GENERATED ALWAYS AS (
        (evaluation_pressure + perceived_scrutiny + observer_expertise + social_anxiety) / 4.0
    ) VIRTUAL,
    distraction_conflict_index REAL GENERATED ALWAYS AS (
        (distraction_index + attentional_conflict + perceived_scrutiny) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_sf_condition ON social_facilitation_trials(condition);
CREATE INDEX idx_sf_domain ON social_facilitation_trials(task_domain);
CREATE INDEX idx_sf_participant ON social_facilitation_trials(participant);
CREATE INDEX idx_sf_audience ON social_facilitation_trials(audience_present);
CREATE INDEX idx_sf_monitoring ON social_facilitation_trials(digital_monitoring);

DROP VIEW IF EXISTS social_facilitation_summary;
CREATE VIEW social_facilitation_summary AS
SELECT
    condition,
    task_domain,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(performance_score) AS mean_performance,
    AVG(accuracy) AS mean_accuracy,
    AVG(error_rate) AS mean_error_rate,
    AVG(response_time_ms) AS mean_response_time,
    AVG(arousal_index) AS mean_arousal,
    AVG(distraction_index) AS mean_distraction,
    AVG(evaluation_pressure) AS mean_evaluation,
    AVG(task_difficulty) AS mean_task_difficulty,
    AVG(task_mastery) AS mean_task_mastery,
    AVG(social_presence_intensity) AS mean_social_presence
FROM social_facilitation_trials
GROUP BY condition, task_domain;

DROP VIEW IF EXISTS facilitation_inhibition_cases;
CREATE VIEW facilitation_inhibition_cases AS
SELECT
    participant,
    session_id,
    condition,
    task_domain,
    trial,
    performance_score,
    task_difficulty,
    task_mastery,
    mastery_advantage,
    arousal_index,
    evaluation_apprehension_index,
    distraction_conflict_index,
    CASE
        WHEN social_presence_intensity > 0 AND mastery_advantage >= 1 THEN 'facilitation_likely'
        WHEN social_presence_intensity > 0 AND mastery_advantage < 0 THEN 'inhibition_likely'
        ELSE 'baseline_or_mixed'
    END AS predicted_pattern
FROM social_facilitation_trials;
