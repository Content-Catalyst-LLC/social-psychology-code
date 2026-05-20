-- Tragedy of the Commons in Social Psychology
-- Relational schema for commons extraction, resource depletion, governance legitimacy, monitoring, sanctions, and common-pool resource research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS commons_groups;
DROP TABLE IF EXISTS commons_trials;
DROP TABLE IF EXISTS resource_periods;

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

CREATE TABLE commons_groups (
    group_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    property_regime TEXT NOT NULL,
    group_size INTEGER CHECK (group_size >= 1),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE commons_trials (
    participant TEXT NOT NULL,
    group_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    property_regime TEXT NOT NULL,
    round INTEGER NOT NULL CHECK (round >= 1),
    resource_stock REAL NOT NULL CHECK (resource_stock >= 0),
    carrying_capacity REAL NOT NULL CHECK (carrying_capacity >= 0),
    regeneration_rate REAL NOT NULL CHECK (regeneration_rate >= 0),
    regeneration REAL NOT NULL CHECK (regeneration >= 0),
    extraction REAL NOT NULL CHECK (extraction >= 0),
    sustainable_threshold REAL NOT NULL CHECK (sustainable_threshold >= 0),
    trust_score REAL NOT NULL CHECK (trust_score >= 0 AND trust_score <= 10),
    legitimacy_score REAL NOT NULL CHECK (legitimacy_score >= 0 AND legitimacy_score <= 10),
    monitoring_credibility REAL NOT NULL CHECK (monitoring_credibility >= 0 AND monitoring_credibility <= 10),
    sanction_probability REAL NOT NULL CHECK (sanction_probability >= 0 AND sanction_probability <= 1),
    sanction_severity REAL NOT NULL CHECK (sanction_severity >= 0 AND sanction_severity <= 10),
    boundary_clarity REAL NOT NULL CHECK (boundary_clarity >= 0 AND boundary_clarity <= 10),
    rule_participation REAL NOT NULL CHECK (rule_participation >= 0 AND rule_participation <= 10),
    conflict_resolution_access REAL NOT NULL CHECK (conflict_resolution_access >= 0 AND conflict_resolution_access <= 10),
    local_ecological_knowledge REAL NOT NULL CHECK (local_ecological_knowledge >= 0 AND local_ecological_knowledge <= 10),
    perceived_fairness REAL NOT NULL CHECK (perceived_fairness >= 0 AND perceived_fairness <= 10),
    reciprocity_expectation REAL NOT NULL CHECK (reciprocity_expectation >= 0 AND reciprocity_expectation <= 10),
    stewardship_norm_salience REAL NOT NULL CHECK (stewardship_norm_salience >= 0 AND stewardship_norm_salience <= 10),
    asymmetry_index REAL NOT NULL CHECK (asymmetry_index >= 0 AND asymmetry_index <= 10),
    depletion_risk REAL NOT NULL CHECK (depletion_risk >= 0 AND depletion_risk <= 1),
    group_welfare REAL NOT NULL,
    individual_payoff REAL NOT NULL,
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    expected_sanction REAL GENERATED ALWAYS AS (
        monitoring_credibility * sanction_probability * sanction_severity / 10.0
    ) VIRTUAL,
    institutional_effectiveness REAL GENERATED ALWAYS AS (
        boundary_clarity * monitoring_credibility * sanction_probability * sanction_severity *
        (legitimacy_score / 10.0) * (rule_participation / 10.0)
    ) VIRTUAL,
    PRIMARY KEY (participant, group_id, round),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES commons_groups(group_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE resource_periods (
    group_id TEXT NOT NULL,
    period INTEGER NOT NULL CHECK (period >= 1),
    resource_stock REAL NOT NULL CHECK (resource_stock >= 0),
    carrying_capacity REAL NOT NULL CHECK (carrying_capacity >= 0),
    total_extraction REAL NOT NULL CHECK (total_extraction >= 0),
    regeneration REAL NOT NULL CHECK (regeneration >= 0),
    sustainable_threshold REAL NOT NULL CHECK (sustainable_threshold >= 0),
    depletion_risk REAL NOT NULL CHECK (depletion_risk >= 0 AND depletion_risk <= 1),
    PRIMARY KEY (group_id, period),
    FOREIGN KEY (group_id) REFERENCES commons_groups(group_id)
);

CREATE INDEX idx_tc_condition ON commons_trials(condition);
CREATE INDEX idx_tc_regime ON commons_trials(property_regime);
CREATE INDEX idx_tc_group ON commons_trials(group_id);
CREATE INDEX idx_tc_round ON commons_trials(round);
CREATE INDEX idx_tc_depletion ON commons_trials(depletion_risk);

DROP VIEW IF EXISTS commons_governance_summary;
CREATE VIEW commons_governance_summary AS
SELECT
    condition,
    property_regime,
    round,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    AVG(extraction) AS mean_extraction,
    SUM(extraction) AS total_extraction,
    AVG(resource_stock) AS mean_resource_stock,
    AVG(regeneration) AS mean_regeneration,
    AVG(depletion_risk) AS mean_depletion_risk,
    AVG(trust_score) AS mean_trust,
    AVG(legitimacy_score) AS mean_legitimacy,
    AVG(monitoring_credibility) AS mean_monitoring,
    AVG(boundary_clarity) AS mean_boundary_clarity,
    AVG(rule_participation) AS mean_rule_participation,
    AVG(institutional_effectiveness) AS mean_institutional_effectiveness,
    AVG(group_welfare) AS mean_group_welfare
FROM commons_trials
GROUP BY condition, property_regime, round;

DROP VIEW IF EXISTS high_depletion_risk_cases;
CREATE VIEW high_depletion_risk_cases AS
SELECT
    participant,
    group_id,
    site_id,
    condition,
    property_regime,
    round,
    extraction,
    sustainable_threshold,
    resource_stock,
    depletion_risk,
    trust_score,
    legitimacy_score,
    monitoring_credibility,
    boundary_clarity,
    rule_participation,
    asymmetry_index
FROM commons_trials
WHERE depletion_risk >= 0.60 OR extraction > sustainable_threshold;
