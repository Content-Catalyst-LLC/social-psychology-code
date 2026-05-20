-- Prisoner's Dilemma in Social Psychology
-- Relational schema for cooperation, defection, trust, fairness, reciprocity, and institutional enforcement research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS dyads;
DROP TABLE IF EXISTS prisoners_dilemma_trials;
DROP TABLE IF EXISTS strategy_tournament_rounds;

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

CREATE TABLE dyads (
    dyad_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    horizon_type TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE prisoners_dilemma_trials (
    participant TEXT NOT NULL,
    dyad_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    round INTEGER NOT NULL CHECK (round >= 1),
    horizon_type TEXT NOT NULL,
    own_choice TEXT NOT NULL CHECK (own_choice IN ('cooperate', 'defect')),
    partner_choice TEXT NOT NULL CHECK (partner_choice IN ('cooperate', 'defect')),
    cooperate INTEGER NOT NULL CHECK (cooperate IN (0, 1)),
    partner_cooperate INTEGER NOT NULL CHECK (partner_cooperate IN (0, 1)),
    own_payoff REAL NOT NULL,
    partner_payoff REAL NOT NULL,
    cumulative_payoff REAL NOT NULL,
    temptation_payoff REAL NOT NULL,
    reward_payoff REAL NOT NULL,
    punishment_payoff REAL NOT NULL,
    sucker_payoff REAL NOT NULL,
    trust_score REAL NOT NULL CHECK (trust_score >= 0 AND trust_score <= 10),
    fairness_score REAL NOT NULL CHECK (fairness_score >= 0 AND fairness_score <= 10),
    expected_partner_cooperation REAL NOT NULL CHECK (expected_partner_cooperation >= 0 AND expected_partner_cooperation <= 10),
    communication_access INTEGER NOT NULL CHECK (communication_access IN (0, 1)),
    punishment_available INTEGER NOT NULL CHECK (punishment_available IN (0, 1)),
    reputation_visibility REAL NOT NULL CHECK (reputation_visibility >= 0 AND reputation_visibility <= 10),
    monitoring_strength REAL NOT NULL CHECK (monitoring_strength >= 0 AND monitoring_strength <= 10),
    institutional_enforcement REAL NOT NULL CHECK (institutional_enforcement >= 0 AND institutional_enforcement <= 10),
    social_identity_salience REAL NOT NULL CHECK (social_identity_salience >= 0 AND social_identity_salience <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    temptation_gap REAL GENERATED ALWAYS AS (temptation_payoff - reward_payoff) VIRTUAL,
    cooperation_surplus REAL GENERATED ALWAYS AS ((2 * reward_payoff) - (temptation_payoff + sucker_payoff)) VIRTUAL,
    PRIMARY KEY (participant, dyad_id, round),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (dyad_id) REFERENCES dyads(dyad_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE strategy_tournament_rounds (
    tournament_id TEXT NOT NULL,
    strategy_a TEXT NOT NULL,
    strategy_b TEXT NOT NULL,
    round INTEGER NOT NULL CHECK (round >= 1),
    choice_a INTEGER NOT NULL CHECK (choice_a IN (0, 1)),
    choice_b INTEGER NOT NULL CHECK (choice_b IN (0, 1)),
    payoff_a REAL NOT NULL,
    payoff_b REAL NOT NULL,
    cumulative_a REAL NOT NULL,
    cumulative_b REAL NOT NULL,
    PRIMARY KEY (tournament_id, strategy_a, strategy_b, round)
);

CREATE INDEX idx_pd_condition ON prisoners_dilemma_trials(condition);
CREATE INDEX idx_pd_dyad ON prisoners_dilemma_trials(dyad_id);
CREATE INDEX idx_pd_participant ON prisoners_dilemma_trials(participant);
CREATE INDEX idx_pd_round ON prisoners_dilemma_trials(round);
CREATE INDEX idx_pd_cooperate ON prisoners_dilemma_trials(cooperate);

DROP VIEW IF EXISTS cooperation_summary;
CREATE VIEW cooperation_summary AS
SELECT
    condition,
    round,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT dyad_id) AS n_dyads,
    AVG(cooperate) AS cooperation_rate,
    AVG(partner_cooperate) AS partner_cooperation_rate,
    AVG(own_payoff) AS mean_payoff,
    AVG(cumulative_payoff) AS mean_cumulative_payoff,
    AVG(trust_score) AS mean_trust,
    AVG(fairness_score) AS mean_fairness,
    AVG(expected_partner_cooperation) AS mean_expected_partner_cooperation
FROM prisoners_dilemma_trials
GROUP BY condition, round;

DROP VIEW IF EXISTS high_cooperation_contexts;
CREATE VIEW high_cooperation_contexts AS
SELECT
    condition,
    horizon_type,
    AVG(cooperate) AS cooperation_rate,
    AVG(trust_score) AS mean_trust,
    AVG(reputation_visibility) AS mean_reputation,
    AVG(institutional_enforcement) AS mean_enforcement,
    AVG(communication_access) AS communication_rate,
    COUNT(*) AS n
FROM prisoners_dilemma_trials
GROUP BY condition, horizon_type
HAVING AVG(cooperate) >= 0.60;
