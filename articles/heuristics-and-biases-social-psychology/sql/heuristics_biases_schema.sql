-- Heuristics and Biases
-- Relational schema for judgment under uncertainty, anchoring, availability,
-- representativeness, affect, framing, confirmation, calibration, and institutional debiasing.

DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS research_groups;
DROP TABLE IF EXISTS research_sites;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS heuristics_biases_trials;

CREATE TABLE participants (
    participant TEXT PRIMARY KEY,
    consent_status TEXT NOT NULL DEFAULT 'consented',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research_groups (
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
    judgment_domain TEXT NOT NULL,
    scenario_description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE heuristics_biases_trials (
    participant TEXT NOT NULL,
    session_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    institution_context TEXT NOT NULL,
    judgment_domain TEXT NOT NULL,
    heuristic_type TEXT NOT NULL,
    condition TEXT NOT NULL,
    trial INTEGER NOT NULL CHECK (trial >= 1),
    anchor_value REAL NOT NULL CHECK (anchor_value >= -1000 AND anchor_value <= 1000),
    true_value REAL NOT NULL CHECK (true_value >= -1000 AND true_value <= 1000),
    estimate REAL NOT NULL CHECK (estimate >= -1000 AND estimate <= 1000),
    base_rate REAL NOT NULL CHECK (base_rate >= 0 AND base_rate <= 1),
    individuating_information_strength REAL NOT NULL CHECK (individuating_information_strength >= 0 AND individuating_information_strength <= 10),
    representativeness_rating REAL NOT NULL CHECK (representativeness_rating >= 0 AND representativeness_rating <= 10),
    availability_salience REAL NOT NULL CHECK (availability_salience >= 0 AND availability_salience <= 10),
    affect_valence REAL NOT NULL CHECK (affect_valence >= -10 AND affect_valence <= 10),
    perceived_risk REAL NOT NULL CHECK (perceived_risk >= 0 AND perceived_risk <= 100),
    perceived_benefit REAL NOT NULL CHECK (perceived_benefit >= 0 AND perceived_benefit <= 100),
    frame_type TEXT NOT NULL CHECK (frame_type IN ('gain', 'loss', 'neutral')),
    choice_binary INTEGER NOT NULL CHECK (choice_binary IN (0, 1)),
    confidence_rating REAL NOT NULL CHECK (confidence_rating >= 0 AND confidence_rating <= 100),
    actual_accuracy REAL NOT NULL CHECK (actual_accuracy >= 0 AND actual_accuracy <= 100),
    confirmation_tendency REAL NOT NULL CHECK (confirmation_tendency >= 0 AND confirmation_tendency <= 10),
    disconfirming_evidence_exposure REAL NOT NULL CHECK (disconfirming_evidence_exposure >= 0 AND disconfirming_evidence_exposure <= 10),
    overconfidence_score REAL NOT NULL CHECK (overconfidence_score >= -100 AND overconfidence_score <= 100),
    response_time_ms REAL NOT NULL CHECK (response_time_ms >= 150),
    debiasing_intervention_strength REAL NOT NULL CHECK (debiasing_intervention_strength >= 0 AND debiasing_intervention_strength <= 10),
    institutional_accountability REAL NOT NULL CHECK (institutional_accountability >= 0 AND institutional_accountability <= 10),
    feedback_quality REAL NOT NULL CHECK (feedback_quality >= 0 AND feedback_quality <= 10),
    decision_quality REAL NOT NULL CHECK (decision_quality >= 0 AND decision_quality <= 100),
    anchoring_error REAL GENERATED ALWAYS AS (
        estimate - true_value
    ) VIRTUAL,
    absolute_error REAL GENERATED ALWAYS AS (
        ABS(estimate - true_value)
    ) VIRTUAL,
    calibration_error REAL GENERATED ALWAYS AS (
        ABS(confidence_rating - actual_accuracy)
    ) VIRTUAL,
    evidence_discipline_index REAL GENERATED ALWAYS AS (
        (debiasing_intervention_strength + institutional_accountability + feedback_quality + disconfirming_evidence_exposure) / 4.0
    ) VIRTUAL,
    PRIMARY KEY (participant, session_id, trial),
    FOREIGN KEY (participant) REFERENCES participants(participant),
    FOREIGN KEY (group_id) REFERENCES research_groups(group_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id),
    FOREIGN KEY (site_id) REFERENCES research_sites(site_id)
);

CREATE INDEX idx_hb_heuristic ON heuristics_biases_trials(heuristic_type);
CREATE INDEX idx_hb_condition ON heuristics_biases_trials(condition);
CREATE INDEX idx_hb_context ON heuristics_biases_trials(institution_context);
CREATE INDEX idx_hb_domain ON heuristics_biases_trials(judgment_domain);
CREATE INDEX idx_hb_participant ON heuristics_biases_trials(participant);

DROP VIEW IF EXISTS heuristics_biases_summary;
CREATE VIEW heuristics_biases_summary AS
SELECT
    heuristic_type,
    condition,
    institution_context,
    judgment_domain,
    COUNT(*) AS n_trials,
    COUNT(DISTINCT participant) AS n_participants,
    AVG(estimate) AS mean_estimate,
    AVG(true_value) AS mean_true_value,
    AVG(anchoring_error) AS mean_anchoring_error,
    AVG(absolute_error) AS mean_absolute_error,
    AVG(calibration_error) AS mean_calibration_error,
    AVG(overconfidence_score) AS mean_overconfidence,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(evidence_discipline_index) AS mean_evidence_discipline
FROM heuristics_biases_trials
GROUP BY heuristic_type, condition, institution_context, judgment_domain;
