-- Group Polarization and Collective Judgment
-- Relational schema for pre-post attitudes, confidence amplification, persuasive arguments, social comparison, identity salience, norm enforcement, dissent quality, deliberation structure, algorithmic reinforcement, and collective judgment research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS discussion_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS group_polarization_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE discussion_groups (
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
    platform_context TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_polarization_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    platform_context TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    pre_attitude REAL NOT NULL CHECK (pre_attitude >= -100 AND pre_attitude <= 100),
    post_attitude REAL NOT NULL CHECK (post_attitude >= -100 AND post_attitude <= 100),
    pre_confidence REAL NOT NULL CHECK (pre_confidence >= 0 AND pre_confidence <= 100),
    post_confidence REAL NOT NULL CHECK (post_confidence >= 0 AND post_confidence <= 100),
    argument_exposure REAL NOT NULL CHECK (argument_exposure >= 0 AND argument_exposure <= 10),
    argument_diversity REAL NOT NULL CHECK (argument_diversity >= 0 AND argument_diversity <= 10),
    informational_homogeneity REAL NOT NULL CHECK (informational_homogeneity >= 0 AND informational_homogeneity <= 10),
    social_comparison_pressure REAL NOT NULL CHECK (social_comparison_pressure >= 0 AND social_comparison_pressure <= 10),
    identity_salience REAL NOT NULL CHECK (identity_salience >= 0 AND identity_salience <= 10),
    group_identification REAL NOT NULL CHECK (group_identification >= 0 AND group_identification <= 10),
    norm_enforcement REAL NOT NULL CHECK (norm_enforcement >= 0 AND norm_enforcement <= 10),
    dissent_presence INTEGER NOT NULL CHECK (dissent_presence IN (0, 1)),
    dissent_quality REAL NOT NULL CHECK (dissent_quality >= 0 AND dissent_quality <= 10),
    minority_view_protection REAL NOT NULL CHECK (minority_view_protection >= 0 AND minority_view_protection <= 10),
    deliberation_structure REAL NOT NULL CHECK (deliberation_structure >= 0 AND deliberation_structure <= 10),
    moderation_quality REAL NOT NULL CHECK (moderation_quality >= 0 AND moderation_quality <= 10),
    algorithmic_reinforcement REAL NOT NULL CHECK (algorithmic_reinforcement >= 0 AND algorithmic_reinforcement <= 10),
    cross_cutting_exposure REAL NOT NULL CHECK (cross_cutting_exposure >= 0 AND cross_cutting_exposure <= 10),
    perceived_consensus REAL NOT NULL CHECK (perceived_consensus >= 0 AND perceived_consensus <= 100),
    perceived_legitimacy REAL NOT NULL CHECK (perceived_legitimacy >= 0 AND perceived_legitimacy <= 10),
    decision_quality REAL NOT NULL CHECK (decision_quality >= 0 AND decision_quality <= 100),
    collective_judgment_accuracy REAL NOT NULL CHECK (collective_judgment_accuracy >= 0 AND collective_judgment_accuracy <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    attitude_shift REAL GENERATED ALWAYS AS (post_attitude - pre_attitude) VIRTUAL,
    extremity_shift REAL GENERATED ALWAYS AS (abs(post_attitude) - abs(pre_attitude)) VIRTUAL,
    confidence_shift REAL GENERATED ALWAYS AS (post_confidence - pre_confidence) VIRTUAL,
    polarization_risk_index REAL GENERATED ALWAYS AS (
        (argument_exposure + informational_homogeneity + social_comparison_pressure + identity_salience + group_identification + norm_enforcement + algorithmic_reinforcement - argument_diversity - dissent_quality - minority_view_protection - deliberation_structure - cross_cutting_exposure) / 6.0
    ) VIRTUAL,
    deliberative_safeguard_index REAL GENERATED ALWAYS AS (
        (argument_diversity + dissent_quality + minority_view_protection + deliberation_structure + moderation_quality + cross_cutting_exposure + perceived_legitimacy) / 7.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES discussion_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_gp_condition ON group_polarization_trials(condition);
CREATE INDEX idx_gp_context ON group_polarization_trials(platform_context);
CREATE INDEX idx_gp_group ON group_polarization_trials(group_id);
CREATE INDEX idx_gp_participant ON group_polarization_trials(participant);

DROP VIEW IF EXISTS group_polarization_summary;
CREATE VIEW group_polarization_summary AS
SELECT
    condition,
    platform_context,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    AVG(pre_attitude) AS mean_pre_attitude,
    AVG(post_attitude) AS mean_post_attitude,
    AVG(attitude_shift) AS mean_attitude_shift,
    AVG(extremity_shift) AS mean_extremity_shift,
    AVG(confidence_shift) AS mean_confidence_shift,
    AVG(polarization_risk_index) AS mean_polarization_risk,
    AVG(deliberative_safeguard_index) AS mean_deliberative_safeguards,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(collective_judgment_accuracy) AS mean_collective_accuracy
FROM group_polarization_trials
GROUP BY condition, platform_context;

DROP VIEW IF EXISTS high_risk_polarization_cases;
CREATE VIEW high_risk_polarization_cases AS
SELECT
    participant,
    session_id,
    group_id,
    scenario_id,
    condition,
    platform_context,
    pre_attitude,
    post_attitude,
    attitude_shift,
    extremity_shift,
    confidence_shift,
    polarization_risk_index,
    deliberative_safeguard_index,
    perceived_consensus,
    decision_quality,
    collective_judgment_accuracy
FROM group_polarization_trials
WHERE extremity_shift >= 20 OR polarization_risk_index >= 4 OR collective_judgment_accuracy <= 40;
