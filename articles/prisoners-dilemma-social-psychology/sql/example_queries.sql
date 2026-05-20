-- Example analytical queries for prisoner’s dilemma research.

-- 1. Cooperation by condition and round.
SELECT
    condition,
    round,
    n_trials,
    cooperation_rate,
    mean_payoff,
    mean_trust,
    mean_fairness,
    mean_expected_partner_cooperation
FROM cooperation_summary
ORDER BY condition, round;

-- 2. Cooperation by institutional condition.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(cooperate) AS cooperation_rate,
    AVG(trust_score) AS mean_trust,
    AVG(reputation_visibility) AS mean_reputation,
    AVG(monitoring_strength) AS mean_monitoring,
    AVG(institutional_enforcement) AS mean_enforcement,
    AVG(own_payoff) AS mean_payoff
FROM prisoners_dilemma_trials
GROUP BY condition
ORDER BY cooperation_rate DESC;

-- 3. Payoff-matrix validation.
SELECT
    condition,
    MIN(temptation_payoff > reward_payoff) AS all_t_gt_r,
    MIN(reward_payoff > punishment_payoff) AS all_r_gt_p,
    MIN(punishment_payoff > sucker_payoff) AS all_p_gt_s,
    MIN((2 * reward_payoff) > (temptation_payoff + sucker_payoff)) AS all_collective_surplus
FROM prisoners_dilemma_trials
GROUP BY condition;

-- 4. Reciprocity: cooperation after previous partner cooperation.
WITH lagged AS (
    SELECT
        participant,
        dyad_id,
        condition,
        round,
        cooperate,
        partner_cooperate,
        LAG(partner_cooperate) OVER (
            PARTITION BY participant, dyad_id ORDER BY round
        ) AS previous_partner_cooperate
    FROM prisoners_dilemma_trials
)
SELECT
    condition,
    previous_partner_cooperate,
    COUNT(*) AS n,
    AVG(cooperate) AS cooperation_rate
FROM lagged
WHERE previous_partner_cooperate IS NOT NULL
GROUP BY condition, previous_partner_cooperate
ORDER BY condition, previous_partner_cooperate;
