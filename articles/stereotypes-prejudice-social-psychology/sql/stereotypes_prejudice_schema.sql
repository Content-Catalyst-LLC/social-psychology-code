-- Stereotypes, Prejudice, and Discrimination
-- Relational schema for stereotype strength, prejudice, discrimination tendency,
-- contact, stereotype threat, stereotype content, and cumulative institutional inequality.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS stereotypes_prejudice_trials;

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

CREATE TABLE stereotypes_prejudice_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    target_group TEXT NOT NULL,
    evaluator_group TEXT NOT NULL,
    stereotype_strength REAL NOT NULL CHECK (stereotype_strength >= 0 AND stereotype_strength <= 10),
    warmth_rating REAL NOT NULL CHECK (warmth_rating >= 0 AND warmth_rating <= 10),
    competence_rating REAL NOT NULL CHECK (competence_rating >= 0 AND competence_rating <= 10),
    prejudice_rating REAL NOT NULL CHECK (prejudice_rating >= 0 AND prejudice_rating <= 10),
    perceived_threat REAL NOT NULL CHECK (perceived_threat >= 0 AND perceived_threat <= 10),
    perceived_competition REAL NOT NULL CHECK (perceived_competition >= 0 AND perceived_competition <= 10),
    perceived_status REAL NOT NULL CHECK (perceived_status >= 0 AND perceived_status <= 10),
    social_distance REAL NOT NULL CHECK (social_distance >= 0 AND social_distance <= 10),
    contact_quality REAL NOT NULL CHECK (contact_quality >= 0 AND contact_quality <= 10),
    contact_quantity REAL NOT NULL CHECK (contact_quantity >= 0 AND contact_quantity <= 10),
    institutional_support REAL NOT NULL CHECK (institutional_support >= 0 AND institutional_support <= 10),
    stereotype_threat_salience REAL NOT NULL CHECK (stereotype_threat_salience >= 0 AND stereotype_threat_salience <= 10),
    identity_safety REAL NOT NULL CHECK (identity_safety >= 0 AND identity_safety <= 10),
    implicit_score REAL NOT NULL CHECK (implicit_score >= -3 AND implicit_score <= 3),
    explicit_attitude REAL NOT NULL CHECK (explicit_attitude >= -100 AND explicit_attitude <= 100),
    discrimination_tendency REAL NOT NULL CHECK (discrimination_tendency >= 0 AND discrimination_tendency <= 100),
    behavioral_outcome REAL NOT NULL CHECK (behavioral_outcome >= 0 AND behavioral_outcome <= 100),
    performance_score REAL NOT NULL CHECK (performance_score >= 0 AND performance_score <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 250),
    structured_criteria REAL NOT NULL CHECK (structured_criteria >= 0 AND structured_criteria <= 10),
    accountability REAL NOT NULL CHECK (accountability >= 0 AND accountability <= 10),
    contact_support_index REAL GENERATED ALWAYS AS (
        (contact_quality + contact_quantity + institutional_support) / 3.0
    ) VIRTUAL,
    threat_competition_index REAL GENERATED ALWAYS AS (
        (perceived_threat + perceived_competition) / 2.0
    ) VIRTUAL,
    decision_structure_index REAL GENERATED ALWAYS AS (
        (structured_criteria + accountability) / 2.0
    ) VIRTUAL,
    stereotype_content_asymmetry REAL GENERATED ALWAYS AS (
        competence_rating - warmth_rating
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES research_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_sp_condition ON stereotypes_prejudice_trials(condition);
CREATE INDEX idx_sp_context ON stereotypes_prejudice_trials(institution_context);
CREATE INDEX idx_sp_target ON stereotypes_prejudice_trials(target_group);
CREATE INDEX idx_sp_participant ON stereotypes_prejudice_trials(participant);

DROP VIEW IF EXISTS stereotypes_prejudice_summary;
CREATE VIEW stereotypes_prejudice_summary AS
SELECT
    condition,
    institution_context,
    target_group,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(stereotype_strength) AS mean_stereotype_strength,
    AVG(warmth_rating) AS mean_warmth,
    AVG(competence_rating) AS mean_competence,
    AVG(prejudice_rating) AS mean_prejudice,
    AVG(discrimination_tendency) AS mean_discrimination,
    AVG(behavioral_outcome) AS mean_behavioral_outcome,
    AVG(performance_score) AS mean_performance,
    AVG(contact_support_index) AS mean_contact_support,
    AVG(threat_competition_index) AS mean_threat_competition,
    AVG(decision_structure_index) AS mean_decision_structure
FROM stereotypes_prejudice_trials
GROUP BY condition, institution_context, target_group;

DROP VIEW IF EXISTS high_disparity_risk_cases;
CREATE VIEW high_disparity_risk_cases AS
SELECT
    participant,
    session_id,
    group_id,
    scenario_id,
    condition,
    institution_context,
    target_group,
    stereotype_strength,
    prejudice_rating,
    perceived_threat,
    implicit_score,
    discrimination_tendency,
    behavioral_outcome,
    decision_structure_index,
    contact_support_index
FROM stereotypes_prejudice_trials
WHERE discrimination_tendency >= 65
  AND decision_structure_index <= 4;
