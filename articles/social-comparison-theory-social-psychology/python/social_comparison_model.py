#!/usr/bin/env python3
"""
Social comparison theory research model.

This script can:
1. Generate synthetic social-comparison data.
2. Estimate self-evaluation, motivation, envy, inspiration, discouragement,
   relative deprivation, norm perception, and response-time models.
3. Simulate repeated digital comparison and organizational benchmarking dynamics.
4. Save researcher-readable summaries to outputs/.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

try:
    import statsmodels.formula.api as smf
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "control", "upward", "downward", "lateral", "attainable_upward",
    "unattainable_upward", "digital_feed", "organizational_benchmark", "relative_deprivation"
]
DOMAINS = ["ability", "income", "appearance", "status", "morality", "productivity", "health", "achievement", "belonging"]
REFERENCES = ["peers", "coworkers", "friends", "family", "influencers", "profession", "organization", "nation", "classmates"]


def generate_dataset(n_participants: int = 500, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"direction": 0.0, "attainability": 0.0, "digital": 0.0, "deprivation": 0.0},
        "upward": {"direction": 2.2, "attainability": 0.0, "digital": 0.0, "deprivation": 0.3},
        "downward": {"direction": -2.0, "attainability": 0.0, "digital": 0.0, "deprivation": -0.5},
        "lateral": {"direction": 0.0, "attainability": 0.5, "digital": 0.0, "deprivation": 0.0},
        "attainable_upward": {"direction": 2.0, "attainability": 2.4, "digital": 0.0, "deprivation": 0.2},
        "unattainable_upward": {"direction": 3.8, "attainability": -2.6, "digital": 0.6, "deprivation": 1.4},
        "digital_feed": {"direction": 3.2, "attainability": -1.2, "digital": 3.0, "deprivation": 1.1},
        "organizational_benchmark": {"direction": 2.0, "attainability": 0.5, "digital": 0.0, "deprivation": 1.0},
        "relative_deprivation": {"direction": 3.0, "attainability": -0.8, "digital": 0.2, "deprivation": 2.4},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        comparison_orientation = rng.normal(5.8, 1.5)
        baseline_self_eval = rng.normal(6.0, 1.0)
        emotion_sensitivity = rng.normal(0, 0.55)
        achievement_motive = rng.normal(0, 0.60)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            ce = condition_effects[condition]
            domain = rng.choice(DOMAINS)
            reference = rng.choice(REFERENCES)

            if condition in ["upward", "attainable_upward", "unattainable_upward", "digital_feed", "organizational_benchmark", "relative_deprivation"]:
                comparison_type = "upward"
            elif condition == "downward":
                comparison_type = "downward"
            elif condition == "lateral":
                comparison_type = "lateral"
            else:
                comparison_type = rng.choice(["upward", "downward", "lateral"], p=[0.35, 0.25, 0.40])

            self_standing = float(np.clip(rng.normal(baseline_self_eval, 1.0), 0, 10))
            if comparison_type == "upward":
                reference_standing = float(np.clip(self_standing + abs(rng.normal(ce["direction"] + 1.4, 1.1)), 0, 10))
            elif comparison_type == "downward":
                reference_standing = float(np.clip(self_standing - abs(rng.normal(abs(ce["direction"]) + 1.2, 1.0)), 0, 10))
            else:
                reference_standing = float(np.clip(self_standing + rng.normal(0, 0.8), 0, 10))

            comparison_gap = self_standing - reference_standing
            attainability = float(np.clip(rng.normal(5.4 + ce["attainability"] - 0.30 * max(0, -comparison_gap), 1.1), 0, 10))
            similarity = float(np.clip(rng.normal(5.6 - 0.20 * abs(comparison_gap) + 0.35 * (reference in ["peers", "coworkers", "classmates", "friends"]), 1.0), 0, 10))
            identity_relevance = float(np.clip(rng.normal(6.0 + 0.50 * (domain in ["achievement", "income", "status", "appearance"]) + 0.20 * comparison_orientation, 1.0), 0, 10))
            social_comparison_orientation = float(np.clip(rng.normal(comparison_orientation, 0.8), 0, 10))
            digital_exposure = float(np.clip(rng.normal(1.5 + ce["digital"] + 0.80 * (reference == "influencers"), 1.2), 0, 10))

            self_eval_pre = float(np.clip(rng.normal(baseline_self_eval, 0.65), 0, 10))

            upward_pressure = max(0.0, -comparison_gap)
            downward_reassurance = max(0.0, comparison_gap)
            unattainable_penalty = upward_pressure * max(0.0, 5.0 - attainability) / 5.0
            attainable_inspiration = upward_pressure * attainability / 10.0 * similarity / 10.0

            envy = float(np.clip(rng.normal(1.5 + 0.65 * upward_pressure + 0.35 * digital_exposure + 0.20 * identity_relevance - 0.35 * attainability + emotion_sensitivity, 1.0), 0, 10))
            inspiration = float(np.clip(rng.normal(2.2 + 0.70 * attainable_inspiration + 0.20 * similarity + 0.18 * achievement_motive, 1.0), 0, 10))
            discouragement = float(np.clip(rng.normal(1.8 + 0.75 * unattainable_penalty + 0.25 * envy - 0.25 * inspiration, 1.0), 0, 10))
            reassurance = float(np.clip(rng.normal(2.5 + 0.55 * downward_reassurance + 0.15 * similarity - 0.20 * upward_pressure, 1.0), 0, 10))
            relative_deprivation = float(np.clip(rng.normal(1.0 + 0.60 * upward_pressure + ce["deprivation"] + 0.25 * identity_relevance - 0.25 * attainability, 1.0), 0, 10))
            norm_perception = float(np.clip(rng.normal(4.2 + 0.35 * reference_standing + 0.25 * digital_exposure + 0.20 * similarity, 1.0), 0, 10))
            perceived_fairness = float(np.clip(rng.normal(6.0 - 0.35 * relative_deprivation + 0.18 * attainability - 0.20 * abs(comparison_gap), 1.0), 0, 10))

            self_eval_post = float(np.clip(
                self_eval_pre
                - 0.22 * upward_pressure * identity_relevance / 10.0
                + 0.18 * downward_reassurance
                + 0.18 * inspiration
                - 0.18 * discouragement
                - 0.10 * relative_deprivation
                + rng.normal(0, 0.45),
                0, 10
            ))

            motivation_score = float(np.clip(
                rng.normal(
                    4.0
                    + 0.40 * inspiration
                    + 0.28 * attainability
                    + 0.15 * upward_pressure
                    - 0.22 * discouragement
                    - 0.10 * relative_deprivation
                    + 0.25 * achievement_motive,
                    1.0
                ),
                0, 10
            ))

            self_esteem = float(np.clip(
                rng.normal(5.0 + 0.55 * self_eval_post + 0.18 * reassurance - 0.18 * envy - 0.20 * discouragement, 0.8),
                0, 10
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(1050)
                + 0.05 * abs(comparison_gap)
                + 0.04 * identity_relevance
                + 0.04 * relative_deprivation
                + 0.03 * social_comparison_orientation
                + rng.normal(0, 0.17)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "trial": trial,
                "comparison_type": comparison_type,
                "comparison_domain": domain,
                "reference_group": reference,
                "self_standing": round(self_standing, 3),
                "reference_standing": round(reference_standing, 3),
                "comparison_gap": round(comparison_gap, 3),
                "attainability": round(attainability, 3),
                "similarity": round(similarity, 3),
                "identity_relevance": round(identity_relevance, 3),
                "social_comparison_orientation": round(social_comparison_orientation, 3),
                "self_eval_pre": round(self_eval_pre, 3),
                "self_eval_post": round(self_eval_post, 3),
                "motivation_score": round(motivation_score, 3),
                "envy": round(envy, 3),
                "inspiration": round(inspiration, 3),
                "discouragement": round(discouragement, 3),
                "reassurance": round(reassurance, 3),
                "self_esteem": round(self_esteem, 3),
                "perceived_fairness": round(perceived_fairness, 3),
                "relative_deprivation": round(relative_deprivation, 3),
                "norm_perception": round(norm_perception, 3),
                "digital_exposure": round(digital_exposure, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = df.copy()
    data["self_eval_change"] = data["self_eval_post"] - data["self_eval_pre"]

    comparison_summary = (
        data.groupby(["condition", "comparison_type"])
        .agg(
            n=("self_eval_change", "size"),
            participants=("participant", "nunique"),
            mean_gap=("comparison_gap", "mean"),
            mean_attainability=("attainability", "mean"),
            mean_similarity=("similarity", "mean"),
            mean_identity_relevance=("identity_relevance", "mean"),
            mean_self_eval_change=("self_eval_change", "mean"),
            mean_motivation=("motivation_score", "mean"),
            mean_envy=("envy", "mean"),
            mean_inspiration=("inspiration", "mean"),
            mean_discouragement=("discouragement", "mean"),
            mean_reassurance=("reassurance", "mean"),
            mean_self_esteem=("self_esteem", "mean"),
            mean_relative_deprivation=("relative_deprivation", "mean"),
            mean_norm_perception=("norm_perception", "mean"),
            mean_digital_exposure=("digital_exposure", "mean"),
        )
        .reset_index()
    )

    domain_summary = (
        data.groupby(["comparison_domain", "comparison_type"])
        .agg(
            n=("self_eval_change", "size"),
            mean_self_eval_change=("self_eval_change", "mean"),
            mean_motivation=("motivation_score", "mean"),
            mean_relative_deprivation=("relative_deprivation", "mean"),
            mean_envy=("envy", "mean"),
            mean_inspiration=("inspiration", "mean"),
        )
        .reset_index()
    )

    comparison_summary.to_csv(outputs / "summary_by_condition_comparison_type.csv", index=False)
    domain_summary.to_csv(outputs / "summary_by_domain_comparison_type.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = df.copy()
    data["self_eval_change"] = data["self_eval_post"] - data["self_eval_pre"]
    data["log_response_time"] = np.log(data["response_time_ms"])

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "self_evaluation_change_model": "self_eval_change ~ comparison_type * attainability + comparison_gap + similarity + identity_relevance + social_comparison_orientation + condition + comparison_domain",
        "motivation_model": "motivation_score ~ comparison_type * attainability + comparison_gap + similarity + identity_relevance + inspiration + discouragement + condition + comparison_domain",
        "envy_model": "envy ~ comparison_gap + attainability + similarity + identity_relevance + social_comparison_orientation + digital_exposure + condition + comparison_domain",
        "inspiration_model": "inspiration ~ comparison_type * attainability + comparison_gap + similarity + identity_relevance + condition + comparison_domain",
        "relative_deprivation_model": "relative_deprivation ~ comparison_gap + attainability + identity_relevance + perceived_fairness + condition + reference_group",
        "self_esteem_model": "self_esteem ~ self_eval_post + envy + inspiration + discouragement + reassurance + relative_deprivation + condition",
        "response_time_model": "log_response_time ~ comparison_type * identity_relevance + comparison_gap + attainability + relative_deprivation + social_comparison_orientation + condition",
    }

    model_text = []
    coefficient_frames = []
    for name, formula in formulas.items():
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


def simulate_digital_exposure(outputs: Path, n_people: int = 1000, days: int = 30, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    records = []

    baseline_self_eval = rng.uniform(4.5, 7.0, n_people)
    orientation = rng.uniform(0, 10, n_people)
    self_eval = baseline_self_eval.copy()

    for day in range(1, days + 1):
        exposure = rng.gamma(shape=2.0, scale=1.2, size=n_people)
        upward_gap = np.maximum(0, rng.normal(2.0 + 0.20 * exposure, 1.0, n_people))
        attainability = np.clip(rng.normal(4.5 - 0.25 * exposure, 1.0, n_people), 0, 10)
        inspiration = np.clip(0.30 * upward_gap * attainability / 10 + rng.normal(0, 0.4, n_people), 0, 10)
        discouragement = np.clip(0.28 * upward_gap * np.maximum(0, 5 - attainability) / 5 + 0.05 * exposure + rng.normal(0, 0.4, n_people), 0, 10)

        self_eval = np.clip(
            self_eval
            - 0.04 * upward_gap * orientation / 10
            + 0.05 * inspiration
            - 0.05 * discouragement,
            0, 10
        )

        records.append(pd.DataFrame({
            "day": day,
            "participant": np.arange(1, n_people + 1),
            "digital_exposure": exposure,
            "upward_gap": upward_gap,
            "attainability": attainability,
            "inspiration": inspiration,
            "discouragement": discouragement,
            "self_eval": self_eval,
        }))

    sim = pd.concat(records, ignore_index=True)
    daily = (
        sim.groupby("day")
        .agg(
            mean_digital_exposure=("digital_exposure", "mean"),
            mean_upward_gap=("upward_gap", "mean"),
            mean_attainability=("attainability", "mean"),
            mean_inspiration=("inspiration", "mean"),
            mean_discouragement=("discouragement", "mean"),
            mean_self_eval=("self_eval", "mean"),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "digital_comparison_simulation.csv", index=False)
    daily.to_csv(outputs / "digital_comparison_daily_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/social_comparison_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=500)
    parser.add_argument("--trials", type=int, default=6)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulate:
        df = generate_dataset(n_participants=args.participants, trials_per_participant=args.trials, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote simulated dataset: {args.output}")
    elif args.input:
        df = pd.read_csv(args.input)
    else:
        default_input = Path("data/social_comparison_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_digital_exposure(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
