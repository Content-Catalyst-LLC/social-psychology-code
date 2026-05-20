-- Moral Disengagement in Social Psychology
-- Relational schema for moral self-regulation, harmful choices, and institutional normalization research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS moral_disengagement_trials;
DROP TABLE IF EXISTS institutional_harm_cases;
DROP TABLE IF EXISTS accountability_interventions;

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

CREATE TABLE moral_disengagement_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    scenario_domain TEXT NOT NULL,
    moral_justification REAL NOT NULL CHECK (moral_justification >= 0 AND moral_justification <= 10),
    euphemistic_labeling REAL NOT NULL CHECK (euphemistic_labeling >= 0 AND euphemistic_labeling <= 10),
    advantageous_comparison REAL NOT NULL CHECK (advantageous_comparison >= 0 AND advantageous_comparison <= 10),
    displaced_responsibility REAL NOT NULL CHECK (displaced_responsibility >= 0 AND displaced_responsibility <= 10),
    diffused_responsibility REAL NOT NULL CHECK (diffused_responsibility >= 0 AND diffused_responsibility <= 10),
    consequence_distortion REAL NOT NULL CHECK (consequence_distortion >= 0 AND consequence_distortion <= 10),
    dehumanization REAL NOT NULL CHECK (dehumanization >= 0 AND dehumanization <= 10),
    blame_attribution REAL NOT NULL CHECK (blame_attribution >= 0 AND blame_attribution <= 10),
    harm_visibility REAL NOT NULL CHECK (harm_visibility >= 0 AND harm_visibility <= 10),
    perceived_agency REAL NOT NULL CHECK (perceived_agency >= 0 AND perceived_agency <= 10),
    responsibility_clarity REAL NOT NULL CHECK (responsibility_clarity >= 0 AND responsibility_clarity <= 10),
    institutional_pressure REAL NOT NULL CHECK (institutional_pressure >= 0 AND institutional_pressure <= 10),
    authority_pressure REAL NOT NULL CHECK (authority_pressure >= 0 AND authority_pressure <= 10),
    group_norm_strength REAL NOT NULL CHECK (group_norm_strength >= 0 AND group_norm_strength <= 10),
    victim_distance REAL NOT NULL CHECK (victim_distance >= 0 AND victim_distance <= 10),
    empathy REAL NOT NULL CHECK (empathy >= 0 AND empathy <= 10),
    guilt REAL NOT NULL CHECK (guilt >= 0 AND guilt <= 10),
    harmful_decision INTEGER NOT NULL CHECK (harmful_decision IN (0, 1)),
    policy_endorsement REAL NOT NULL CHECK (policy_endorsement >= 0 AND policy_endorsement <= 10),
    unethical_intention REAL NOT NULL CHECK (unethical_intention >= 0 AND unethical_intention <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    md_index REAL GENERATED ALWAYS AS (
        (moral_justification + euphemistic_labeling + advantageous_comparison +
         displaced_responsibility + diffused_responsibility + consequence_distortion +
         dehumanization + blame_attribution) / 8.0
    ) VIRTUAL,
    agency_reduction_index REAL GENERATED ALWAYS AS (
        (displaced_responsibility + diffused_responsibility) / 2.0
    ) VIRTUAL,
    target_denigration_index REAL GENERATED ALWAYS AS (
        (dehumanization + blame_attribution) / 2.0
    ) VIRTUAL,
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE institutional_harm_cases (
    case_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    normalized_harm REAL CHECK (normalized_harm >= 0 AND normalized_harm <= 10),
    mean_moral_disengagement REAL CHECK (mean_moral_disengagement >= 0 AND mean_moral_disengagement <= 10),
    accountability_strength REAL CHECK (accountability_strength >= 0 AND accountability_strength <= 10),
    dissent_protection REAL CHECK (dissent_protection >= 0 AND dissent_protection <= 10),
    reward_for_harm REAL CHECK (reward_for_harm >= 0 AND reward_for_harm <= 10),
    case_date TEXT,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE accountability_interventions (
    intervention_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    intervention_type TEXT NOT NULL,
    harm_visibility_change REAL CHECK (harm_visibility_change >= -10 AND harm_visibility_change <= 10),
    responsibility_clarity_change REAL CHECK (responsibility_clarity_change >= -10 AND responsibility_clarity_change <= 10),
    dissent_protection_change REAL CHECK (dissent_protection_change >= -10 AND dissent_protection_change <= 10),
    harmful_rate_change REAL,
    FOREIGN KEY (case_id) REFERENCES institutional_harm_cases(case_id)
);

CREATE INDEX idx_md_condition ON moral_disengagement_trials(condition);
CREATE INDEX idx_md_domain ON moral_disengagement_trials(scenario_domain);
CREATE INDEX idx_md_participant ON moral_disengagement_trials(participant);
CREATE INDEX idx_md_harmful ON moral_disengagement_trials(harmful_decision);

DROP VIEW IF EXISTS moral_disengagement_summary;
CREATE VIEW moral_disengagement_summary AS
SELECT
    condition,
    scenario_domain,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(md_index) AS mean_md_index,
    AVG(harmful_decision) AS harmful_rate,
    AVG(policy_endorsement) AS mean_policy_endorsement,
    AVG(unethical_intention) AS mean_unethical_intention,
    AVG(empathy) AS mean_empathy,
    AVG(guilt) AS mean_guilt,
    AVG(harm_visibility) AS mean_harm_visibility,
    AVG(responsibility_clarity) AS mean_responsibility_clarity,
    AVG(institutional_pressure) AS mean_institutional_pressure,
    AVG(authority_pressure) AS mean_authority_pressure
FROM moral_disengagement_trials
GROUP BY condition, scenario_domain;

DROP VIEW IF EXISTS high_disengagement_harm_cases;
CREATE VIEW high_disengagement_harm_cases AS
SELECT
    participant,
    site_id,
    condition,
    scenario_domain,
    md_index,
    moral_justification,
    displaced_responsibility,
    diffused_responsibility,
    consequence_distortion,
    dehumanization,
    blame_attribution,
    harm_visibility,
    responsibility_clarity,
    empathy,
    guilt,
    harmful_decision,
    policy_endorsement
FROM moral_disengagement_trials
WHERE md_index >= 7
  AND harmful_decision = 1;
