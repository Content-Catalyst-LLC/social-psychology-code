-- Deindividuation in Social Psychology
-- Relational schema for anonymity, self-awareness, accountability, SIDE, norm congruence, and online/crowd behavior research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS deindividuation_groups;
DROP TABLE IF EXISTS deindividuation_trials;

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

CREATE TABLE deindividuation_groups (
    group_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    context_type TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE deindividuation_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    context_type TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    anonymity REAL NOT NULL CHECK (anonymity >= 0 AND anonymity <= 10),
    identifiability REAL NOT NULL CHECK (identifiability >= 0 AND identifiability <= 10),
    group_size INTEGER NOT NULL CHECK (group_size >= 1),
    crowd_immersion REAL NOT NULL CHECK (crowd_immersion >= 0 AND crowd_immersion <= 10),
    self_awareness REAL NOT NULL CHECK (self_awareness >= 0 AND self_awareness <= 10),
    accountability REAL NOT NULL CHECK (accountability >= 0 AND accountability <= 10),
    group_identity_salience REAL NOT NULL CHECK (group_identity_salience >= 0 AND group_identity_salience <= 10),
    personal_identity_salience REAL NOT NULL CHECK (personal_identity_salience >= 0 AND personal_identity_salience <= 10),
    group_norm_valence REAL NOT NULL CHECK (group_norm_valence >= -5 AND group_norm_valence <= 5),
    norm_clarity REAL NOT NULL CHECK (norm_clarity >= 0 AND norm_clarity <= 10),
    norm_congruence REAL NOT NULL CHECK (norm_congruence >= 0 AND norm_congruence <= 10),
    arousal_index REAL NOT NULL CHECK (arousal_index >= 0 AND arousal_index <= 10),
    emotional_contagion REAL NOT NULL CHECK (emotional_contagion >= 0 AND emotional_contagion <= 10),
    responsibility_diffusion REAL NOT NULL CHECK (responsibility_diffusion >= 0 AND responsibility_diffusion <= 10),
    moral_disengagement REAL NOT NULL CHECK (moral_disengagement >= 0 AND moral_disengagement <= 10),
    perceived_surveillance REAL NOT NULL CHECK (perceived_surveillance >= 0 AND perceived_surveillance <= 10),
    moderation_visibility REAL NOT NULL CHECK (moderation_visibility >= 0 AND moderation_visibility <= 10),
    behavior_score REAL NOT NULL CHECK (behavior_score >= 0 AND behavior_score <= 100),
    prosocial_behavior REAL NOT NULL CHECK (prosocial_behavior >= 0 AND prosocial_behavior <= 100),
    antisocial_behavior REAL NOT NULL CHECK (antisocial_behavior >= 0 AND antisocial_behavior <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    log_group_size REAL GENERATED ALWAYS AS (log(group_size + 1)) VIRTUAL,
    identity_shift_index REAL GENERATED ALWAYS AS (group_identity_salience - personal_identity_salience) VIRTUAL,
    deindividuation_index REAL GENERATED ALWAYS AS (
        (anonymity + crowd_immersion + responsibility_diffusion + arousal_index - self_awareness - accountability) / 4.0
    ) VIRTUAL,
    side_norm_activation REAL GENERATED ALWAYS AS (
        anonymity * group_identity_salience * norm_clarity / 100.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES deindividuation_groups(group_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_deind_condition ON deindividuation_trials(condition);
CREATE INDEX idx_deind_context ON deindividuation_trials(context_type);
CREATE INDEX idx_deind_group ON deindividuation_trials(group_id);
CREATE INDEX idx_deind_participant ON deindividuation_trials(participant);
CREATE INDEX idx_deind_anonymity ON deindividuation_trials(anonymity);

DROP VIEW IF EXISTS deindividuation_summary;
CREATE VIEW deindividuation_summary AS
SELECT
    condition,
    context_type,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(behavior_score) AS mean_behavior,
    AVG(prosocial_behavior) AS mean_prosocial,
    AVG(antisocial_behavior) AS mean_antisocial,
    AVG(anonymity) AS mean_anonymity,
    AVG(self_awareness) AS mean_self_awareness,
    AVG(accountability) AS mean_accountability,
    AVG(group_identity_salience) AS mean_group_identity,
    AVG(norm_congruence) AS mean_norm_congruence,
    AVG(deindividuation_index) AS mean_deindividuation
FROM deindividuation_trials
GROUP BY condition, context_type;

DROP VIEW IF EXISTS side_model_cases;
CREATE VIEW side_model_cases AS
SELECT
    participant,
    session_id,
    group_id,
    condition,
    context_type,
    trial,
    anonymity,
    group_identity_salience,
    group_norm_valence,
    norm_clarity,
    norm_congruence,
    prosocial_behavior,
    antisocial_behavior,
    side_norm_activation,
    CASE
        WHEN group_norm_valence > 1 THEN 'prosocial_norm'
        WHEN group_norm_valence < -1 THEN 'antisocial_norm'
        ELSE 'neutral_norm'
    END AS norm_valence_band
FROM deindividuation_trials;
