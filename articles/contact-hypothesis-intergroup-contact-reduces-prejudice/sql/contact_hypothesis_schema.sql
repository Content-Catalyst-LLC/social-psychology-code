-- Contact Hypothesis and Intergroup Contact
-- Relational schema for social psychology prejudice-reduction research.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS contact_trials;
DROP TABLE IF EXISTS contact_events;
DROP TABLE IF EXISTS cross_group_network_edges;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    group_status TEXT NOT NULL,
    demographic_group TEXT,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_sites (
    site_id TEXT PRIMARY KEY,
    site_type TEXT,
    institutional_support_policy TEXT,
    location_code TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contact_trials (
    participant TEXT NOT NULL,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    wave INTEGER NOT NULL CHECK (wave >= 1),
    target_group TEXT NOT NULL,
    group_status TEXT NOT NULL,
    contact_frequency REAL NOT NULL CHECK (contact_frequency >= 0 AND contact_frequency <= 10),
    contact_quality REAL NOT NULL CHECK (contact_quality >= 0 AND contact_quality <= 10),
    equal_status REAL NOT NULL CHECK (equal_status >= 0 AND equal_status <= 10),
    common_goals REAL NOT NULL CHECK (common_goals >= 0 AND common_goals <= 10),
    cooperation REAL NOT NULL CHECK (cooperation >= 0 AND cooperation <= 10),
    institutional_support REAL NOT NULL CHECK (institutional_support >= 0 AND institutional_support <= 10),
    voluntariness REAL NOT NULL CHECK (voluntariness >= 0 AND voluntariness <= 10),
    negative_contact REAL NOT NULL CHECK (negative_contact >= 0 AND negative_contact <= 10),
    indirect_contact REAL NOT NULL CHECK (indirect_contact >= 0 AND indirect_contact <= 10),
    intergroup_anxiety REAL NOT NULL CHECK (intergroup_anxiety >= 0 AND intergroup_anxiety <= 10),
    empathy REAL NOT NULL CHECK (empathy >= 0 AND empathy <= 10),
    perspective_taking REAL NOT NULL CHECK (perspective_taking >= 0 AND perspective_taking <= 10),
    trust REAL NOT NULL CHECK (trust >= 0 AND trust <= 10),
    perceived_threat REAL NOT NULL CHECK (perceived_threat >= 0 AND perceived_threat <= 10),
    prejudice_pre REAL NOT NULL CHECK (prejudice_pre >= 0 AND prejudice_pre <= 10),
    prejudice_post REAL NOT NULL CHECK (prejudice_post >= 0 AND prejudice_post <= 10),
    stereotype_endorsement REAL NOT NULL CHECK (stereotype_endorsement >= 0 AND stereotype_endorsement <= 10),
    future_contact_willingness REAL NOT NULL CHECK (future_contact_willingness >= 0 AND future_contact_willingness <= 10),
    social_distance REAL NOT NULL CHECK (social_distance >= 0 AND social_distance <= 10),
    inclusive_norm_perception REAL NOT NULL CHECK (inclusive_norm_perception >= 0 AND inclusive_norm_perception <= 10),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    prejudice_change REAL GENERATED ALWAYS AS (prejudice_post - prejudice_pre) VIRTUAL,
    allport_quality REAL GENERATED ALWAYS AS (
        (equal_status + common_goals + cooperation + institutional_support + voluntariness) / 5.0
    ) VIRTUAL,
    PRIMARY KEY (participant, wave, target_group),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE contact_events (
    event_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT,
    shared_goal TEXT,
    cooperation_required INTEGER CHECK (cooperation_required IN (0, 1)),
    facilitator_present INTEGER CHECK (facilitator_present IN (0, 1)),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE TABLE cross_group_network_edges (
    source_participant TEXT NOT NULL,
    target_participant TEXT NOT NULL,
    tie_type TEXT NOT NULL DEFAULT 'cross_group_contact',
    contact_quality REAL CHECK (contact_quality >= 0 AND contact_quality <= 10),
    negative_contact REAL CHECK (negative_contact >= 0 AND negative_contact <= 10),
    observed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_participant, target_participant, tie_type)
);

CREATE INDEX idx_contact_condition ON contact_trials(condition);
CREATE INDEX idx_contact_site ON contact_trials(site_id);
CREATE INDEX idx_contact_group_status ON contact_trials(group_status);
CREATE INDEX idx_contact_wave ON contact_trials(wave);
CREATE INDEX idx_contact_target_group ON contact_trials(target_group);
CREATE INDEX idx_contact_prejudice_change ON contact_trials(prejudice_change);

DROP VIEW IF EXISTS condition_summary;
CREATE VIEW condition_summary AS
SELECT
    condition,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    COUNT(DISTINCT site_id) AS n_sites,
    AVG(contact_frequency) AS mean_contact_frequency,
    AVG(contact_quality) AS mean_contact_quality,
    AVG(allport_quality) AS mean_allport_quality,
    AVG(negative_contact) AS mean_negative_contact,
    AVG(indirect_contact) AS mean_indirect_contact,
    AVG(intergroup_anxiety) AS mean_anxiety,
    AVG(empathy) AS mean_empathy,
    AVG(trust) AS mean_trust,
    AVG(prejudice_pre) AS mean_prejudice_pre,
    AVG(prejudice_post) AS mean_prejudice_post,
    AVG(prejudice_change) AS mean_prejudice_change,
    AVG(social_distance) AS mean_social_distance,
    AVG(future_contact_willingness) AS mean_future_contact
FROM contact_trials
GROUP BY condition;

DROP VIEW IF EXISTS high_quality_low_prejudice_cases;
CREATE VIEW high_quality_low_prejudice_cases AS
SELECT
    participant,
    site_id,
    condition,
    target_group,
    group_status,
    contact_quality,
    allport_quality,
    negative_contact,
    intergroup_anxiety,
    empathy,
    trust,
    prejudice_pre,
    prejudice_post,
    prejudice_change
FROM contact_trials
WHERE contact_quality >= 7
  AND prejudice_change < 0;

DROP VIEW IF EXISTS negative_contact_risk_cases;
CREATE VIEW negative_contact_risk_cases AS
SELECT
    participant,
    site_id,
    condition,
    target_group,
    group_status,
    contact_quality,
    negative_contact,
    intergroup_anxiety,
    perceived_threat,
    prejudice_pre,
    prejudice_post,
    prejudice_change,
    social_distance
FROM contact_trials
WHERE negative_contact >= 7;
