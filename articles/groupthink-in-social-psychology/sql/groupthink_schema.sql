-- Groupthink in Social Psychology
-- Relational schema for cohesion, directive leadership, insulation, stress, consensus pressure, self-censorship, mindguarding, dissent visibility, outside information, decision quality, and institutional safeguards.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS decision_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS groupthink_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE decision_groups (
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

CREATE TABLE groupthink_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    cohesion REAL NOT NULL CHECK (cohesion >= 0 AND cohesion <= 10),
    leadership_directive REAL NOT NULL CHECK (leadership_directive >= 0 AND leadership_directive <= 10),
    group_insulation REAL NOT NULL CHECK (group_insulation >= 0 AND group_insulation <= 10),
    stress_level REAL NOT NULL CHECK (stress_level >= 0 AND stress_level <= 10),
    consensus_pressure REAL NOT NULL CHECK (consensus_pressure >= 0 AND consensus_pressure <= 10),
    self_censorship REAL NOT NULL CHECK (self_censorship >= 0 AND self_censorship <= 10),
    illusion_invulnerability REAL NOT NULL CHECK (illusion_invulnerability >= 0 AND illusion_invulnerability <= 10),
    collective_rationalization REAL NOT NULL CHECK (collective_rationalization >= 0 AND collective_rationalization <= 10),
    inherent_morality REAL NOT NULL CHECK (inherent_morality >= 0 AND inherent_morality <= 10),
    outgroup_stereotyping REAL NOT NULL CHECK (outgroup_stereotyping >= 0 AND outgroup_stereotyping <= 10),
    direct_pressure_dissenters REAL NOT NULL CHECK (direct_pressure_dissenters >= 0 AND direct_pressure_dissenters <= 10),
    mindguarding REAL NOT NULL CHECK (mindguarding >= 0 AND mindguarding <= 10),
    dissent_visibility REAL NOT NULL CHECK (dissent_visibility >= 0 AND dissent_visibility <= 10),
    outside_information REAL NOT NULL CHECK (outside_information >= 0 AND outside_information <= 10),
    alternative_search REAL NOT NULL CHECK (alternative_search >= 0 AND alternative_search <= 10),
    risk_analysis REAL NOT NULL CHECK (risk_analysis >= 0 AND risk_analysis <= 10),
    contingency_planning REAL NOT NULL CHECK (contingency_planning >= 0 AND contingency_planning <= 10),
    devils_advocate INTEGER NOT NULL CHECK (devils_advocate IN (0, 1)),
    independent_expert_consulted INTEGER NOT NULL CHECK (independent_expert_consulted IN (0, 1)),
    subgroup_review INTEGER NOT NULL CHECK (subgroup_review IN (0, 1)),
    leader_impartiality REAL NOT NULL CHECK (leader_impartiality >= 0 AND leader_impartiality <= 10),
    psychological_safety REAL NOT NULL CHECK (psychological_safety >= 0 AND psychological_safety <= 10),
    perceived_unanimity REAL NOT NULL CHECK (perceived_unanimity >= 0 AND perceived_unanimity <= 100),
    private_disagreement REAL NOT NULL CHECK (private_disagreement >= 0 AND private_disagreement <= 100),
    decision_quality REAL NOT NULL CHECK (decision_quality >= 0 AND decision_quality <= 100),
    forecast_calibration REAL NOT NULL CHECK (forecast_calibration >= 0 AND forecast_calibration <= 100),
    implementation_risk REAL NOT NULL CHECK (implementation_risk >= 0 AND implementation_risk <= 100),
    post_decision_review_quality REAL NOT NULL CHECK (post_decision_review_quality >= 0 AND post_decision_review_quality <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    symptom_index REAL GENERATED ALWAYS AS (
        (illusion_invulnerability + collective_rationalization + inherent_morality + outgroup_stereotyping + self_censorship + direct_pressure_dissenters + mindguarding) / 7.0
    ) VIRTUAL,
    antecedent_risk_index REAL GENERATED ALWAYS AS (
        (cohesion + leadership_directive + group_insulation + stress_level + consensus_pressure) / 5.0
    ) VIRTUAL,
    process_quality_index REAL GENERATED ALWAYS AS (
        (dissent_visibility + outside_information + alternative_search + risk_analysis + contingency_planning + leader_impartiality + psychological_safety) / 7.0
    ) VIRTUAL,
    safeguard_index REAL GENERATED ALWAYS AS (
        (dissent_visibility + outside_information + alternative_search + risk_analysis + contingency_planning + leader_impartiality + psychological_safety + 2.0*devils_advocate + 2.0*independent_expert_consulted + 2.0*subgroup_review) / 9.0
    ) VIRTUAL,
    unanimity_gap REAL GENERATED ALWAYS AS (
        perceived_unanimity - (100.0 - private_disagreement)
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES decision_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_gt_condition ON groupthink_trials(condition);
CREATE INDEX idx_gt_context ON groupthink_trials(institution_context);
CREATE INDEX idx_gt_group ON groupthink_trials(group_id);
CREATE INDEX idx_gt_participant ON groupthink_trials(participant);

DROP VIEW IF EXISTS groupthink_summary;
CREATE VIEW groupthink_summary AS
SELECT
    condition,
    institution_context,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    AVG(antecedent_risk_index + symptom_index - process_quality_index) AS mean_groupthink_risk,
    AVG(antecedent_risk_index) AS mean_antecedent_risk,
    AVG(symptom_index) AS mean_symptoms,
    AVG(process_quality_index) AS mean_process_quality,
    AVG(safeguard_index) AS mean_safeguards,
    AVG(unanimity_gap) AS mean_unanimity_gap,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(forecast_calibration) AS mean_forecast_calibration,
    AVG(implementation_risk) AS mean_implementation_risk,
    AVG(post_decision_review_quality) AS mean_review_quality
FROM groupthink_trials
GROUP BY condition, institution_context;

DROP VIEW IF EXISTS high_risk_groupthink_cases;
CREATE VIEW high_risk_groupthink_cases AS
SELECT
    participant,
    session_id,
    group_id,
    scenario_id,
    condition,
    institution_context,
    antecedent_risk_index,
    symptom_index,
    process_quality_index,
    safeguard_index,
    unanimity_gap,
    self_censorship,
    dissent_visibility,
    outside_information,
    decision_quality,
    forecast_calibration,
    implementation_risk
FROM groupthink_trials
WHERE (antecedent_risk_index + symptom_index - process_quality_index) >= 6
   OR decision_quality <= 40
   OR implementation_risk >= 75;
