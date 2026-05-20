#!/usr/bin/env python3
"""
Self-serving bias research model.

This script can:
1. Generate synthetic attribution data for success/failure outcomes.
2. Estimate internal attribution, external attribution, responsibility,
   blame, credit, excuse-making, learning intention, and response-time models.
3. Compute self-serving bias scores and accountability effects.
4. Simulate organizational credit/blame learning dynamics.
5. Save researcher-readable summaries to outputs/.
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
    "control", "ego_threat", "accountability", "public_review",
    "private_feedback", "high_evidence", "ambiguous_evidence",
    "team_context", "leadership_context"
]
TARGETS = ["self", "other", "team", "leader", "institution", "outgroup"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 500, trials_per_participant: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"threat": 0.0, "accountability": 0.0, "evidence": 0.0, "public": 0.0},
        "ego_threat": {"threat": 2.8, "accountability": -0.2, "evidence": -0.2, "public": 0.0},
        "accountability": {"threat": -0.2, "accountability": 3.0, "evidence": 1.0, "public": 0.8},
        "public_review": {"threat": 1.2, "accountability": 2.6, "evidence": 1.0, "public": 2.4},
        "private_feedback": {"threat": 0.7, "accountability": -0.8, "evidence": -0.4, "public": -1.0},
        "high_evidence": {"threat": -0.2, "accountability": 1.2, "evidence": 3.0, "public": 0.3},
        "ambiguous_evidence": {"threat": 1.0, "accountability": -0.4, "evidence": -2.0, "public": 0.0},
        "team_context": {"threat": 0.8, "accountability": 0.4, "evidence": 0.0, "public": 0.5},
        "leadership_context": {"threat": 1.5, "accountability": 1.0, "evidence": 0.4, "public": 1.2},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        baseline_self_esteem = rng.normal(6.2, 1.1)
        defensive_orientation = rng.normal(0, 0.65)
        accountability_disposition = rng.normal(0, 0.50)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            ce = condition_effects[condition]
            outcome_valence = rng.choice(["positive", "negative", "mixed", "ambiguous"], p=[0.36, 0.36, 0.14, 0.14])
            actor_target = rng.choice(TARGETS, p=[0.45, 0.22, 0.12, 0.08, 0.08, 0.05])
            self_other = "self" if actor_target in ["self", "team"] else "other"

            self_relevance = 1.0 if self_other == "self" else 0.25
            positive = 1.0 if outcome_valence == "positive" else 0.0
            negative = 1.0 if outcome_valence == "negative" else 0.0
            mixed_or_ambiguous = 1.0 if outcome_valence in ["mixed", "ambiguous"] else 0.0

            self_esteem = float(np.clip(rng.normal(baseline_self_esteem, 0.75), 0, 10))
            ego_threat = float(np.clip(rng.normal(2.4 + ce["threat"] + 2.2 * negative * self_relevance + 0.7 * mixed_or_ambiguous, 1.0), 0, 10))
            task_importance = float(np.clip(rng.normal(5.4 + 1.2 * self_relevance + 0.4 * ce["public"], 1.0), 0, 10))
            outcome_expectancy = float(np.clip(rng.normal(5.2 + 0.6 * positive - 0.6 * negative, 1.1), 0, 10))
            evidence_strength = float(np.clip(rng.normal(5.0 + ce["evidence"], 1.1), 0, 10))
            accountability_pressure = float(np.clip(rng.normal(4.0 + ce["accountability"] + ce["public"] + accountability_disposition, 1.0), 0, 10))
            perceived_fairness = float(np.clip(rng.normal(5.6 + 0.25 * evidence_strength - 0.18 * ego_threat, 1.0), 0, 10))

            # Self-serving force increases with threat and self-relevance, and declines with accountability/evidence.
            self_serving_force = (
                self_relevance
                * (0.38 * ego_threat + 0.30 * task_importance + 0.28 * defensive_orientation + 0.18 * self_esteem)
                - 0.30 * accountability_pressure
                - 0.22 * evidence_strength
            )

            internal_attribution = float(np.clip(
                rng.normal(
                    5.0
                    + 1.4 * positive * self_relevance
                    - 1.2 * negative * self_relevance
                    + 0.33 * self_serving_force * (positive - negative)
                    + 0.20 * evidence_strength * positive
                    - 0.15 * evidence_strength * negative,
                    1.0
                ),
                0, 10
            ))

            external_attribution = float(np.clip(
                rng.normal(
                    5.0
                    - 1.0 * positive * self_relevance
                    + 1.5 * negative * self_relevance
                    - 0.25 * self_serving_force * (positive - negative)
                    + 0.18 * evidence_strength * negative
                    - 0.10 * accountability_pressure,
                    1.0
                ),
                0, 10
            ))

            stable_attribution = float(np.clip(
                rng.normal(4.5 + 0.40 * internal_attribution - 0.18 * external_attribution + 0.20 * positive - 0.15 * negative, 1.0),
                0, 10
            ))

            controllable_attribution = float(np.clip(
                rng.normal(4.8 + 0.35 * internal_attribution - 0.20 * external_attribution + 0.18 * accountability_pressure, 1.0),
                0, 10
            ))

            responsibility_rating = float(np.clip(
                rng.normal(2.0 + 0.55 * internal_attribution - 0.25 * external_attribution + 0.20 * controllable_attribution + 0.12 * evidence_strength, 1.0),
                0, 10
            ))

            blame_rating = float(np.clip(
                rng.normal(1.4 + 0.85 * negative + 0.25 * responsibility_rating + 0.15 * ego_threat - 0.12 * external_attribution, 1.0),
                0, 10
            ))

            credit_claiming = float(np.clip(
                rng.normal(1.5 + 0.85 * positive + 0.45 * internal_attribution * self_relevance - 0.15 * accountability_pressure, 1.0),
                0, 10
            ))

            excuse_making = float(np.clip(
                rng.normal(1.5 + 0.85 * negative * self_relevance + 0.45 * external_attribution + 0.18 * ego_threat - 0.25 * accountability_pressure - 0.18 * evidence_strength, 1.0),
                0, 10
            ))

            learning_intention = float(np.clip(
                rng.normal(
                    4.5
                    + 0.28 * accountability_pressure
                    + 0.25 * evidence_strength
                    + 0.16 * responsibility_rating
                    - 0.22 * excuse_making
                    - 0.16 * self_serving_force * negative,
                    1.0
                ),
                0, 10
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(1050)
                + 0.05 * ego_threat
                + 0.04 * task_importance
                + 0.04 * abs(internal_attribution - external_attribution)
                - 0.03 * evidence_strength
                + rng.normal(0, 0.17)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "trial": trial,
                "outcome_valence": outcome_valence,
                "actor_target": actor_target,
                "self_other": self_other,
                "internal_attribution": round(internal_attribution, 3),
                "external_attribution": round(external_attribution, 3),
                "stable_attribution": round(stable_attribution, 3),
                "controllable_attribution": round(controllable_attribution, 3),
                "responsibility_rating": round(responsibility_rating, 3),
                "blame_rating": round(blame_rating, 3),
                "credit_claiming": round(credit_claiming, 3),
                "excuse_making": round(excuse_making, 3),
                "self_esteem": round(self_esteem, 3),
                "ego_threat": round(ego_threat, 3),
                "task_importance": round(task_importance, 3),
                "outcome_expectancy": round(outcome_expectancy, 3),
                "perceived_fairness": round(perceived_fairness, 3),
                "evidence_strength": round(evidence_strength, 3),
                "learning_intention": round(learning_intention, 3),
                "accountability_pressure": round(accountability_pressure, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)

    summary = (
        df.groupby(["condition", "outcome_valence", "self_other"])
        .agg(
            n=("internal_attribution", "size"),
            participants=("participant", "nunique"),
            mean_internal=("internal_attribution", "mean"),
            mean_external=("external_attribution", "mean"),
            mean_responsibility=("responsibility_rating", "mean"),
            mean_blame=("blame_rating", "mean"),
            mean_credit=("credit_claiming", "mean"),
            mean_excuse=("excuse_making", "mean"),
            mean_ego_threat=("ego_threat", "mean"),
            mean_learning=("learning_intention", "mean"),
            mean_accountability=("accountability_pressure", "mean"),
            mean_evidence=("evidence_strength", "mean"),
        )
        .reset_index()
    )

    ssb_records = []
    for (participant, self_other), g in df.groupby(["participant", "self_other"]):
        pos = g[g["outcome_valence"] == "positive"]
        neg = g[g["outcome_valence"] == "negative"]
        if len(pos) and len(neg):
            ssb_records.append({
                "participant": participant,
                "self_other": self_other,
                "internal_success": pos["internal_attribution"].mean(),
                "internal_failure": neg["internal_attribution"].mean(),
                "external_success": pos["external_attribution"].mean(),
                "external_failure": neg["external_attribution"].mean(),
                "ssb_internal": pos["internal_attribution"].mean() - neg["internal_attribution"].mean(),
                "ssb_external": neg["external_attribution"].mean() - pos["external_attribution"].mean(),
                "ssb_full": (
                    pos["internal_attribution"].mean()
                    - neg["internal_attribution"].mean()
                    + neg["external_attribution"].mean()
                    - pos["external_attribution"].mean()
                ),
            })
    ssb_scores = pd.DataFrame(ssb_records)

    summary.to_csv(outputs / "summary_by_condition_valence_self_other.csv", index=False)
    ssb_scores.to_csv(outputs / "self_serving_bias_scores.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = df.copy()
    data["log_response_time"] = np.log(data["response_time_ms"])

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "internal_attribution_model": "internal_attribution ~ outcome_valence * self_other + ego_threat + self_esteem + task_importance + evidence_strength + accountability_pressure + condition + actor_target",
        "external_attribution_model": "external_attribution ~ outcome_valence * self_other + ego_threat + self_esteem + task_importance + evidence_strength + accountability_pressure + condition + actor_target",
        "responsibility_model": "responsibility_rating ~ internal_attribution + external_attribution + controllable_attribution + outcome_valence * self_other + evidence_strength + accountability_pressure + condition",
        "blame_model": "blame_rating ~ outcome_valence * self_other + internal_attribution + external_attribution + responsibility_rating + ego_threat + condition",
        "credit_model": "credit_claiming ~ outcome_valence * self_other + internal_attribution + self_esteem + ego_threat + accountability_pressure + condition",
        "excuse_model": "excuse_making ~ outcome_valence * self_other + external_attribution + ego_threat + evidence_strength + accountability_pressure + condition",
        "learning_model": "learning_intention ~ responsibility_rating + excuse_making + evidence_strength + accountability_pressure + outcome_valence + self_other + condition",
        "response_time_model": "log_response_time ~ outcome_valence * self_other + ego_threat + task_importance + evidence_strength + accountability_pressure + condition",
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


def simulate_organizational_learning(outputs: Path, n_projects: int = 5000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    project_success = rng.integers(0, 2, size=n_projects)
    ego_threat = rng.uniform(0, 10, size=n_projects)
    evidence_strength = rng.uniform(0, 10, size=n_projects)
    accountability = rng.uniform(0, 10, size=n_projects)

    credit_claiming = np.clip(
        2.0 + 5.0 * project_success + 0.20 * ego_threat - 0.20 * accountability + rng.normal(0, 1.0, n_projects),
        0, 10
    )
    excuse_making = np.clip(
        2.0 + 5.0 * (1 - project_success) + 0.35 * ego_threat - 0.35 * accountability - 0.25 * evidence_strength + rng.normal(0, 1.0, n_projects),
        0, 10
    )
    learning = np.clip(
        4.0 + 0.40 * accountability + 0.35 * evidence_strength - 0.40 * excuse_making + rng.normal(0, 1.0, n_projects),
        0, 10
    )

    sim = pd.DataFrame({
        "project_id": np.arange(1, n_projects + 1),
        "project_success": project_success,
        "ego_threat": ego_threat,
        "evidence_strength": evidence_strength,
        "accountability": accountability,
        "credit_claiming": credit_claiming,
        "excuse_making": excuse_making,
        "learning": learning,
    })

    sim["success_label"] = np.where(sim["project_success"] == 1, "success", "failure")

    summary = (
        sim.groupby("success_label")
        .agg(
            n=("learning", "size"),
            mean_credit_claiming=("credit_claiming", "mean"),
            mean_excuse_making=("excuse_making", "mean"),
            mean_learning=("learning", "mean"),
            mean_accountability=("accountability", "mean"),
            mean_evidence=("evidence_strength", "mean"),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "organizational_learning_simulation.csv", index=False)
    summary.to_csv(outputs / "organizational_learning_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/self_serving_bias_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=500)
    parser.add_argument("--trials", type=int, default=8)
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
        default_input = Path("data/self_serving_bias_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_organizational_learning(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
