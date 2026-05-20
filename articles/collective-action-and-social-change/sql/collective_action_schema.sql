-- Collective Action and Social Change
-- Relational schema for social psychology and social movement research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS movement_groups;
DROP TABLE IF EXISTS collective_action_trials;
DROP TABLE IF EXISTS network_edges;
DROP TABLE IF EXISTS movement_events;
DROP TABLE IF EXISTS institutional_responses;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    demographic_group TEXT,
    location_code TEXT,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movement_groups (
    group_id TEXT PRIMARY KEY,
    movement_domain TEXT NOT NULL,
    group_name TEXT,
    organization_type TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE collective_action_trials (
    participant TEXT NOT NULL,
    group_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    movement_domain TEXT NOT NULL,
    identity_strength REAL NOT NULL CHECK (identity_strength >= 0 AND identity_strength <= 10),
    perceived_injustice REAL NOT NULL CHECK (perceived_injustice >= 0 AND perceived_injustice <= 10),
    moral_outrage REAL NOT NULL CHECK (moral_outrage >= 0 AND moral_outrage <= 10),
    collective_efficacy REAL NOT NULL CHECK (collective_efficacy >= 0 AND collective_efficacy <= 10),
    network_support REAL NOT NULL CHECK (network_support >= 0 AND network_support <= 10),
    mobilization_exposure REAL NOT NULL CHECK (mobilization_exposure >= 0 AND mobilization_exposure <= 10),
    participation_cost REAL NOT NULL CHECK (participation_cost >= 0 AND participation_cost <= 10),
    perceived_repression_risk REAL NOT NULL CHECK (perceived_repression_risk >= 0 AND perceived_repression_risk <= 10),
    free_rider_incentive REAL NOT NULL CHECK (free_rider_incentive >= 0 AND free_rider_incentive <= 10),
    participation_intention REAL NOT NULL CHECK (participation_intention >= 0 AND participation_intention <= 1),
    action_participation INTEGER NOT NULL CHECK (action_participation IN (0, 1)),
    digital_engagement REAL NOT NULL CHECK (digital_engagement >= 0 AND digital_engagement <= 10),
    offline_engagement REAL NOT NULL CHECK (offline_engagement >= 0 AND offline_engagement <= 10),
    recruitment_source TEXT NOT NULL,
    institutional_response TEXT NOT NULL,
    perceived_legitimacy REAL NOT NULL CHECK (perceived_legitimacy >= 0 AND perceived_legitimacy <= 10),
    movement_outcome REAL NOT NULL CHECK (movement_outcome >= 0 AND movement_outcome <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES movement_groups(group_id)
);

CREATE TABLE network_edges (
    source_participant TEXT NOT NULL,
    target_participant TEXT NOT NULL,
    tie_type TEXT NOT NULL DEFAULT 'social',
    tie_strength REAL CHECK (tie_strength >= 0 AND tie_strength <= 10),
    observed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_participant, target_participant, tie_type)
);

CREATE TABLE movement_events (
    event_id TEXT PRIMARY KEY,
    group_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT,
    estimated_participants INTEGER CHECK (estimated_participants >= 0),
    digital_reach INTEGER CHECK (digital_reach >= 0),
    issue_frame TEXT,
    location_code TEXT,
    FOREIGN KEY (group_id) REFERENCES movement_groups(group_id)
);

CREATE TABLE institutional_responses (
    response_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    response_type TEXT NOT NULL,
    response_date TEXT,
    institution_type TEXT,
    response_severity REAL CHECK (response_severity >= 0 AND response_severity <= 10),
    policy_change INTEGER CHECK (policy_change IN (0, 1)),
    repression_indicator INTEGER CHECK (repression_indicator IN (0, 1)),
    FOREIGN KEY (event_id) REFERENCES movement_events(event_id)
);

CREATE INDEX idx_collective_condition ON collective_action_trials(condition);
CREATE INDEX idx_collective_group ON collective_action_trials(group_id);
CREATE INDEX idx_collective_domain ON collective_action_trials(movement_domain);
CREATE INDEX idx_collective_response ON collective_action_trials(institutional_response);
CREATE INDEX idx_collective_participation ON collective_action_trials(action_participation);
CREATE INDEX idx_network_source ON network_edges(source_participant);
CREATE INDEX idx_network_target ON network_edges(target_participant);
CREATE INDEX idx_events_group ON movement_events(group_id);

DROP VIEW IF EXISTS condition_summary;
CREATE VIEW condition_summary AS
SELECT
    condition,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    AVG(action_participation) AS participation_rate,
    AVG(participation_intention) AS mean_intention,
    AVG(identity_strength) AS mean_identity,
    AVG(perceived_injustice) AS mean_injustice,
    AVG(moral_outrage) AS mean_outrage,
    AVG(collective_efficacy) AS mean_efficacy,
    AVG(network_support) AS mean_network_support,
    AVG(participation_cost) AS mean_cost,
    AVG(perceived_repression_risk) AS mean_repression_risk,
    AVG(digital_engagement) AS mean_digital_engagement,
    AVG(offline_engagement) AS mean_offline_engagement,
    AVG(movement_outcome) AS mean_outcome
FROM collective_action_trials
GROUP BY condition;

DROP VIEW IF EXISTS domain_summary;
CREATE VIEW domain_summary AS
SELECT
    movement_domain,
    COUNT(*) AS n_trials,
    AVG(action_participation) AS participation_rate,
    AVG(participation_intention) AS mean_intention,
    AVG(perceived_injustice) AS mean_injustice,
    AVG(collective_efficacy) AS mean_efficacy,
    AVG(participation_cost) AS mean_cost,
    AVG(perceived_repression_risk) AS mean_repression_risk
FROM collective_action_trials
GROUP BY movement_domain;

DROP VIEW IF EXISTS high_cost_high_identity_cases;
CREATE VIEW high_cost_high_identity_cases AS
SELECT
    participant,
    group_id,
    condition,
    movement_domain,
    identity_strength,
    perceived_injustice,
    moral_outrage,
    collective_efficacy,
    network_support,
    participation_cost,
    perceived_repression_risk,
    participation_intention,
    action_participation
FROM collective_action_trials
WHERE identity_strength >= 7
  AND participation_cost >= 7;

DROP VIEW IF EXISTS digital_offline_gap;
CREATE VIEW digital_offline_gap AS
SELECT
    participant,
    group_id,
    condition,
    movement_domain,
    digital_engagement,
    offline_engagement,
    digital_engagement - offline_engagement AS digital_offline_difference,
    participation_cost,
    perceived_repression_risk,
    action_participation
FROM collective_action_trials;

DROP VIEW IF EXISTS network_exposure;
CREATE VIEW network_exposure AS
SELECT
    e.source_participant AS participant,
    COUNT(*) AS observed_ties,
    AVG(e.tie_strength) AS mean_tie_strength
FROM network_edges e
GROUP BY e.source_participant;
