-- Self-Serving Bias in Social Psychology
-- Relational schema for attribution, responsibility, accountability, and learning research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS self_serving_bias_trials;
DROP TABLE IF EXISTS organizational_incidents;
DROP TABLE IF EXISTS accountability_reviews;

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

CREATE TABLE self_serving_bias_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    outcome_valence TEXT NOT NULL CHECK (outcome_valence IN ('positive', 'negative', 'mixed', 'ambiguous')),
    actor_target TEXT NOT NULL,
    self_other TEXT NOT NULL CHECK (self_other IN ('self', 'other')),
    internal_attribution REAL NOT NULL CHECK (internal_attribution >= 0 AND internal_attribution <= 10),
    external_attribution REAL NOT NULL CHECK (external_attribution >= 0 AND external_attribution <= 10),
    stable_attribution REAL NOT NULL CHECK (stable_attribution >= 0 AND stable_attribution <= 10),
    controllable_attribution REAL NOT NULL CHECK (controllable_attribution >= 0 AND controllable_attribution <= 10),
    responsibility_rating REAL NOT NULL CHECK (responsibility_rating >= 0 AND responsibility_rating <= 10),
    blame_rating REAL NOT NULL CHECK (blame_rating >= 0 AND blame_rating <= 10),
    credit_claiming REAL NOT NULL CHECK (credit_claiming >= 0 AND credit_claiming <= 10),
    excuse_making REAL NOT NULL CHECK (excuse_making >= 0 AND excuse_making <= 10),
    self_esteem REAL NOT NULL CHECK (self_esteem >= 0 AND self_esteem <= 10),
    ego_threat REAL NOT NULL CHECK (ego_threat >= 0 AND ego_threat <= 10),
    task_importance REAL NOT NULL CHECK (task_importance >= 0 AND task_importance <= 10),
    outcome_expectancy REAL NOT NULL CHECK (outcome_expectancy >= 0 AND outcome_expectancy <= 10),
    perceived_fairness REAL NOT NULL CHECK (perceived_fairness >= 0 AND perceived_fairness <= 10),
    evidence_strength REAL NOT NULL CHECK (evidence_strength >= 0 AND evidence_strength <= 10),
    learning_intention REAL NOT NULL CHECK (learning_intention >= 0 AND learning_intention <= 10),
    accountability_pressure REAL NOT NULL CHECK (accountability_pressure >= 0 AND accountability_pressure <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE organizational_incidents (
    incident_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    outcome_valence TEXT NOT NULL,
    evidence_strength REAL CHECK (evidence_strength >= 0 AND evidence_strength <= 10),
    leader_credit_claiming REAL CHECK (leader_credit_claiming >= 0 AND leader_credit_claiming <= 10),
    leader_excuse_making REAL CHECK (leader_excuse_making >= 0 AND leader_excuse_making <= 10),
    learning_score REAL CHECK (learning_score >= 0 AND learning_score <= 10),
    incident_date TEXT,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE accountability_reviews (
    review_id TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    accountability_pressure REAL CHECK (accountability_pressure >= 0 AND accountability_pressure <= 10),
    evidence_review_quality REAL CHECK (evidence_review_quality >= 0 AND evidence_review_quality <= 10),
    corrective_action INTEGER CHECK (corrective_action IN (0, 1)),
    FOREIGN KEY (incident_id) REFERENCES organizational_incidents(incident_id)
);

CREATE INDEX idx_ssb_condition ON self_serving_bias_trials(condition);
CREATE INDEX idx_ssb_valence ON self_serving_bias_trials(outcome_valence);
CREATE INDEX idx_ssb_self_other ON self_serving_bias_trials(self_other);
CREATE INDEX idx_ssb_actor ON self_serving_bias_trials(actor_target);
CREATE INDEX idx_ssb_participant ON self_serving_bias_trials(participant);

DROP VIEW IF EXISTS attribution_summary;
CREATE VIEW attribution_summary AS
SELECT
    condition,
    outcome_valence,
    self_other,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(internal_attribution) AS mean_internal,
    AVG(external_attribution) AS mean_external,
    AVG(responsibility_rating) AS mean_responsibility,
    AVG(blame_rating) AS mean_blame,
    AVG(credit_claiming) AS mean_credit,
    AVG(excuse_making) AS mean_excuse,
    AVG(ego_threat) AS mean_ego_threat,
    AVG(learning_intention) AS mean_learning,
    AVG(accountability_pressure) AS mean_accountability,
    AVG(evidence_strength) AS mean_evidence
FROM self_serving_bias_trials
GROUP BY condition, outcome_valence, self_other;

DROP VIEW IF EXISTS high_deflection_cases;
CREATE VIEW high_deflection_cases AS
SELECT
    participant,
    site_id,
    condition,
    outcome_valence,
    actor_target,
    self_other,
    internal_attribution,
    external_attribution,
    responsibility_rating,
    excuse_making,
    ego_threat,
    evidence_strength,
    accountability_pressure,
    learning_intention
FROM self_serving_bias_trials
WHERE outcome_valence = 'negative'
  AND self_other = 'self'
  AND external_attribution >= 7
  AND excuse_making >= 7;
