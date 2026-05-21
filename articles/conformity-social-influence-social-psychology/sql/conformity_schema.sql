-- Conformity and Social Influence
-- Relational schema for conformity, normative influence, informational influence, unanimity,
-- visible dissent, minority influence, digital social proof, and institutional conformity.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS influence_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS conformity_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE influence_groups (
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
    context TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conformity_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    context TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    ambiguity REAL NOT NULL CHECK (ambiguity >= 0 AND ambiguity <= 10),
    majority_size INTEGER NOT NULL CHECK (majority_size >= 0),
    unanimity REAL NOT NULL CHECK (unanimity >= 0 AND unanimity <= 10),
    visible_dissent REAL NOT NULL CHECK (visible_dissent >= 0 AND visible_dissent <= 10),
    cohesion REAL NOT NULL CHECK (cohesion >= 0 AND cohesion <= 10),
    normative_pressure REAL NOT NULL CHECK (normative_pressure >= 0 AND normative_pressure <= 10),
    informational_uncertainty REAL NOT NULL CHECK (informational_uncertainty >= 0 AND informational_uncertainty <= 10),
    status_strength REAL NOT NULL CHECK (status_strength >= 0 AND status_strength <= 10),
    public_response INTEGER NOT NULL CHECK (public_response IN (0, 1)),
    private_response INTEGER NOT NULL CHECK (private_response IN (0, 1)),
    group_identification REAL NOT NULL CHECK (group_identification >= 0 AND group_identification <= 10),
    social_identity_salience REAL NOT NULL CHECK (social_identity_salience >= 0 AND social_identity_salience <= 10),
    minority_consistency REAL NOT NULL CHECK (minority_consistency >= 0 AND minority_consistency <= 10),
    network_exposure REAL NOT NULL CHECK (network_exposure >= 0 AND network_exposure <= 10),
    social_proof_metrics REAL NOT NULL CHECK (social_proof_metrics >= 0 AND social_proof_metrics <= 10),
    algorithmic_amplification REAL NOT NULL CHECK (algorithmic_amplification >= 0 AND algorithmic_amplification <= 10),
    conformed INTEGER NOT NULL CHECK (conformed IN (0, 1)),
    dissented INTEGER NOT NULL CHECK (dissented IN (0, 1)),
    confidence_pre REAL NOT NULL CHECK (confidence_pre >= 0 AND confidence_pre <= 100),
    confidence_post REAL NOT NULL CHECK (confidence_post >= 0 AND confidence_post <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    confidence_shift REAL GENERATED ALWAYS AS (confidence_post - confidence_pre) VIRTUAL,
    normative_influence_index REAL GENERATED ALWAYS AS (
        (normative_pressure + unanimity + cohesion + status_strength + public_response * 10.0 + group_identification - visible_dissent) / 6.0
    ) VIRTUAL,
    informational_influence_index REAL GENERATED ALWAYS AS (
        (ambiguity + informational_uncertainty + status_strength + social_proof_metrics - visible_dissent) / 4.0
    ) VIRTUAL,
    digital_social_proof_index REAL GENERATED ALWAYS AS (
        (network_exposure + social_proof_metrics + algorithmic_amplification) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES influence_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_conf_condition ON conformity_trials(condition);
CREATE INDEX idx_conf_context ON conformity_trials(context);
CREATE INDEX idx_conf_group ON conformity_trials(group_id);
CREATE INDEX idx_conf_participant ON conformity_trials(participant);

DROP VIEW IF EXISTS conformity_summary;
CREATE VIEW conformity_summary AS
SELECT
    condition,
    context,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    AVG(conformed) AS conformity_rate,
    AVG(dissented) AS dissent_rate,
    AVG(confidence_shift) AS mean_confidence_shift,
    AVG(normative_influence_index) AS mean_normative_influence,
    AVG(informational_influence_index) AS mean_informational_influence,
    AVG(digital_social_proof_index) AS mean_digital_social_proof,
    AVG(response_time_ms) AS mean_response_time
FROM conformity_trials
GROUP BY condition, context;

DROP VIEW IF EXISTS high_conformity_risk_cases;
CREATE VIEW high_conformity_risk_cases AS
SELECT
    participant,
    session_id,
    group_id,
    scenario_id,
    condition,
    context,
    normative_influence_index,
    informational_influence_index,
    digital_social_proof_index,
    unanimity,
    visible_dissent,
    conformed,
    dissented,
    confidence_shift,
    response_time_ms
FROM conformity_trials
WHERE conformed = 1
  AND (normative_influence_index >= 6 OR informational_influence_index >= 6 OR digital_social_proof_index >= 7)
  AND visible_dissent <= 3;
