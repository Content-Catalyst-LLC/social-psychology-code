-- Implicit Bias in Social Psychology
-- Relational schema for IAT-style trials, implicit associations, explicit attitudes,
-- judgment outcomes, behavioral outcomes, interventions, and institutional disparity.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS implicit_bias_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE groups (
    group_id TEXT PRIMARY KEY,
    group_type TEXT,
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
    institution_context TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE implicit_bias_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    target_category TEXT NOT NULL,
    attribute_category TEXT NOT NULL,
    congruent_block INTEGER NOT NULL CHECK (congruent_block IN (0, 1)),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 250),
    accuracy INTEGER NOT NULL CHECK (accuracy IN (0, 1)),
    explicit_attitude REAL NOT NULL CHECK (explicit_attitude >= -100 AND explicit_attitude <= 100),
    judgment_score REAL NOT NULL CHECK (judgment_score >= 0 AND judgment_score <= 100),
    behavioral_outcome REAL NOT NULL CHECK (behavioral_outcome >= 0 AND behavioral_outcome <= 100),
    cognitive_load REAL NOT NULL CHECK (cognitive_load >= 0 AND cognitive_load <= 10),
    accountability REAL NOT NULL CHECK (accountability >= 0 AND accountability <= 10),
    time_pressure REAL NOT NULL CHECK (time_pressure >= 0 AND time_pressure <= 10),
    counter_stereotypical_exposure REAL NOT NULL CHECK (counter_stereotypical_exposure >= 0 AND counter_stereotypical_exposure <= 10),
    perspective_taking REAL NOT NULL CHECK (perspective_taking >= 0 AND perspective_taking <= 10),
    structured_decision_support REAL NOT NULL CHECK (structured_decision_support >= 0 AND structured_decision_support <= 10),
    followup_days REAL NOT NULL CHECK (followup_days >= 0),
    automaticity_risk_index REAL GENERATED ALWAYS AS (
        (cognitive_load + time_pressure - accountability - structured_decision_support) / 4.0
    ) VIRTUAL,
    mitigation_index REAL GENERATED ALWAYS AS (
        (accountability + counter_stereotypical_exposure + perspective_taking + structured_decision_support) / 4.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_implicit_condition ON implicit_bias_trials(condition);
CREATE INDEX idx_implicit_context ON implicit_bias_trials(institution_context);
CREATE INDEX idx_implicit_participant ON implicit_bias_trials(participant);
CREATE INDEX idx_implicit_congruence ON implicit_bias_trials(congruent_block);

DROP VIEW IF EXISTS implicit_bias_summary;
CREATE VIEW implicit_bias_summary AS
SELECT
    condition,
    institution_context,
    congruent_block,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(response_time_ms) AS mean_response_time,
    AVG(accuracy) AS accuracy_rate,
    AVG(explicit_attitude) AS mean_explicit_attitude,
    AVG(judgment_score) AS mean_judgment,
    AVG(behavioral_outcome) AS mean_behavioral_outcome,
    AVG(automaticity_risk_index) AS mean_automaticity_risk,
    AVG(mitigation_index) AS mean_mitigation
FROM implicit_bias_trials
GROUP BY condition, institution_context, congruent_block;

DROP VIEW IF EXISTS participant_latency_blocks;
CREATE VIEW participant_latency_blocks AS
SELECT
    participant,
    condition,
    AVG(CASE WHEN congruent_block = 1 AND accuracy = 1 THEN response_time_ms END) AS mean_congruent_rt,
    AVG(CASE WHEN congruent_block = 0 AND accuracy = 1 THEN response_time_ms END) AS mean_incongruent_rt,
    AVG(explicit_attitude) AS mean_explicit_attitude,
    AVG(judgment_score) AS mean_judgment,
    AVG(behavioral_outcome) AS mean_behavioral_outcome
FROM implicit_bias_trials
GROUP BY participant, condition;
