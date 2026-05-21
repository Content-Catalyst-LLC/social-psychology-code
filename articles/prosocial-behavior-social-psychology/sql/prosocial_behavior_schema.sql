-- Prosocial Behavior in Social Psychology
-- Relational schema for helping, cooperation, donation, volunteering, emotional support, public-goods contribution, bystander effects, norms, efficacy, trust, and institutional legitimacy research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS recipients;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS prosocial_behavior_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipients (
    recipient_id TEXT PRIMARY KEY,
    recipient_type TEXT,
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

CREATE TABLE prosocial_behavior_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    context_type TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    empathy_score REAL NOT NULL CHECK (empathy_score >= 0 AND empathy_score <= 10),
    perspective_taking REAL NOT NULL CHECK (perspective_taking >= 0 AND perspective_taking <= 10),
    norm_salience REAL NOT NULL CHECK (norm_salience >= 0 AND norm_salience <= 10),
    reciprocity_expectation REAL NOT NULL CHECK (reciprocity_expectation >= 0 AND reciprocity_expectation <= 10),
    efficacy_belief REAL NOT NULL CHECK (efficacy_belief >= 0 AND efficacy_belief <= 10),
    helping_cost REAL NOT NULL CHECK (helping_cost >= 0 AND helping_cost <= 10),
    intervention_risk REAL NOT NULL CHECK (intervention_risk >= 0 AND intervention_risk <= 10),
    bystander_count INTEGER NOT NULL CHECK (bystander_count >= 0),
    felt_responsibility REAL NOT NULL CHECK (felt_responsibility >= 0 AND felt_responsibility <= 10),
    identity_overlap REAL NOT NULL CHECK (identity_overlap >= 0 AND identity_overlap <= 10),
    group_identification REAL NOT NULL CHECK (group_identification >= 0 AND group_identification <= 10),
    trust_level REAL NOT NULL CHECK (trust_level >= 0 AND trust_level <= 10),
    moral_identity REAL NOT NULL CHECK (moral_identity >= 0 AND moral_identity <= 10),
    reputation_visibility REAL NOT NULL CHECK (reputation_visibility >= 0 AND reputation_visibility <= 10),
    institutional_legitimacy REAL NOT NULL CHECK (institutional_legitimacy >= 0 AND institutional_legitimacy <= 10),
    helping_decision INTEGER NOT NULL CHECK (helping_decision IN (0, 1)),
    donation_amount REAL NOT NULL CHECK (donation_amount >= 0 AND donation_amount <= 100),
    volunteer_minutes REAL NOT NULL CHECK (volunteer_minutes >= 0),
    cooperation_contribution REAL NOT NULL CHECK (cooperation_contribution >= 0 AND cooperation_contribution <= 100),
    emotional_support INTEGER NOT NULL CHECK (emotional_support IN (0, 1)),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    log_bystanders REAL GENERATED ALWAYS AS (log(bystander_count + 1)) VIRTUAL,
    prosocial_motivation_index REAL GENERATED ALWAYS AS (
        (empathy_score + perspective_taking + norm_salience + efficacy_belief + felt_responsibility + moral_identity - helping_cost - intervention_risk) / 6.0
    ) VIRTUAL,
    social_embeddedness_index REAL GENERATED ALWAYS AS (
        (identity_overlap + group_identification + trust_level + institutional_legitimacy + reciprocity_expectation) / 5.0
    ) VIRTUAL,
    cost_pressure_index REAL GENERATED ALWAYS AS (
        (helping_cost + intervention_risk + log(bystander_count + 1)) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (recipient_id) REFERENCES recipients(recipient_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_pb_condition ON prosocial_behavior_trials(condition);
CREATE INDEX idx_pb_context ON prosocial_behavior_trials(context_type);
CREATE INDEX idx_pb_participant ON prosocial_behavior_trials(participant);
CREATE INDEX idx_pb_recipient ON prosocial_behavior_trials(recipient_id);
CREATE INDEX idx_pb_bystanders ON prosocial_behavior_trials(bystander_count);

DROP VIEW IF EXISTS prosocial_behavior_summary;
CREATE VIEW prosocial_behavior_summary AS
SELECT
    condition,
    context_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(helping_decision) AS helping_rate,
    AVG(emotional_support) AS emotional_support_rate,
    AVG(donation_amount) AS mean_donation,
    AVG(volunteer_minutes) AS mean_volunteer_minutes,
    AVG(cooperation_contribution) AS mean_cooperation_contribution,
    AVG(empathy_score) AS mean_empathy,
    AVG(norm_salience) AS mean_norm_salience,
    AVG(efficacy_belief) AS mean_efficacy,
    AVG(helping_cost) AS mean_helping_cost,
    AVG(bystander_count) AS mean_bystander_count,
    AVG(felt_responsibility) AS mean_felt_responsibility,
    AVG(institutional_legitimacy) AS mean_institutional_legitimacy
FROM prosocial_behavior_trials
GROUP BY condition, context_type;

DROP VIEW IF EXISTS low_legitimacy_cooperation_cases;
CREATE VIEW low_legitimacy_cooperation_cases AS
SELECT
    participant,
    session_id,
    recipient_id,
    scenario_id,
    condition,
    context_type,
    institutional_legitimacy,
    trust_level,
    norm_salience,
    efficacy_belief,
    helping_decision,
    cooperation_contribution,
    donation_amount,
    volunteer_minutes
FROM prosocial_behavior_trials
WHERE institutional_legitimacy <= 3 OR trust_level <= 3;
