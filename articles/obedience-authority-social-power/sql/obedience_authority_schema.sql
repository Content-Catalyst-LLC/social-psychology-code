-- Obedience, Authority, and Social Power
-- Relational schema for obedience, authority legitimacy, escalation, responsibility displacement,
-- moral conflict, peer dissent, resistance, and institutional safeguards.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS authority_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS obedience_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE authority_groups (
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

CREATE TABLE obedience_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    authority_legitimacy REAL NOT NULL CHECK (authority_legitimacy >= 0 AND authority_legitimacy <= 10),
    authority_proximity REAL NOT NULL CHECK (authority_proximity >= 0 AND authority_proximity <= 10),
    institutional_prestige REAL NOT NULL CHECK (institutional_prestige >= 0 AND institutional_prestige <= 10),
    command_clarity REAL NOT NULL CHECK (command_clarity >= 0 AND command_clarity <= 10),
    cost_of_defiance REAL NOT NULL CHECK (cost_of_defiance >= 0 AND cost_of_defiance <= 10),
    escalation_step INTEGER NOT NULL CHECK (escalation_step >= 1),
    responsibility_displacement REAL NOT NULL CHECK (responsibility_displacement >= 0 AND responsibility_displacement <= 10),
    moral_conflict REAL NOT NULL CHECK (moral_conflict >= 0 AND moral_conflict <= 10),
    victim_proximity REAL NOT NULL CHECK (victim_proximity >= 0 AND victim_proximity <= 10),
    harm_salience REAL NOT NULL CHECK (harm_salience >= 0 AND harm_salience <= 10),
    peer_dissent REAL NOT NULL CHECK (peer_dissent >= 0 AND peer_dissent <= 10),
    peer_compliance REAL NOT NULL CHECK (peer_compliance >= 0 AND peer_compliance <= 10),
    role_identification REAL NOT NULL CHECK (role_identification >= 0 AND role_identification <= 10),
    mission_identification REAL NOT NULL CHECK (mission_identification >= 0 AND mission_identification <= 10),
    obeyed INTEGER NOT NULL CHECK (obeyed IN (0, 1)),
    resisted INTEGER NOT NULL CHECK (resisted IN (0, 1)),
    hesitation REAL NOT NULL CHECK (hesitation >= 0 AND hesitation <= 10),
    protest INTEGER NOT NULL CHECK (protest IN (0, 1)),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    perceived_responsibility_after REAL NOT NULL CHECK (perceived_responsibility_after >= 0 AND perceived_responsibility_after <= 10),
    authority_pressure_index REAL GENERATED ALWAYS AS (
        (authority_legitimacy + authority_proximity + institutional_prestige + command_clarity + cost_of_defiance + peer_compliance - peer_dissent) / 6.0
    ) VIRTUAL,
    moral_resistance_index REAL GENERATED ALWAYS AS (
        (moral_conflict + victim_proximity + harm_salience + peer_dissent + perceived_responsibility_after) / 5.0
    ) VIRTUAL,
    identification_index REAL GENERATED ALWAYS AS (
        (role_identification + mission_identification + institutional_prestige) / 3.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES authority_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_obedience_condition ON obedience_trials(condition);
CREATE INDEX idx_obedience_context ON obedience_trials(institution_context);
CREATE INDEX idx_obedience_group ON obedience_trials(group_id);
CREATE INDEX idx_obedience_participant ON obedience_trials(participant);
CREATE INDEX idx_obedience_escalation ON obedience_trials(escalation_step);

DROP VIEW IF EXISTS obedience_summary;
CREATE VIEW obedience_summary AS
SELECT
    condition,
    institution_context,
    escalation_step,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(obeyed) AS obedience_rate,
    AVG(resisted) AS resistance_rate,
    AVG(protest) AS protest_rate,
    AVG(hesitation) AS mean_hesitation,
    AVG(authority_pressure_index) AS mean_authority_pressure,
    AVG(moral_resistance_index) AS mean_moral_resistance,
    AVG(identification_index) AS mean_identification,
    AVG(perceived_responsibility_after) AS mean_responsibility_after
FROM obedience_trials
GROUP BY condition, institution_context, escalation_step;

DROP VIEW IF EXISTS high_risk_obedience_cases;
CREATE VIEW high_risk_obedience_cases AS
SELECT
    participant,
    session_id,
    group_id,
    scenario_id,
    condition,
    institution_context,
    escalation_step,
    authority_pressure_index,
    moral_resistance_index,
    responsibility_displacement,
    moral_conflict,
    peer_dissent,
    obeyed,
    resisted,
    hesitation,
    protest,
    perceived_responsibility_after
FROM obedience_trials
WHERE obeyed = 1
  AND moral_resistance_index >= 6.5
  AND perceived_responsibility_after <= 5;
