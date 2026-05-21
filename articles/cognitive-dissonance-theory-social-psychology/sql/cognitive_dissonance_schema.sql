-- Cognitive Dissonance Theory
-- Relational schema for forced compliance, post-decision dissonance, effort justification,
-- belief disconfirmation, self-affirmation, response latency, and institutional escalation.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS dissonance_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_groups (
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

CREATE TABLE dissonance_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    paradigm TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    pre_attitude REAL NOT NULL CHECK (pre_attitude >= -100 AND pre_attitude <= 100),
    post_attitude REAL NOT NULL CHECK (post_attitude >= -100 AND post_attitude <= 100),
    counter_attitudinal_behavior REAL NOT NULL CHECK (counter_attitudinal_behavior >= 0 AND counter_attitudinal_behavior <= 10),
    perceived_choice REAL NOT NULL CHECK (perceived_choice >= 0 AND perceived_choice <= 10),
    perceived_responsibility REAL NOT NULL CHECK (perceived_responsibility >= 0 AND perceived_responsibility <= 10),
    identity_threat REAL NOT NULL CHECK (identity_threat >= 0 AND identity_threat <= 10),
    self_affirmation REAL NOT NULL CHECK (self_affirmation >= 0 AND self_affirmation <= 10),
    external_justification REAL NOT NULL CHECK (external_justification >= 0 AND external_justification <= 10),
    public_commitment REAL NOT NULL CHECK (public_commitment >= 0 AND public_commitment <= 10),
    effort_cost REAL NOT NULL CHECK (effort_cost >= 0 AND effort_cost <= 10),
    outcome_value REAL NOT NULL CHECK (outcome_value >= 0 AND outcome_value <= 100),
    chosen_pre_value REAL NOT NULL CHECK (chosen_pre_value >= 0 AND chosen_pre_value <= 100),
    chosen_post_value REAL NOT NULL CHECK (chosen_post_value >= 0 AND chosen_post_value <= 100),
    rejected_pre_value REAL NOT NULL CHECK (rejected_pre_value >= 0 AND rejected_pre_value <= 100),
    rejected_post_value REAL NOT NULL CHECK (rejected_post_value >= 0 AND rejected_post_value <= 100),
    belief_disconfirmation_strength REAL NOT NULL CHECK (belief_disconfirmation_strength >= 0 AND belief_disconfirmation_strength <= 10),
    commitment_strength REAL NOT NULL CHECK (commitment_strength >= 0 AND commitment_strength <= 10),
    proselytizing_intensity REAL NOT NULL CHECK (proselytizing_intensity >= 0 AND proselytizing_intensity <= 100),
    coherence_pressure REAL NOT NULL CHECK (coherence_pressure >= 0 AND coherence_pressure <= 10),
    dissonance_discomfort REAL NOT NULL CHECK (dissonance_discomfort >= 0 AND dissonance_discomfort <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    institutional_identity_threat REAL NOT NULL CHECK (institutional_identity_threat >= 0 AND institutional_identity_threat <= 10),
    sunk_cost REAL NOT NULL CHECK (sunk_cost >= 0 AND sunk_cost <= 10),
    evidence_strength REAL NOT NULL CHECK (evidence_strength >= 0 AND evidence_strength <= 10),
    accountability REAL NOT NULL CHECK (accountability >= 0 AND accountability <= 10),
    policy_reversal_willingness REAL NOT NULL CHECK (policy_reversal_willingness >= 0 AND policy_reversal_willingness <= 100),
    attitude_change REAL GENERATED ALWAYS AS (
        post_attitude - pre_attitude
    ) VIRTUAL,
    spreading_of_alternatives REAL GENERATED ALWAYS AS (
        (chosen_post_value - chosen_pre_value) - (rejected_post_value - rejected_pre_value)
    ) VIRTUAL,
    dissonance_magnitude_index REAL GENERATED ALWAYS AS (
        (counter_attitudinal_behavior + perceived_choice + perceived_responsibility + identity_threat + public_commitment - external_justification - self_affirmation) / 5.0
    ) VIRTUAL,
    institutional_escalation_index REAL GENERATED ALWAYS AS (
        (sunk_cost + public_commitment + institutional_identity_threat - evidence_strength - accountability) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES research_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_dissonance_paradigm ON dissonance_trials(paradigm);
CREATE INDEX idx_dissonance_condition ON dissonance_trials(condition);
CREATE INDEX idx_dissonance_context ON dissonance_trials(institution_context);
CREATE INDEX idx_dissonance_participant ON dissonance_trials(participant);

DROP VIEW IF EXISTS dissonance_summary;
CREATE VIEW dissonance_summary AS
SELECT
    paradigm,
    condition,
    institution_context,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(attitude_change) AS mean_attitude_change,
    AVG(spreading_of_alternatives) AS mean_spreading,
    AVG(outcome_value) AS mean_outcome_value,
    AVG(proselytizing_intensity) AS mean_proselytizing,
    AVG(coherence_pressure) AS mean_coherence_pressure,
    AVG(dissonance_discomfort) AS mean_discomfort,
    AVG(policy_reversal_willingness) AS mean_policy_reversal
FROM dissonance_trials
GROUP BY paradigm, condition, institution_context;
