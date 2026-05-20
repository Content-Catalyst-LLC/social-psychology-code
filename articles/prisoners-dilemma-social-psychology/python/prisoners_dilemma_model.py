#!/usr/bin/env python3
"""
Prisoner's dilemma research model.

This script can:
1. Generate synthetic prisoner’s dilemma data.
2. Estimate cooperation, payoff, reciprocity, fairness, trust, and response-time models.
3. Compute reciprocity, exploitation sensitivity, and cumulative payoff summaries.
4. Simulate repeated-game strategies and institutional enforcement.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

try:
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "one_shot", "repeated", "communication", "no_communication", "reputation",
    "sanction", "monitoring", "identity_in_group", "identity_out_group",
    "institutional_enforcement"
]
HORIZONS = ["one_shot", "fixed", "indefinite"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def payoff(own_coop: int, partner_coop: int, T: float, R: float, P: float, S: float) -> float:
    if own_coop == 1 and partner_coop == 1:
        return R
    if own_coop == 1 and partner_coop == 0:
        return S
    if own_coop == 0 and partner_coop == 1:
        return T
    return P


def generate_dataset(n_dyads: int = 300, rounds_per_dyad: int = 10, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "one_shot": {"trust": -1.2, "comm": 0, "rep": 0, "sanction": 0, "identity": 0, "enforce": 0, "monitor": 0},
        "repeated": {"trust": 0.6, "comm": 0, "rep": 2, "sanction": 0, "identity": 0.5, "enforce": 0, "monitor": 1},
        "communication": {"trust": 1.8, "comm": 1, "rep": 1.5, "sanction": 0, "identity": 0.8, "enforce": 0, "monitor": 1},
        "no_communication": {"trust": -0.5, "comm": 0, "rep": 1, "sanction": 0, "identity": 0, "enforce": 0, "monitor": 0.5},
        "reputation": {"trust": 1.0, "comm": 0, "rep": 3.5, "sanction": 0, "identity": 0.4, "enforce": 0, "monitor": 1.5},
        "sanction": {"trust": 0.4, "comm": 0, "rep": 1.5, "sanction": 1, "identity": 0.2, "enforce": 3.0, "monitor": 3.0},
        "monitoring": {"trust": 0.6, "comm": 0, "rep": 1.5, "sanction": 0, "identity": 0.2, "enforce": 1.0, "monitor": 3.5},
        "identity_in_group": {"trust": 2.0, "comm": 0, "rep": 1.5, "sanction": 0, "identity": 3.5, "enforce": 0, "monitor": 1},
        "identity_out_group": {"trust": -1.0, "comm": 0, "rep": 1.5, "sanction": 0, "identity": 3.0, "enforce": 0, "monitor": 1},
        "institutional_enforcement": {"trust": 0.8, "comm": 0, "rep": 2.0, "sanction": 1, "identity": 0.4, "enforce": 3.8, "monitor": 3.2},
    }

    for d in range(1, n_dyads + 1):
        condition = rng.choice(CONDITIONS)
        e = effects[condition]
        horizon_type = "one_shot" if condition == "one_shot" else rng.choice(["fixed", "indefinite"], p=[0.4, 0.6])
        site_id = f"S{rng.integers(1, 31):02d}"
        dyad_id = f"D{d:04d}"
        players = [f"P{2*d-1:04d}", f"P{2*d:04d}"]

        T, R, P, S = 5.0, 3.0, 1.0, 0.0
        if e["enforce"] > 0:
            # Expected sanction reduces the net temptation payoff when defection is detected.
            T_effective = T - 0.45 * e["enforce"]
        else:
            T_effective = T

        traits = {
            players[0]: {
                "trust_trait": rng.normal(5.2 + e["trust"], 1.1),
                "fairness_trait": rng.normal(5.0, 1.1),
                "cooperative_orientation": rng.normal(5.2, 1.2),
            },
            players[1]: {
                "trust_trait": rng.normal(5.2 + e["trust"], 1.1),
                "fairness_trait": rng.normal(5.0, 1.1),
                "cooperative_orientation": rng.normal(5.2, 1.2),
            },
        }

        last_choice = {players[0]: 1, players[1]: 1}
        cumulative = {players[0]: 0.0, players[1]: 0.0}

        rounds = 1 if condition == "one_shot" else rounds_per_dyad

        for r in range(1, rounds + 1):
            round_choices = {}

            for player in players:
                partner = players[1] if player == players[0] else players[0]
                partner_last = last_choice[partner]
                own_last = last_choice[player]

                communication = int(e["comm"] == 1)
                punishment_available = int(e["sanction"] == 1)
                reputation_visibility = float(np.clip(rng.normal(3.0 + e["rep"], 1.0), 0, 10))
                monitoring_strength = float(np.clip(rng.normal(3.0 + e["monitor"], 1.0), 0, 10))
                institutional_enforcement = float(np.clip(rng.normal(e["enforce"], 1.0), 0, 10))
                social_identity_salience = float(np.clip(rng.normal(3.5 + e["identity"], 1.0), 0, 10))

                trust_score = float(np.clip(
                    rng.normal(
                        traits[player]["trust_trait"]
                        + 0.55 * partner_last
                        + 0.22 * communication
                        + 0.16 * reputation_visibility
                        + 0.12 * social_identity_salience
                        - 0.18 * (condition == "identity_out_group"),
                        1.0
                    ),
                    0, 10
                ))

                expected_partner_cooperation = float(np.clip(
                    rng.normal(
                        3.0
                        + 0.45 * trust_score
                        + 0.35 * partner_last
                        + 0.18 * reputation_visibility
                        + 0.15 * institutional_enforcement
                        + 0.14 * communication,
                        1.0
                    ),
                    0, 10
                ))

                temptation_gap = T_effective - R
                cooperation_probability = logistic(
                    -3.2
                    + 0.33 * trust_score
                    + 0.30 * expected_partner_cooperation
                    + 0.20 * traits[player]["cooperative_orientation"]
                    + 0.24 * partner_last
                    + 0.16 * communication
                    + 0.15 * reputation_visibility
                    + 0.15 * institutional_enforcement
                    + 0.12 * social_identity_salience
                    - 0.55 * temptation_gap
                    - 0.20 * (horizon_type == "one_shot")
                )

                own_coop = int(rng.random() < cooperation_probability)
                round_choices[player] = {
                    "cooperate": own_coop,
                    "trust_score": trust_score,
                    "expected_partner_cooperation": expected_partner_cooperation,
                    "communication_access": communication,
                    "punishment_available": punishment_available,
                    "reputation_visibility": reputation_visibility,
                    "monitoring_strength": monitoring_strength,
                    "institutional_enforcement": institutional_enforcement,
                    "social_identity_salience": social_identity_salience,
                }

            for player in players:
                partner = players[1] if player == players[0] else players[0]
                own_coop = round_choices[player]["cooperate"]
                partner_coop = round_choices[partner]["cooperate"]
                own_payoff = payoff(own_coop, partner_coop, T_effective, R, P, S)
                partner_payoff = payoff(partner_coop, own_coop, T_effective, R, P, S)
                cumulative[player] += own_payoff

                fairness_score = float(np.clip(
                    rng.normal(
                        traits[player]["fairness_trait"]
                        + 0.55 * (own_coop == partner_coop)
                        + 0.25 * partner_coop
                        - 0.30 * (own_coop == 1 and partner_coop == 0)
                        + 0.15 * round_choices[player]["institutional_enforcement"],
                        1.0
                    ),
                    0, 10
                ))

                response_time_ms = int(np.clip(np.exp(
                    math.log(1050)
                    + 0.05 * abs(round_choices[player]["expected_partner_cooperation"] - 5)
                    + 0.04 * (own_coop != last_choice[player])
                    + rng.normal(0, 0.18)
                ), 150, 60000))

                rows.append({
                    "participant": player,
                    "dyad_id": dyad_id,
                    "site_id": site_id,
                    "condition": condition,
                    "round": r,
                    "horizon_type": horizon_type,
                    "own_choice": "cooperate" if own_coop == 1 else "defect",
                    "partner_choice": "cooperate" if partner_coop == 1 else "defect",
                    "cooperate": own_coop,
                    "partner_cooperate": partner_coop,
                    "own_payoff": round(own_payoff, 3),
                    "partner_payoff": round(partner_payoff, 3),
                    "cumulative_payoff": round(cumulative[player], 3),
                    "temptation_payoff": round(T_effective, 3),
                    "reward_payoff": R,
                    "punishment_payoff": P,
                    "sucker_payoff": S,
                    "trust_score": round(round_choices[player]["trust_score"], 3),
                    "fairness_score": round(fairness_score, 3),
                    "expected_partner_cooperation": round(round_choices[player]["expected_partner_cooperation"], 3),
                    "communication_access": round_choices[player]["communication_access"],
                    "punishment_available": round_choices[player]["punishment_available"],
                    "reputation_visibility": round(round_choices[player]["reputation_visibility"], 3),
                    "monitoring_strength": round(round_choices[player]["monitoring_strength"], 3),
                    "institutional_enforcement": round(round_choices[player]["institutional_enforcement"], 3),
                    "social_identity_salience": round(round_choices[player]["social_identity_salience"], 3),
                    "response_time_ms": response_time_ms,
                })

            for player in players:
                last_choice[player] = round_choices[player]["cooperate"]

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data = data.sort_values(["dyad_id", "participant", "round"])
    data["previous_partner_cooperate"] = data.groupby(["dyad_id", "participant"])["partner_cooperate"].shift(1)
    data["previous_own_cooperate"] = data.groupby(["dyad_id", "participant"])["cooperate"].shift(1)
    data["reciprocity_opportunity"] = data["previous_partner_cooperate"].notna().astype(int)
    data["cooperation_after_partner_cooperation"] = ((data["previous_partner_cooperate"] == 1) & (data["cooperate"] == 1)).astype(int)
    data["defection_after_partner_defection"] = ((data["previous_partner_cooperate"] == 0) & (data["cooperate"] == 0)).astype(int)
    data["temptation_gap"] = data["temptation_payoff"] - data["reward_payoff"]
    data["cooperation_surplus"] = 2 * data["reward_payoff"] - (data["temptation_payoff"] + data["sucker_payoff"])
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "round"])
        .agg(
            n=("cooperate", "size"),
            participants=("participant", "nunique"),
            dyads=("dyad_id", "nunique"),
            cooperation_rate=("cooperate", "mean"),
            partner_cooperation_rate=("partner_cooperate", "mean"),
            mean_payoff=("own_payoff", "mean"),
            mean_cumulative_payoff=("cumulative_payoff", "mean"),
            mean_trust=("trust_score", "mean"),
            mean_fairness=("fairness_score", "mean"),
            mean_expected_partner_cooperation=("expected_partner_cooperation", "mean"),
            mean_reputation=("reputation_visibility", "mean"),
            mean_enforcement=("institutional_enforcement", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby("condition")
        .agg(
            n=("cooperate", "size"),
            cooperation_rate=("cooperate", "mean"),
            mean_payoff=("own_payoff", "mean"),
            mean_trust=("trust_score", "mean"),
            mean_fairness=("fairness_score", "mean"),
            mean_expected_partner_cooperation=("expected_partner_cooperation", "mean"),
            mean_response_time=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_round.csv", index=False)
    condition_summary.to_csv(outputs / "summary_by_condition.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    model_text = []
    coefficient_frames = []

    glm_formulas = {
        "cooperation_model": "cooperate ~ round + previous_partner_cooperate + trust_score + fairness_score + expected_partner_cooperation + communication_access + reputation_visibility + monitoring_strength + institutional_enforcement + social_identity_salience + temptation_gap + condition",
    }

    ols_formulas = {
        "payoff_model": "own_payoff ~ cooperate * partner_cooperate + round + trust_score + fairness_score + institutional_enforcement + condition",
        "trust_model": "trust_score ~ previous_partner_cooperate + communication_access + reputation_visibility + institutional_enforcement + social_identity_salience + condition",
        "fairness_model": "fairness_score ~ own_payoff + partner_cooperate + cooperate + institutional_enforcement + condition",
        "response_time_model": "log_response_time ~ round + cooperate + partner_cooperate + trust_score + fairness_score + expected_partner_cooperation + condition",
    }

    for name, formula in glm_formulas.items():
        model = smf.glm(formula, data=data, family=sm.families.Binomial()).fit(
            cov_type="cluster", cov_kwds={"groups": data["participant"]}
        )
        model_text.append(f"\n\n=== {name} ===\n")
        model_text.append(str(model.summary()))
        coefficient_frames.append(pd.DataFrame({
            "model": name,
            "term": model.params.index,
            "estimate": model.params.values,
            "std_error": model.bse.values,
        }))

    for name, formula in ols_formulas.items():
        model = smf.ols(formula, data=data).fit(
            cov_type="cluster", cov_kwds={"groups": data["participant"]}
        )
        model_text.append(f"\n\n=== {name} ===\n")
        model_text.append(str(model.summary()))
        coefficient_frames.append(pd.DataFrame({
            "model": name,
            "term": model.params.index,
            "estimate": model.params.values,
            "std_error": model.bse.values,
        }))

    with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(model_text))

    pd.concat(coefficient_frames, ignore_index=True).to_csv(outputs / "model_coefficients.csv", index=False)


def simulate_strategy_tournament(outputs: Path, n_rounds: int = 200, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    strategies = ["always_cooperate", "always_defect", "tit_for_tat", "generous_tit_for_tat", "win_stay_lose_shift"]
    T, R, P, S = 5.0, 3.0, 1.0, 0.0
    rows = []

    def choose(strategy: str, own_hist: list[int], opp_hist: list[int]) -> int:
        if strategy == "always_cooperate":
            return 1
        if strategy == "always_defect":
            return 0
        if strategy == "tit_for_tat":
            return 1 if not opp_hist else opp_hist[-1]
        if strategy == "generous_tit_for_tat":
            if not opp_hist:
                return 1
            if opp_hist[-1] == 0 and rng.random() < 0.15:
                return 1
            return opp_hist[-1]
        if strategy == "win_stay_lose_shift":
            if not own_hist:
                return 1
            last_payoff = payoff(own_hist[-1], opp_hist[-1], T, R, P, S)
            return own_hist[-1] if last_payoff >= R else 1 - own_hist[-1]
        return 0

    for s1 in strategies:
        for s2 in strategies:
            hist1, hist2 = [], []
            score1, score2 = 0.0, 0.0
            for r in range(1, n_rounds + 1):
                c1 = choose(s1, hist1, hist2)
                c2 = choose(s2, hist2, hist1)
                p1 = payoff(c1, c2, T, R, P, S)
                p2 = payoff(c2, c1, T, R, P, S)
                score1 += p1
                score2 += p2
                hist1.append(c1)
                hist2.append(c2)
                rows.append({
                    "strategy_a": s1,
                    "strategy_b": s2,
                    "round": r,
                    "choice_a": c1,
                    "choice_b": c2,
                    "payoff_a": p1,
                    "payoff_b": p2,
                    "cumulative_a": score1,
                    "cumulative_b": score2,
                })

    tournament = pd.DataFrame(rows)
    summary = (
        tournament.groupby("strategy_a")
        .agg(
            total_payoff=("payoff_a", "sum"),
            mean_payoff=("payoff_a", "mean"),
            cooperation_rate=("choice_a", "mean"),
        )
        .reset_index()
        .sort_values("total_payoff", ascending=False)
    )

    tournament.to_csv(outputs / "strategy_tournament_rounds.csv", index=False)
    summary.to_csv(outputs / "strategy_tournament_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/prisoners_dilemma_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--dyads", type=int, default=300)
    parser.add_argument("--rounds", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulate:
        df = generate_dataset(n_dyads=args.dyads, rounds_per_dyad=args.rounds, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote simulated dataset: {args.output}")
    elif args.input:
        df = pd.read_csv(args.input)
    else:
        default_input = Path("data/prisoners_dilemma_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_strategy_tournament(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and strategy tournament outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
