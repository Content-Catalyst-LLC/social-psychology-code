-- Social Comparison Theory in Social Psychology
-- Relational schema for self-evaluation, motivation, affect, and comparison research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS social_comparison_trials;
DROP TABLE IF EXISTS comparison_exposures;
DROP TABLE IF EXISTS institutional_benchmarks;

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

CREATE TABLE social_comparison_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    comparison_type TEXT NOT NULL,
    comparison_domain TEXT NOT NULL,
    reference_group TEXT NOT NULL,
    self_standing REAL NOT NULL CHECK (self_standing >= 0 AND self_standing <= 10),
    reference_standing REAL NOT NULL CHECK (reference_standing >= 0 AND reference_standing <= 10),
    comparison_gap REAL NOT NULL CHECK (comparison_gap >= -10 AND comparison_gap <= 10),
    attainability REAL NOT NULL CHECK (attainability >= 0 AND attainability <= 10),
    similarity REAL NOT NULL CHECK (similarity >= 0 AND similarity <= 10),
    identity_relevance REAL NOT NULL CHECK (identity_relevance >= 0 AND identity_relevance <= 10),
    social_comparison_orientation REAL NOT NULL CHECK (social_comparison_orientation >= 0 AND social_comparison_orientation <= 10),
    self_eval_pre REAL NOT NULL CHECK (self_eval_pre >= 0 AND self_eval_pre <= 10),
    self_eval_post REAL NOT NULL CHECK (self_eval_post >= 0 AND self_eval_post <= 10),
    motivation_score REAL NOT NULL CHECK (motivation_score >= 0 AND motivation_score <= 10),
    envy REAL NOT NULL CHECK (envy >= 0 AND envy <= 10),
    inspiration REAL NOT NULL CHECK (inspiration >= 0 AND inspiration <= 10),
    discouragement REAL NOT NULL CHECK (discouragement >= 0 AND discouragement <= 10),
    reassurance REAL NOT NULL CHECK (reassurance >= 0 AND reassurance <= 10),
    self_esteem REAL NOT NULL CHECK (self_esteem >= 0 AND self_esteem <= 10),
    perceived_fairness REAL NOT NULL CHECK (perceived_fairness >= 0 AND perceived_fairness <= 10),
    relative_deprivation REAL NOT NULL CHECK (relative_deprivation >= 0 AND relative_deprivation <= 10),
    norm_perception REAL NOT NULL CHECK (norm_perception >= 0 AND norm_perception <= 10),
    digital_exposure REAL NOT NULL CHECK (digital_exposure >= 0 AND digital_exposure <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    self_eval_change REAL GENERATED ALWAYS AS (self_eval_post - self_eval_pre) VIRTUAL,
    PRIMARY KEY (participant, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE comparison_exposures (
    exposure_id TEXT PRIMARY KEY,
    participant TEXT NOT NULL,
    exposure_type TEXT NOT NULL,
    comparison_domain TEXT NOT NULL,
    reference_group TEXT NOT NULL,
    exposure_intensity REAL CHECK (exposure_intensity >= 0 AND exposure_intensity <= 10),
    exposure_date TEXT,
    FOREIGN KEY (participant) REFERENCES participants(participant)
);

CREATE TABLE institutional_benchmarks (
    benchmark_id TEXT PRIMARY KEY,
    institution_id TEXT NOT NULL,
    benchmark_domain TEXT NOT NULL,
    reference_institution TEXT,
    institution_score REAL,
    reference_score REAL,
    perceived_gap REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comparison_condition ON social_comparison_trials(condition);
CREATE INDEX idx_comparison_type ON social_comparison_trials(comparison_type);
CREATE INDEX idx_comparison_domain ON social_comparison_trials(comparison_domain);
CREATE INDEX idx_reference_group ON social_comparison_trials(reference_group);
CREATE INDEX idx_participant ON social_comparison_trials(participant);

DROP VIEW IF EXISTS comparison_type_summary;
CREATE VIEW comparison_type_summary AS
SELECT
    condition,
    comparison_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(comparison_gap) AS mean_gap,
    AVG(attainability) AS mean_attainability,
    AVG(similarity) AS mean_similarity,
    AVG(identity_relevance) AS mean_identity_relevance,
    AVG(self_eval_change) AS mean_self_eval_change,
    AVG(motivation_score) AS mean_motivation,
    AVG(envy) AS mean_envy,
    AVG(inspiration) AS mean_inspiration,
    AVG(discouragement) AS mean_discouragement,
    AVG(reassurance) AS mean_reassurance,
    AVG(relative_deprivation) AS mean_relative_deprivation,
    AVG(digital_exposure) AS mean_digital_exposure
FROM social_comparison_trials
GROUP BY condition, comparison_type;

DROP VIEW IF EXISTS high_risk_digital_comparison_cases;
CREATE VIEW high_risk_digital_comparison_cases AS
SELECT
    participant,
    site_id,
    condition,
    comparison_type,
    comparison_domain,
    reference_group,
    comparison_gap,
    attainability,
    identity_relevance,
    social_comparison_orientation,
    self_eval_change,
    envy,
    discouragement,
    relative_deprivation,
    digital_exposure
FROM social_comparison_trials
WHERE digital_exposure >= 7
  AND comparison_gap <= -3
  AND attainability <= 4;
