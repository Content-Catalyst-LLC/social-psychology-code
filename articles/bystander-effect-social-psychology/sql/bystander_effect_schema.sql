-- Bystander Effect in Social Psychology
-- Relational schema for bystander intervention, diffusion of responsibility, pluralistic ignorance, evaluation apprehension, direct assignment, and online intervention research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS bystander_effect_trials;

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

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    context_type TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bystander_effect_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    context_type TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    actual_bystander_count INTEGER NOT NULL CHECK (actual_bystander_count >= 0),
    perceived_bystander_count INTEGER NOT NULL CHECK (perceived_bystander_count >= 0),
    emergency_clarity REAL NOT NULL CHECK (emergency_clarity >= 0 AND emergency_clarity <= 10),
    danger_level REAL NOT NULL CHECK (danger_level >= 0 AND danger_level <= 10),
    victim_identifiability REAL NOT NULL CHECK (victim_identifiability >= 0 AND victim_identifiability <= 10),
    shared_identity REAL NOT NULL CHECK (shared_identity >= 0 AND shared_identity <= 10),
    felt_responsibility REAL NOT NULL CHECK (felt_responsibility >= 0 AND felt_responsibility <= 10),
    diffusion_responsibility REAL NOT NULL CHECK (diffusion_responsibility >= 0 AND diffusion_responsibility <= 10),
    pluralistic_ignorance REAL NOT NULL CHECK (pluralistic_ignorance >= 0 AND pluralistic_ignorance <= 10),
    evaluation_apprehension REAL NOT NULL CHECK (evaluation_apprehension >= 0 AND evaluation_apprehension <= 10),
    perceived_competence REAL NOT NULL CHECK (perceived_competence >= 0 AND perceived_competence <= 10),
    intervention_cost REAL NOT NULL CHECK (intervention_cost >= 0 AND intervention_cost <= 10),
    direct_assignment INTEGER NOT NULL CHECK (direct_assignment IN (0, 1)),
    leadership_cue INTEGER NOT NULL CHECK (leadership_cue IN (0, 1)),
    intervention_norm_salience REAL NOT NULL CHECK (intervention_norm_salience >= 0 AND intervention_norm_salience <= 10),
    online_context INTEGER NOT NULL CHECK (online_context IN (0, 1)),
    platform_traceability REAL NOT NULL CHECK (platform_traceability >= 0 AND platform_traceability <= 10),
    moderation_visibility REAL NOT NULL CHECK (moderation_visibility >= 0 AND moderation_visibility <= 10),
    intervention_likelihood REAL NOT NULL CHECK (intervention_likelihood >= 0 AND intervention_likelihood <= 100),
    actual_intervention INTEGER NOT NULL CHECK (actual_intervention IN (0, 1)),
    intervention_latency_ms REAL NOT NULL CHECK (intervention_latency_ms >= 150),
    response_confidence REAL NOT NULL CHECK (response_confidence >= 0 AND response_confidence <= 10),
    log_perceived_bystanders REAL GENERATED ALWAYS AS (log(perceived_bystander_count + 1)) VIRTUAL,
    responsibility_assignment_index REAL GENERATED ALWAYS AS (
        (felt_responsibility + 2.0 * direct_assignment + 1.4 * leadership_cue + intervention_norm_salience) / 4.0
    ) VIRTUAL,
    ambiguity_index REAL GENERATED ALWAYS AS (
        (pluralistic_ignorance + evaluation_apprehension + (10.0 - emergency_clarity)) / 3.0
    ) VIRTUAL,
    helping_capacity_index REAL GENERATED ALWAYS AS (
        (perceived_competence + response_confidence + intervention_norm_salience - intervention_cost) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_be_condition ON bystander_effect_trials(condition);
CREATE INDEX idx_be_context ON bystander_effect_trials(context_type);
CREATE INDEX idx_be_participant ON bystander_effect_trials(participant);
CREATE INDEX idx_be_scenario ON bystander_effect_trials(scenario_id);
CREATE INDEX idx_be_bystanders ON bystander_effect_trials(perceived_bystander_count);

DROP VIEW IF EXISTS bystander_effect_summary;
CREATE VIEW bystander_effect_summary AS
SELECT
    condition,
    context_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(perceived_bystander_count) AS mean_perceived_bystanders,
    AVG(actual_intervention) AS intervention_rate,
    AVG(intervention_likelihood) AS mean_intervention_likelihood,
    AVG(intervention_latency_ms) AS mean_latency_ms,
    AVG(felt_responsibility) AS mean_felt_responsibility,
    AVG(diffusion_responsibility) AS mean_diffusion,
    AVG(pluralistic_ignorance) AS mean_pluralistic_ignorance,
    AVG(evaluation_apprehension) AS mean_evaluation_apprehension,
    AVG(emergency_clarity) AS mean_emergency_clarity,
    AVG(perceived_competence) AS mean_competence
FROM bystander_effect_trials
GROUP BY condition, context_type;

DROP VIEW IF EXISTS high_risk_nonintervention_cases;
CREATE VIEW high_risk_nonintervention_cases AS
SELECT
    participant,
    session_id,
    scenario_id,
    condition,
    context_type,
    perceived_bystander_count,
    emergency_clarity,
    danger_level,
    felt_responsibility,
    diffusion_responsibility,
    pluralistic_ignorance,
    evaluation_apprehension,
    perceived_competence,
    intervention_cost,
    direct_assignment,
    intervention_likelihood,
    actual_intervention,
    intervention_latency_ms
FROM bystander_effect_trials
WHERE danger_level >= 6 AND emergency_clarity >= 6 AND actual_intervention = 0;
