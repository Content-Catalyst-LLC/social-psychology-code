-- Altruism in Social Psychology
-- Relational schema for empathy, costly helping, kinship, reciprocity, moral identity, warm-glow giving, public-goods contribution, and altruistic punishment research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS recipients;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS altruism_trials;

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

CREATE TABLE altruism_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    context_type TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    empathy_score REAL NOT NULL CHECK (empathy_score >= 0 AND empathy_score <= 10),
    personal_distress REAL NOT NULL CHECK (personal_distress >= 0 AND personal_distress <= 10),
    helping_cost REAL NOT NULL CHECK (helping_cost >= 0 AND helping_cost <= 10),
    recipient_need REAL NOT NULL CHECK (recipient_need >= 0 AND recipient_need <= 10),
    recipient_closeness REAL NOT NULL CHECK (recipient_closeness >= 0 AND recipient_closeness <= 10),
    identity_overlap REAL NOT NULL CHECK (identity_overlap >= 0 AND identity_overlap <= 10),
    kinship_coefficient REAL NOT NULL CHECK (kinship_coefficient >= 0 AND kinship_coefficient <= 1),
    reciprocity_expectation REAL NOT NULL CHECK (reciprocity_expectation >= 0 AND reciprocity_expectation <= 10),
    reputation_visibility REAL NOT NULL CHECK (reputation_visibility >= 0 AND reputation_visibility <= 10),
    moral_identity REAL NOT NULL CHECK (moral_identity >= 0 AND moral_identity <= 10),
    social_norm_salience REAL NOT NULL CHECK (social_norm_salience >= 0 AND social_norm_salience <= 10),
    warm_glow_expectation REAL NOT NULL CHECK (warm_glow_expectation >= 0 AND warm_glow_expectation <= 10),
    perceived_efficacy REAL NOT NULL CHECK (perceived_efficacy >= 0 AND perceived_efficacy <= 10),
    intervention_risk REAL NOT NULL CHECK (intervention_risk >= 0 AND intervention_risk <= 10),
    altruistic_decision INTEGER NOT NULL CHECK (altruistic_decision IN (0, 1)),
    donation_amount REAL NOT NULL CHECK (donation_amount >= 0 AND donation_amount <= 100),
    time_volunteered_minutes REAL NOT NULL CHECK (time_volunteered_minutes >= 0),
    altruistic_punishment INTEGER NOT NULL CHECK (altruistic_punishment IN (0, 1)),
    punishment_cost REAL NOT NULL CHECK (punishment_cost >= 0 AND punishment_cost <= 100),
    public_goods_contribution REAL NOT NULL CHECK (public_goods_contribution >= 0 AND public_goods_contribution <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    other_regarding_weight REAL GENERATED ALWAYS AS (
        (empathy_score + recipient_need + identity_overlap + moral_identity + perceived_efficacy - helping_cost - intervention_risk) / 5.0
    ) VIRTUAL,
    egoistic_reward_index REAL GENERATED ALWAYS AS (
        (reciprocity_expectation + reputation_visibility + warm_glow_expectation) / 3.0
    ) VIRTUAL,
    cost_pressure_index REAL GENERATED ALWAYS AS (
        (helping_cost + intervention_risk + personal_distress) / 3.0
    ) VIRTUAL,
    inclusive_fitness_score REAL GENERATED ALWAYS AS (
        kinship_coefficient * recipient_need - helping_cost / 10.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (recipient_id) REFERENCES recipients(recipient_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_alt_condition ON altruism_trials(condition);
CREATE INDEX idx_alt_context ON altruism_trials(context_type);
CREATE INDEX idx_alt_participant ON altruism_trials(participant);
CREATE INDEX idx_alt_recipient ON altruism_trials(recipient_id);
CREATE INDEX idx_alt_empathy ON altruism_trials(empathy_score);

DROP VIEW IF EXISTS altruism_summary;
CREATE VIEW altruism_summary AS
SELECT
    condition,
    context_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(altruistic_decision) AS altruism_rate,
    AVG(altruistic_punishment) AS punishment_rate,
    AVG(donation_amount) AS mean_donation,
    AVG(time_volunteered_minutes) AS mean_volunteer_minutes,
    AVG(public_goods_contribution) AS mean_public_goods_contribution,
    AVG(empathy_score) AS mean_empathy,
    AVG(helping_cost) AS mean_helping_cost,
    AVG(recipient_need) AS mean_recipient_need,
    AVG(identity_overlap) AS mean_identity_overlap,
    AVG(moral_identity) AS mean_moral_identity,
    AVG(perceived_efficacy) AS mean_efficacy,
    AVG(other_regarding_weight) AS mean_other_regarding_weight,
    AVG(egoistic_reward_index) AS mean_egoistic_reward
FROM altruism_trials
GROUP BY condition, context_type;

DROP VIEW IF EXISTS high_cost_helping_cases;
CREATE VIEW high_cost_helping_cases AS
SELECT
    participant,
    session_id,
    recipient_id,
    scenario_id,
    condition,
    context_type,
    empathy_score,
    helping_cost,
    recipient_need,
    identity_overlap,
    moral_identity,
    perceived_efficacy,
    reputation_visibility,
    reciprocity_expectation,
    altruistic_decision,
    donation_amount,
    time_volunteered_minutes
FROM altruism_trials
WHERE helping_cost >= 7 AND altruistic_decision = 1;
