-- In-Group Bias in Social Psychology
-- Relational schema for trust, fairness, moral judgment, and allocation research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS ingroup_bias_trials;
DROP TABLE IF EXISTS institutional_decisions;
DROP TABLE IF EXISTS group_network_edges;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    primary_group TEXT,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_sites (
    site_id TEXT PRIMARY KEY,
    site_type TEXT,
    location_code TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ingroup_bias_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    target_group_relation TEXT NOT NULL CHECK (target_group_relation IN ('ingroup', 'outgroup', 'neutral')),
    ingroup_target INTEGER NOT NULL CHECK (ingroup_target IN (0, 1)),
    group_identification REAL NOT NULL CHECK (group_identification >= 0 AND group_identification <= 10),
    identity_salience REAL NOT NULL CHECK (identity_salience >= 0 AND identity_salience <= 10),
    perceived_threat REAL NOT NULL CHECK (perceived_threat >= 0 AND perceived_threat <= 10),
    norm_strength REAL NOT NULL CHECK (norm_strength >= 0 AND norm_strength <= 10),
    status_asymmetry REAL NOT NULL CHECK (status_asymmetry >= 0 AND status_asymmetry <= 10),
    trust_rating REAL NOT NULL CHECK (trust_rating >= 0 AND trust_rating <= 10),
    fairness_rating REAL NOT NULL CHECK (fairness_rating >= 0 AND fairness_rating <= 10),
    competence_rating REAL NOT NULL CHECK (competence_rating >= 0 AND competence_rating <= 10),
    warmth_rating REAL NOT NULL CHECK (warmth_rating >= 0 AND warmth_rating <= 10),
    empathy_rating REAL NOT NULL CHECK (empathy_rating >= 0 AND empathy_rating <= 10),
    moral_blame REAL NOT NULL CHECK (moral_blame >= 0 AND moral_blame <= 10),
    moral_forgiveness REAL NOT NULL CHECK (moral_forgiveness >= 0 AND moral_forgiveness <= 10),
    punishment_severity REAL NOT NULL CHECK (punishment_severity >= 0 AND punishment_severity <= 10),
    reward_allocation REAL NOT NULL CHECK (reward_allocation >= 0 AND reward_allocation <= 100),
    resource_allocation REAL NOT NULL CHECK (resource_allocation >= 0 AND resource_allocation <= 100),
    cooperation_choice INTEGER NOT NULL CHECK (cooperation_choice IN (0, 1)),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    institutional_context TEXT NOT NULL,
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE institutional_decisions (
    decision_id TEXT PRIMARY KEY,
    participant TEXT,
    site_id TEXT,
    institutional_context TEXT NOT NULL,
    target_group_relation TEXT NOT NULL,
    selection_score REAL,
    selected INTEGER CHECK (selected IN (0, 1)),
    decision_date TEXT,
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE group_network_edges (
    source_participant TEXT NOT NULL,
    target_participant TEXT NOT NULL,
    tie_type TEXT NOT NULL DEFAULT 'ingroup_tie',
    tie_strength REAL CHECK (tie_strength >= 0 AND tie_strength <= 10),
    same_group INTEGER CHECK (same_group IN (0, 1)),
    observed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_participant, target_participant, tie_type)
);

CREATE INDEX idx_bias_condition ON ingroup_bias_trials(condition);
CREATE INDEX idx_bias_target_relation ON ingroup_bias_trials(target_group_relation);
CREATE INDEX idx_bias_ingroup_target ON ingroup_bias_trials(ingroup_target);
CREATE INDEX idx_bias_context ON ingroup_bias_trials(institutional_context);
CREATE INDEX idx_bias_participant ON ingroup_bias_trials(participant);
CREATE INDEX idx_decision_context ON institutional_decisions(institutional_context);

DROP VIEW IF EXISTS target_relation_summary;
CREATE VIEW target_relation_summary AS
SELECT
    condition,
    target_group_relation,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(trust_rating) AS mean_trust,
    AVG(fairness_rating) AS mean_fairness,
    AVG(competence_rating) AS mean_competence,
    AVG(warmth_rating) AS mean_warmth,
    AVG(empathy_rating) AS mean_empathy,
    AVG(moral_blame) AS mean_blame,
    AVG(moral_forgiveness) AS mean_forgiveness,
    AVG(punishment_severity) AS mean_punishment,
    AVG(reward_allocation) AS mean_reward,
    AVG(resource_allocation) AS mean_resource,
    AVG(cooperation_choice) AS cooperation_rate
FROM ingroup_bias_trials
GROUP BY condition, target_group_relation;

DROP VIEW IF EXISTS high_bias_cases;
CREATE VIEW high_bias_cases AS
SELECT
    participant,
    site_id,
    condition,
    institutional_context,
    target_group_relation,
    identity_salience,
    perceived_threat,
    norm_strength,
    trust_rating,
    fairness_rating,
    resource_allocation,
    moral_blame,
    punishment_severity
FROM ingroup_bias_trials
WHERE identity_salience >= 7
  AND perceived_threat >= 7;
