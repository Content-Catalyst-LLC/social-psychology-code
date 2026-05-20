-- Social Dilemmas in Social Psychology
-- Relational schema for public-goods games, commons dilemmas, cooperation, enforcement, and institutional legitimacy research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS social_dilemma_groups;
DROP TABLE IF EXISTS social_dilemma_trials;
DROP TABLE IF EXISTS commons_resource_periods;

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

CREATE TABLE social_dilemma_groups (
    group_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    dilemma_type TEXT NOT NULL,
    group_size INTEGER CHECK (group_size >= 1),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE social_dilemma_trials (
    participant TEXT NOT NULL,
    group_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    dilemma_type TEXT NOT NULL,
    round INTEGER NOT NULL CHECK (round >= 1),
    endowment REAL NOT NULL CHECK (endowment >= 0),
    contribution REAL NOT NULL CHECK (contribution >= 0),
    extraction REAL NOT NULL CHECK (extraction >= 0),
    mpcr REAL NOT NULL CHECK (mpcr >= 0),
    trust_score REAL NOT NULL CHECK (trust_score >= 0 AND trust_score <= 10),
    norm_salience REAL NOT NULL CHECK (norm_salience >= 0 AND norm_salience <= 10),
    enforcement_signal REAL NOT NULL CHECK (enforcement_signal >= 0 AND enforcement_signal <= 10),
    fairness_score REAL NOT NULL CHECK (fairness_score >= 0 AND fairness_score <= 10),
    institutional_legitimacy REAL NOT NULL CHECK (institutional_legitimacy >= 0 AND institutional_legitimacy <= 10),
    monitoring_strength REAL NOT NULL CHECK (monitoring_strength >= 0 AND monitoring_strength <= 10),
    sanction_probability REAL NOT NULL CHECK (sanction_probability >= 0 AND sanction_probability <= 1),
    sanction_severity REAL NOT NULL CHECK (sanction_severity >= 0 AND sanction_severity <= 10),
    reciprocity_expectation REAL NOT NULL CHECK (reciprocity_expectation >= 0 AND reciprocity_expectation <= 10),
    resource_stock REAL NOT NULL CHECK (resource_stock >= 0),
    group_welfare REAL NOT NULL,
    individual_payoff REAL NOT NULL,
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    free_riding_index REAL GENERATED ALWAYS AS (
        CASE WHEN endowment > 0 THEN (endowment - contribution) / endowment ELSE NULL END
    ) VIRTUAL,
    institutional_effectiveness REAL GENERATED ALWAYS AS (
        monitoring_strength * sanction_probability * sanction_severity * (institutional_legitimacy / 10.0)
    ) VIRTUAL,
    PRIMARY KEY (participant, group_id, round),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES social_dilemma_groups(group_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE commons_resource_periods (
    group_id TEXT NOT NULL,
    period INTEGER NOT NULL CHECK (period >= 1),
    resource_stock REAL NOT NULL CHECK (resource_stock >= 0),
    total_extraction REAL NOT NULL CHECK (total_extraction >= 0),
    regeneration REAL NOT NULL CHECK (regeneration >= 0),
    sustainability_threshold REAL NOT NULL CHECK (sustainability_threshold >= 0),
    PRIMARY KEY (group_id, period),
    FOREIGN KEY (group_id) REFERENCES social_dilemma_groups(group_id)
);

CREATE INDEX idx_sd_condition ON social_dilemma_trials(condition);
CREATE INDEX idx_sd_type ON social_dilemma_trials(dilemma_type);
CREATE INDEX idx_sd_group ON social_dilemma_trials(group_id);
CREATE INDEX idx_sd_participant ON social_dilemma_trials(participant);
CREATE INDEX idx_sd_round ON social_dilemma_trials(round);

DROP VIEW IF EXISTS social_dilemma_summary;
CREATE VIEW social_dilemma_summary AS
SELECT
    condition,
    dilemma_type,
    round,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT group_id) AS n_groups,
    AVG(contribution) AS mean_contribution,
    AVG(extraction) AS mean_extraction,
    AVG(free_riding_index) AS mean_free_riding,
    AVG(trust_score) AS mean_trust,
    AVG(norm_salience) AS mean_norm_salience,
    AVG(enforcement_signal) AS mean_enforcement,
    AVG(institutional_legitimacy) AS mean_legitimacy,
    AVG(group_welfare) AS mean_group_welfare,
    AVG(resource_stock) AS mean_resource_stock
FROM social_dilemma_trials
GROUP BY condition, dilemma_type, round;

DROP VIEW IF EXISTS low_cooperation_contexts;
CREATE VIEW low_cooperation_contexts AS
SELECT
    condition,
    dilemma_type,
    AVG(contribution) AS mean_contribution,
    AVG(extraction) AS mean_extraction,
    AVG(trust_score) AS mean_trust,
    AVG(institutional_legitimacy) AS mean_legitimacy,
    AVG(free_riding_index) AS mean_free_riding,
    COUNT(*) AS n
FROM social_dilemma_trials
GROUP BY condition, dilemma_type
HAVING AVG(free_riding_index) >= 0.65 OR AVG(extraction) >= 8;
