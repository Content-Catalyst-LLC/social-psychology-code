-- Attribution Theory
-- Relational schema for causal explanation, dispositional attribution, situational attribution,
-- covariation reasoning, responsibility judgment, hostile attribution, and institutional blame.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS attribution_trials;

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
    behavior_domain TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE attribution_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    behavior_domain TEXT NOT NULL,
    target_type TEXT NOT NULL,
    self_other TEXT NOT NULL CHECK (self_other IN ('self', 'other')),
    outcome_valence TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    ambiguity_level REAL NOT NULL CHECK (ambiguity_level >= 0 AND ambiguity_level <= 10),
    intentionality REAL NOT NULL CHECK (intentionality >= 0 AND intentionality <= 10),
    perceived_choice REAL NOT NULL CHECK (perceived_choice >= 0 AND perceived_choice <= 10),
    perceived_effort REAL NOT NULL CHECK (perceived_effort >= 0 AND perceived_effort <= 10),
    perceived_ability REAL NOT NULL CHECK (perceived_ability >= 0 AND perceived_ability <= 10),
    situational_constraint REAL NOT NULL CHECK (situational_constraint >= 0 AND situational_constraint <= 10),
    consensus REAL NOT NULL CHECK (consensus >= 0 AND consensus <= 10),
    distinctiveness REAL NOT NULL CHECK (distinctiveness >= 0 AND distinctiveness <= 10),
    consistency REAL NOT NULL CHECK (consistency >= 0 AND consistency <= 10),
    attribution_internal REAL NOT NULL CHECK (attribution_internal >= 0 AND attribution_internal <= 100),
    attribution_external REAL NOT NULL CHECK (attribution_external >= 0 AND attribution_external <= 100),
    stability_rating REAL NOT NULL CHECK (stability_rating >= 0 AND stability_rating <= 10),
    controllability_rating REAL NOT NULL CHECK (controllability_rating >= 0 AND controllability_rating <= 10),
    responsibility_rating REAL NOT NULL CHECK (responsibility_rating >= 0 AND responsibility_rating <= 100),
    blame_rating REAL NOT NULL CHECK (blame_rating >= 0 AND blame_rating <= 100),
    sympathy_rating REAL NOT NULL CHECK (sympathy_rating >= 0 AND sympathy_rating <= 100),
    anger_rating REAL NOT NULL CHECK (anger_rating >= 0 AND anger_rating <= 100),
    punishment_support REAL NOT NULL CHECK (punishment_support >= 0 AND punishment_support <= 100),
    help_support REAL NOT NULL CHECK (help_support >= 0 AND help_support <= 100),
    achievement_expectation REAL NOT NULL CHECK (achievement_expectation >= 0 AND achievement_expectation <= 100),
    hostile_attribution_score REAL NOT NULL CHECK (hostile_attribution_score >= 0 AND hostile_attribution_score <= 100),
    attributional_complexity REAL NOT NULL CHECK (attributional_complexity >= 0 AND attributional_complexity <= 10),
    cultural_agency_orientation REAL NOT NULL CHECK (cultural_agency_orientation >= 0 AND cultural_agency_orientation <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    disposition_bias_index REAL GENERATED ALWAYS AS (
        attribution_internal - attribution_external
    ) VIRTUAL,
    covariation_situation_index REAL GENERATED ALWAYS AS (
        (consensus + distinctiveness + consistency) / 3.0
    ) VIRTUAL,
    responsibility_inference_index REAL GENERATED ALWAYS AS (
        (intentionality + perceived_choice + controllability_rating - situational_constraint) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES research_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_attr_condition ON attribution_trials(condition);
CREATE INDEX idx_attr_context ON attribution_trials(institution_context);
CREATE INDEX idx_attr_target ON attribution_trials(target_type);
CREATE INDEX idx_attr_valence ON attribution_trials(outcome_valence);
CREATE INDEX idx_attr_participant ON attribution_trials(participant);

DROP VIEW IF EXISTS attribution_summary;
CREATE VIEW attribution_summary AS
SELECT
    condition,
    target_type,
    outcome_valence,
    institution_context,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(attribution_internal) AS mean_internal,
    AVG(attribution_external) AS mean_external,
    AVG(disposition_bias_index) AS mean_disposition_bias,
    AVG(responsibility_rating) AS mean_responsibility,
    AVG(blame_rating) AS mean_blame,
    AVG(sympathy_rating) AS mean_sympathy,
    AVG(punishment_support) AS mean_punishment,
    AVG(help_support) AS mean_help,
    AVG(hostile_attribution_score) AS mean_hostile_attribution
FROM attribution_trials
GROUP BY condition, target_type, outcome_valence, institution_context;
