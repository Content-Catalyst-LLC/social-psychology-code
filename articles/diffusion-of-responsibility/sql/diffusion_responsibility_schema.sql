-- Diffusion of Responsibility in Social Psychology
-- Relational schema for bystander intervention, role clarity, and organizational accountability research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS diffusion_trials;
DROP TABLE IF EXISTS organizational_incidents;
DROP TABLE IF EXISTS accountability_assignments;

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

CREATE TABLE diffusion_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    scenario_domain TEXT NOT NULL,
    bystander_count INTEGER NOT NULL CHECK (bystander_count >= 0),
    group_size INTEGER NOT NULL CHECK (group_size >= 1),
    ambiguity_level REAL NOT NULL CHECK (ambiguity_level >= 0 AND ambiguity_level <= 10),
    private_concern REAL NOT NULL CHECK (private_concern >= 0 AND private_concern <= 10),
    perceived_group_concern REAL NOT NULL CHECK (perceived_group_concern >= 0 AND perceived_group_concern <= 10),
    evaluation_apprehension REAL NOT NULL CHECK (evaluation_apprehension >= 0 AND evaluation_apprehension <= 10),
    perceived_responsibility REAL NOT NULL CHECK (perceived_responsibility >= 0 AND perceived_responsibility <= 10),
    role_clarity REAL NOT NULL CHECK (role_clarity >= 0 AND role_clarity <= 10),
    intervention_efficacy REAL NOT NULL CHECK (intervention_efficacy >= 0 AND intervention_efficacy <= 10),
    social_visibility REAL NOT NULL CHECK (social_visibility >= 0 AND social_visibility <= 10),
    leadership_cue REAL NOT NULL CHECK (leadership_cue >= 0 AND leadership_cue <= 10),
    accountability_assignment REAL NOT NULL CHECK (accountability_assignment >= 0 AND accountability_assignment <= 10),
    organizational_fragmentation REAL NOT NULL CHECK (organizational_fragmentation >= 0 AND organizational_fragmentation <= 10),
    intervention_decision INTEGER NOT NULL CHECK (intervention_decision IN (0, 1)),
    reporting_decision INTEGER NOT NULL CHECK (reporting_decision IN (0, 1)),
    intervention_delay_seconds REAL NOT NULL CHECK (intervention_delay_seconds >= 0),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    pluralistic_ignorance_gap REAL GENERATED ALWAYS AS (private_concern - perceived_group_concern) VIRTUAL,
    responsibility_clarity_index REAL GENERATED ALWAYS AS ((role_clarity + accountability_assignment + leadership_cue) / 3.0) VIRTUAL,
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE organizational_incidents (
    incident_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    warning_signal_strength REAL CHECK (warning_signal_strength >= 0 AND warning_signal_strength <= 10),
    organizational_fragmentation REAL CHECK (organizational_fragmentation >= 0 AND organizational_fragmentation <= 10),
    ambiguity_level REAL CHECK (ambiguity_level >= 0 AND ambiguity_level <= 10),
    accountability_clarity REAL CHECK (accountability_clarity >= 0 AND accountability_clarity <= 10),
    response_delay_hours REAL CHECK (response_delay_hours >= 0),
    incident_date TEXT,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE accountability_assignments (
    assignment_id TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL,
    assigned_role TEXT NOT NULL,
    assignment_clarity REAL CHECK (assignment_clarity >= 0 AND assignment_clarity <= 10),
    response_authority REAL CHECK (response_authority >= 0 AND response_authority <= 10),
    escalation_path_clear INTEGER CHECK (escalation_path_clear IN (0, 1)),
    FOREIGN KEY (incident_id) REFERENCES organizational_incidents(incident_id)
);

CREATE INDEX idx_diff_condition ON diffusion_trials(condition);
CREATE INDEX idx_diff_domain ON diffusion_trials(scenario_domain);
CREATE INDEX idx_diff_participant ON diffusion_trials(participant);
CREATE INDEX idx_diff_bystanders ON diffusion_trials(bystander_count);
CREATE INDEX idx_diff_intervention ON diffusion_trials(intervention_decision);

DROP VIEW IF EXISTS diffusion_summary;
CREATE VIEW diffusion_summary AS
SELECT
    condition,
    scenario_domain,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(bystander_count) AS mean_bystanders,
    AVG(intervention_decision) AS intervention_rate,
    AVG(reporting_decision) AS reporting_rate,
    AVG(intervention_delay_seconds) AS mean_delay_seconds,
    AVG(perceived_responsibility) AS mean_responsibility,
    AVG(role_clarity) AS mean_role_clarity,
    AVG(ambiguity_level) AS mean_ambiguity,
    AVG(evaluation_apprehension) AS mean_evaluation,
    AVG(pluralistic_ignorance_gap) AS mean_pluralistic_gap
FROM diffusion_trials
GROUP BY condition, scenario_domain;

DROP VIEW IF EXISTS high_risk_diffusion_cases;
CREATE VIEW high_risk_diffusion_cases AS
SELECT
    participant,
    site_id,
    condition,
    scenario_domain,
    bystander_count,
    ambiguity_level,
    private_concern,
    perceived_group_concern,
    pluralistic_ignorance_gap,
    perceived_responsibility,
    role_clarity,
    accountability_assignment,
    organizational_fragmentation,
    intervention_decision,
    reporting_decision,
    intervention_delay_seconds
FROM diffusion_trials
WHERE private_concern >= 7
  AND perceived_responsibility <= 4
  AND intervention_decision = 0;
