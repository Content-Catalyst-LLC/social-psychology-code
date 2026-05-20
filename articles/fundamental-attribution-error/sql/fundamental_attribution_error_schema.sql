-- Fundamental Attribution Error
-- Relational schema for attribution, constraint recognition, blame, and punishment research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS attribution_trials;
DROP TABLE IF EXISTS institutional_cases;
DROP TABLE IF EXISTS accountability_reviews;

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

CREATE TABLE attribution_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    actor_role TEXT NOT NULL,
    observer_role TEXT NOT NULL,
    behavior_valence TEXT NOT NULL,
    dispositional_attribution REAL NOT NULL CHECK (dispositional_attribution >= 0 AND dispositional_attribution <= 10),
    situational_attribution REAL NOT NULL CHECK (situational_attribution >= 0 AND situational_attribution <= 10),
    perceived_constraint REAL NOT NULL CHECK (perceived_constraint >= 0 AND perceived_constraint <= 10),
    actual_constraint REAL NOT NULL CHECK (actual_constraint >= 0 AND actual_constraint <= 10),
    choice_freedom REAL NOT NULL CHECK (choice_freedom >= 0 AND choice_freedom <= 10),
    correspondence_inference REAL NOT NULL CHECK (correspondence_inference >= 0 AND correspondence_inference <= 10),
    cognitive_load REAL NOT NULL CHECK (cognitive_load >= 0 AND cognitive_load <= 10),
    perspective_taking REAL NOT NULL CHECK (perspective_taking >= 0 AND perspective_taking <= 10),
    accountability_pressure REAL NOT NULL CHECK (accountability_pressure >= 0 AND accountability_pressure <= 10),
    evidence_strength REAL NOT NULL CHECK (evidence_strength >= 0 AND evidence_strength <= 10),
    empathy REAL NOT NULL CHECK (empathy >= 0 AND empathy <= 10),
    moral_blame REAL NOT NULL CHECK (moral_blame >= 0 AND moral_blame <= 10),
    punishment_recommendation REAL NOT NULL CHECK (punishment_recommendation >= 0 AND punishment_recommendation <= 10),
    cultural_individualism REAL NOT NULL CHECK (cultural_individualism >= 0 AND cultural_individualism <= 10),
    structural_awareness REAL NOT NULL CHECK (structural_awareness >= 0 AND structural_awareness <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    fae_score REAL GENERATED ALWAYS AS (dispositional_attribution - situational_attribution) VIRTUAL,
    constraint_neglect REAL GENERATED ALWAYS AS (actual_constraint - perceived_constraint) VIRTUAL,
    correspondence_bias_score REAL GENERATED ALWAYS AS (correspondence_inference - choice_freedom) VIRTUAL,
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE institutional_cases (
    case_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    case_type TEXT NOT NULL,
    actual_constraint REAL CHECK (actual_constraint >= 0 AND actual_constraint <= 10),
    perceived_constraint REAL CHECK (perceived_constraint >= 0 AND perceived_constraint <= 10),
    dispositional_attribution REAL CHECK (dispositional_attribution >= 0 AND dispositional_attribution <= 10),
    situational_attribution REAL CHECK (situational_attribution >= 0 AND situational_attribution <= 10),
    moral_blame REAL CHECK (moral_blame >= 0 AND moral_blame <= 10),
    punishment_recommendation REAL CHECK (punishment_recommendation >= 0 AND punishment_recommendation <= 10),
    case_date TEXT,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE accountability_reviews (
    review_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    accountability_pressure REAL CHECK (accountability_pressure >= 0 AND accountability_pressure <= 10),
    evidence_review_quality REAL CHECK (evidence_review_quality >= 0 AND evidence_review_quality <= 10),
    constraint_salience REAL CHECK (constraint_salience >= 0 AND constraint_salience <= 10),
    corrected_judgment INTEGER CHECK (corrected_judgment IN (0, 1)),
    FOREIGN KEY (case_id) REFERENCES institutional_cases(case_id)
);

CREATE INDEX idx_attr_condition ON attribution_trials(condition);
CREATE INDEX idx_attr_valence ON attribution_trials(behavior_valence);
CREATE INDEX idx_attr_actor ON attribution_trials(actor_role);
CREATE INDEX idx_attr_observer ON attribution_trials(observer_role);
CREATE INDEX idx_attr_participant ON attribution_trials(participant);

DROP VIEW IF EXISTS attribution_summary;
CREATE VIEW attribution_summary AS
SELECT
    condition,
    behavior_valence,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(dispositional_attribution) AS mean_dispositional,
    AVG(situational_attribution) AS mean_situational,
    AVG(fae_score) AS mean_fae_score,
    AVG(constraint_neglect) AS mean_constraint_neglect,
    AVG(correspondence_bias_score) AS mean_correspondence_bias,
    AVG(moral_blame) AS mean_blame,
    AVG(punishment_recommendation) AS mean_punishment,
    AVG(empathy) AS mean_empathy
FROM attribution_trials
GROUP BY condition, behavior_valence;

DROP VIEW IF EXISTS high_risk_dispositional_cases;
CREATE VIEW high_risk_dispositional_cases AS
SELECT
    participant,
    site_id,
    condition,
    actor_role,
    observer_role,
    behavior_valence,
    dispositional_attribution,
    situational_attribution,
    perceived_constraint,
    actual_constraint,
    constraint_neglect,
    moral_blame,
    punishment_recommendation
FROM attribution_trials
WHERE dispositional_attribution >= 7
  AND actual_constraint >= 7
  AND perceived_constraint <= 4;
