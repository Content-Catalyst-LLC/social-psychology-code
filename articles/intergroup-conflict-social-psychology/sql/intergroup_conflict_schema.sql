-- Intergroup Conflict in Social Psychology
-- Relational schema for realistic conflict, social identity, status threat, symbolic threat, realistic threat, stereotypes, anxiety, dehumanization, contact, legitimacy, escalation, exclusion, and cooperation research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS groups_table;
DROP TABLE IF EXISTS group_dyads;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS intergroup_conflict_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE groups_table (
    group_id TEXT PRIMARY KEY,
    group_label TEXT,
    group_domain TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_dyads (
    dyad_id TEXT PRIMARY KEY,
    group_id TEXT NOT NULL,
    outgroup_id TEXT NOT NULL,
    relation_type TEXT,
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

CREATE TABLE intergroup_conflict_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    outgroup_id TEXT NOT NULL,
    dyad_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    context_type TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    resource_competition REAL NOT NULL CHECK (resource_competition >= 0 AND resource_competition <= 10),
    zero_sum_perception REAL NOT NULL CHECK (zero_sum_perception >= 0 AND zero_sum_perception <= 10),
    identity_salience REAL NOT NULL CHECK (identity_salience >= 0 AND identity_salience <= 10),
    group_identification REAL NOT NULL CHECK (group_identification >= 0 AND group_identification <= 10),
    status_threat REAL NOT NULL CHECK (status_threat >= 0 AND status_threat <= 10),
    symbolic_threat REAL NOT NULL CHECK (symbolic_threat >= 0 AND symbolic_threat <= 10),
    realistic_threat REAL NOT NULL CHECK (realistic_threat >= 0 AND realistic_threat <= 10),
    stereotype_endorsement REAL NOT NULL CHECK (stereotype_endorsement >= 0 AND stereotype_endorsement <= 10),
    outgroup_warmth REAL NOT NULL CHECK (outgroup_warmth >= 0 AND outgroup_warmth <= 10),
    outgroup_competence REAL NOT NULL CHECK (outgroup_competence >= 0 AND outgroup_competence <= 10),
    intergroup_anxiety REAL NOT NULL CHECK (intergroup_anxiety >= 0 AND intergroup_anxiety <= 10),
    perceived_injustice REAL NOT NULL CHECK (perceived_injustice >= 0 AND perceived_injustice <= 10),
    dehumanization REAL NOT NULL CHECK (dehumanization >= 0 AND dehumanization <= 10),
    perceived_legitimacy REAL NOT NULL CHECK (perceived_legitimacy >= 0 AND perceived_legitimacy <= 10),
    institutional_trust REAL NOT NULL CHECK (institutional_trust >= 0 AND institutional_trust <= 10),
    norm_of_retaliation REAL NOT NULL CHECK (norm_of_retaliation >= 0 AND norm_of_retaliation <= 10),
    group_polarization REAL NOT NULL CHECK (group_polarization >= 0 AND group_polarization <= 10),
    hostility_score REAL NOT NULL CHECK (hostility_score >= 0 AND hostility_score <= 100),
    aggression_intention REAL NOT NULL CHECK (aggression_intention >= 0 AND aggression_intention <= 100),
    avoidance_intention REAL NOT NULL CHECK (avoidance_intention >= 0 AND avoidance_intention <= 100),
    support_for_exclusion REAL NOT NULL CHECK (support_for_exclusion >= 0 AND support_for_exclusion <= 100),
    support_for_cooperation REAL NOT NULL CHECK (support_for_cooperation >= 0 AND support_for_cooperation <= 100),
    contact_quality REAL NOT NULL CHECK (contact_quality >= 0 AND contact_quality <= 10),
    equal_status REAL NOT NULL CHECK (equal_status >= 0 AND equal_status <= 10),
    common_goal_salience REAL NOT NULL CHECK (common_goal_salience >= 0 AND common_goal_salience <= 10),
    institutional_support REAL NOT NULL CHECK (institutional_support >= 0 AND institutional_support <= 10),
    cooperative_task_success REAL NOT NULL CHECK (cooperative_task_success >= 0 AND cooperative_task_success <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    material_conflict_index REAL GENERATED ALWAYS AS (
        (resource_competition + zero_sum_perception + realistic_threat) / 3.0
    ) VIRTUAL,
    identity_threat_index REAL GENERATED ALWAYS AS (
        (identity_salience + group_identification + status_threat + symbolic_threat) / 4.0
    ) VIRTUAL,
    cooperative_contact_index REAL GENERATED ALWAYS AS (
        (contact_quality + equal_status + common_goal_salience + institutional_support) / 4.0
    ) VIRTUAL,
    legitimacy_index REAL GENERATED ALWAYS AS (
        (perceived_legitimacy + institutional_trust) / 2.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE INDEX idx_ic_condition ON intergroup_conflict_trials(condition);
CREATE INDEX idx_ic_context ON intergroup_conflict_trials(context_type);
CREATE INDEX idx_ic_group ON intergroup_conflict_trials(group_id);
CREATE INDEX idx_ic_outgroup ON intergroup_conflict_trials(outgroup_id);
CREATE INDEX idx_ic_dyad ON intergroup_conflict_trials(dyad_id);
CREATE INDEX idx_ic_participant ON intergroup_conflict_trials(participant);

DROP VIEW IF EXISTS intergroup_conflict_summary;
CREATE VIEW intergroup_conflict_summary AS
SELECT
    condition,
    context_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    COUNT(DISTINCT dyad_id) AS n_dyads,
    AVG(hostility_score) AS mean_hostility,
    AVG(aggression_intention) AS mean_aggression,
    AVG(avoidance_intention) AS mean_avoidance,
    AVG(support_for_exclusion) AS mean_exclusion,
    AVG(support_for_cooperation) AS mean_cooperation,
    AVG(material_conflict_index) AS mean_material_conflict,
    AVG(identity_threat_index) AS mean_identity_threat,
    AVG(cooperative_contact_index) AS mean_contact,
    AVG(legitimacy_index) AS mean_legitimacy
FROM intergroup_conflict_trials
GROUP BY condition, context_type;

DROP VIEW IF EXISTS high_risk_escalation_cases;
CREATE VIEW high_risk_escalation_cases AS
SELECT
    participant,
    session_id,
    group_id,
    outgroup_id,
    dyad_id,
    condition,
    context_type,
    material_conflict_index,
    identity_threat_index,
    symbolic_threat,
    realistic_threat,
    dehumanization,
    norm_of_retaliation,
    group_polarization,
    hostility_score,
    aggression_intention,
    support_for_exclusion,
    support_for_cooperation
FROM intergroup_conflict_trials
WHERE hostility_score >= 75 OR aggression_intention >= 65 OR support_for_exclusion >= 70;
