-- Social Norms in Social Psychology
-- Relational schema for descriptive norms, injunctive norms, empirical expectations, normative expectations, sanctions, rewards, legitimacy, pluralistic ignorance, dynamic norms, and norm tipping.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS social_norms_trials;

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

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    policy_domain TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE social_norms_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    reference_group TEXT NOT NULL,
    policy_domain TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    descriptive_norm REAL NOT NULL CHECK (descriptive_norm >= 0 AND descriptive_norm <= 100),
    injunctive_norm REAL NOT NULL CHECK (injunctive_norm >= 0 AND injunctive_norm <= 100),
    empirical_expectation REAL NOT NULL CHECK (empirical_expectation >= 0 AND empirical_expectation <= 100),
    normative_expectation REAL NOT NULL CHECK (normative_expectation >= 0 AND normative_expectation <= 100),
    personal_attitude REAL NOT NULL CHECK (personal_attitude >= 0 AND personal_attitude <= 100),
    norm_salience REAL NOT NULL CHECK (norm_salience >= 0 AND norm_salience <= 10),
    sanction_salience REAL NOT NULL CHECK (sanction_salience >= 0 AND sanction_salience <= 10),
    sanction_severity REAL NOT NULL CHECK (sanction_severity >= 0 AND sanction_severity <= 10),
    reward_salience REAL NOT NULL CHECK (reward_salience >= 0 AND reward_salience <= 10),
    reference_group_identification REAL NOT NULL CHECK (reference_group_identification >= 0 AND reference_group_identification <= 10),
    institutional_legitimacy REAL NOT NULL CHECK (institutional_legitimacy >= 0 AND institutional_legitimacy <= 10),
    trust_in_institution REAL NOT NULL CHECK (trust_in_institution >= 0 AND trust_in_institution <= 10),
    pluralistic_ignorance REAL NOT NULL CHECK (pluralistic_ignorance >= 0 AND pluralistic_ignorance <= 100),
    dynamic_norm_trend REAL NOT NULL CHECK (dynamic_norm_trend >= -100 AND dynamic_norm_trend <= 100),
    message_type TEXT NOT NULL,
    complied INTEGER NOT NULL CHECK (complied IN (0, 1)),
    compliance_intention REAL NOT NULL CHECK (compliance_intention >= 0 AND compliance_intention <= 100),
    contribution_amount REAL NOT NULL CHECK (contribution_amount >= 0 AND contribution_amount <= 100),
    reported_violation INTEGER NOT NULL CHECK (reported_violation IN (0, 1)),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    norm_threshold REAL NOT NULL CHECK (norm_threshold >= 0 AND norm_threshold <= 100),
    tipping_exposure REAL NOT NULL CHECK (tipping_exposure >= 0 AND tipping_exposure <= 100),
    post_message_norm_perception REAL NOT NULL CHECK (post_message_norm_perception >= 0 AND post_message_norm_perception <= 100),
    norm_strength_index REAL GENERATED ALWAYS AS (
        (descriptive_norm + injunctive_norm + empirical_expectation + normative_expectation) / 4.0
    ) VIRTUAL,
    enforcement_index REAL GENERATED ALWAYS AS (
        (sanction_salience + sanction_severity + reward_salience) / 3.0
    ) VIRTUAL,
    legitimacy_trust_index REAL GENERATED ALWAYS AS (
        (institutional_legitimacy + trust_in_institution) / 2.0
    ) VIRTUAL,
    tipping_margin REAL GENERATED ALWAYS AS (
        tipping_exposure - norm_threshold
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_sn_condition ON social_norms_trials(condition);
CREATE INDEX idx_sn_domain ON social_norms_trials(policy_domain);
CREATE INDEX idx_sn_message ON social_norms_trials(message_type);
CREATE INDEX idx_sn_reference_group ON social_norms_trials(reference_group);
CREATE INDEX idx_sn_participant ON social_norms_trials(participant);

DROP VIEW IF EXISTS social_norms_summary;
CREATE VIEW social_norms_summary AS
SELECT
    condition,
    policy_domain,
    message_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(complied) AS compliance_rate,
    AVG(reported_violation) AS reporting_rate,
    AVG(compliance_intention) AS mean_intention,
    AVG(contribution_amount) AS mean_contribution,
    AVG(descriptive_norm) AS mean_descriptive_norm,
    AVG(injunctive_norm) AS mean_injunctive_norm,
    AVG(empirical_expectation) AS mean_empirical_expectation,
    AVG(normative_expectation) AS mean_normative_expectation,
    AVG(pluralistic_ignorance) AS mean_pluralistic_ignorance,
    AVG(norm_strength_index) AS mean_norm_strength,
    AVG(enforcement_index) AS mean_enforcement,
    AVG(legitimacy_trust_index) AS mean_legitimacy_trust,
    AVG(tipping_margin) AS mean_tipping_margin
FROM social_norms_trials
GROUP BY condition, policy_domain, message_type;

DROP VIEW IF EXISTS pluralistic_ignorance_cases;
CREATE VIEW pluralistic_ignorance_cases AS
SELECT
    participant,
    session_id,
    scenario_id,
    reference_group,
    policy_domain,
    condition,
    personal_attitude,
    injunctive_norm,
    descriptive_norm,
    pluralistic_ignorance,
    complied,
    compliance_intention,
    post_message_norm_perception
FROM social_norms_trials
WHERE pluralistic_ignorance >= 25;
