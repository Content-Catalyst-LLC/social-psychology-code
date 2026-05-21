#!/usr/bin/env python3
"""
Bystander effect research model.

This script can:
1. Generate synthetic bystander-intervention data.
2. Estimate intervention, intervention-likelihood, felt-responsibility, and latency models.
3. Test bystander-count, direct-assignment, emergency-clarity, shared-identity, and online-context effects.
4. Simulate diffusion-of-responsibility and intervention-threshold dynamics.
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
    import statsmodels.api as sm
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "alone", "small_group", "large_group", "ambiguous_emergency", "clear_emergency",
    "direct_assignment", "shared_identity", "online_harassment",
    "trained_bystander", "high_evaluation_risk"
]

CONTEXT_TYPES = ["laboratory", "field", "online", "organization", "classroom", "public_space", "platform"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 500, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "alone": {"bystanders": 0, "clarity": 8.0, "danger": 7.0, "identity": 4.0, "direct": 0, "leader": 0, "norm": 6.0, "online": 0, "eval": 2.0, "competence": 7.0},
        "small_group": {"bystanders": 3, "clarity": 7.5, "danger": 7.0, "identity": 4.0, "direct": 0, "leader": 0, "norm": 5.0, "online": 0, "eval": 3.5, "competence": 6.5},
        "large_group": {"bystanders": 10, "clarity": 7.5, "danger": 7.0, "identity": 3.5, "direct": 0, "leader": 0, "norm": 4.5, "online": 0, "eval": 4.5, "competence": 6.0},
        "ambiguous_emergency": {"bystanders": 5, "clarity": 3.0, "danger": 4.5, "identity": 3.5, "direct": 0, "leader": 0, "norm": 3.0, "online": 0, "eval": 6.5, "competence": 4.0},
        "clear_emergency": {"bystanders": 5, "clarity": 9.0, "danger": 8.0, "identity": 5.5, "direct": 0, "leader": 0, "norm": 6.5, "online": 0, "eval": 3.5, "competence": 6.5},
        "direct_assignment": {"bystanders": 8, "clarity": 8.5, "danger": 8.0, "identity": 5.5, "direct": 1, "leader": 1, "norm": 8.0, "online": 0, "eval": 3.0, "competence": 7.5},
        "shared_identity": {"bystanders": 7, "clarity": 7.5, "danger": 6.8, "identity": 8.5, "direct": 0, "leader": 1, "norm": 8.0, "online": 0, "eval": 3.5, "competence": 7.0},
        "online_harassment": {"bystanders": 36, "clarity": 6.5, "danger": 5.8, "identity": 4.0, "direct": 0, "leader": 0, "norm": 4.0, "online": 1, "eval": 6.2, "competence": 5.5},
        "trained_bystander": {"bystanders": 32, "clarity": 7.0, "danger": 6.0, "identity": 6.0, "direct": 1, "leader": 1, "norm": 8.0, "online": 1, "eval": 3.0, "competence": 8.5},
        "high_evaluation_risk": {"bystanders": 4, "clarity": 6.5, "danger": 5.5, "identity": 4.0, "direct": 0, "leader": 0, "norm": 4.5, "online": 0, "eval": 8.5, "competence": 5.0},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        helping_disposition = float(np.clip(rng.normal(5.8, 1.5), 0, 10))
        anxiety = float(np.clip(rng.normal(4.2, 1.6), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context_type = rng.choice(CONTEXT_TYPES)
            scenario_id = f"SC{rng.integers(1, 80):03d}"
            e = effects[condition]

            actual_bystander_count = int(max(0, round(rng.normal(e["bystanders"], max(1.0, e["bystanders"] * 0.12)))))
            perceived_bystander_count = int(max(0, round(actual_bystander_count + rng.normal(0, max(1.0, actual_bystander_count * 0.08)))))

            emergency_clarity = float(np.clip(rng.normal(e["clarity"], 1.0), 0, 10))
            danger_level = float(np.clip(rng.normal(e["danger"], 1.1), 0, 10))
            victim_identifiability = float(np.clip(rng.normal(5.5 + 0.10 * e["identity"], 1.2), 0, 10))
            shared_identity = float(np.clip(rng.normal(e["identity"], 1.2), 0, 10))
            direct_assignment = int(e["direct"])
            leadership_cue = int(e["leader"])
            intervention_norm_salience = float(np.clip(rng.normal(e["norm"], 1.0), 0, 10))
            online_context = int(e["online"])
            platform_traceability = float(np.clip(rng.normal(5.0 if online_context else 1.0, 1.5), 0, 10))
            moderation_visibility = float(np.clip(rng.normal(6.8 if condition == "trained_bystander" else 3.5 if online_context else 1.0, 1.4), 0, 10))

            diffusion_responsibility = float(np.clip(
                rng.normal(
                    1.0
                    + 1.25 * math.log1p(perceived_bystander_count)
                    - 2.5 * direct_assignment
                    - 1.2 * leadership_cue
                    - 0.35 * shared_identity,
                    1.1
                ),
                0, 10
            ))

            pluralistic_ignorance = float(np.clip(
                rng.normal(
                    6.5
                    - 0.65 * emergency_clarity
                    + 0.30 * math.log1p(perceived_bystander_count)
                    - 0.35 * leadership_cue
                    - 0.25 * intervention_norm_salience,
                    1.2
                ),
                0, 10
            ))

            evaluation_apprehension = float(np.clip(
                rng.normal(
                    e["eval"]
                    + 0.28 * anxiety
                    + 0.18 * perceived_bystander_count / 10
                    - 0.22 * emergency_clarity
                    - 0.30 * direct_assignment,
                    1.0
                ),
                0, 10
            ))

            perceived_competence = float(np.clip(
                rng.normal(
                    e["competence"]
                    + 0.35 * (condition == "trained_bystander")
                    + 0.15 * intervention_norm_salience
                    - 0.15 * pluralistic_ignorance,
                    1.0
                ),
                0, 10
            ))

            intervention_cost = float(np.clip(
                rng.normal(
                    2.5
                    + 0.45 * danger_level
                    + 0.25 * evaluation_apprehension
                    + 0.40 * online_context
                    - 0.25 * perceived_competence,
                    1.0
                ),
                0, 10
            ))

            felt_responsibility = float(np.clip(
                rng.normal(
                    8.5
                    - 0.80 * diffusion_responsibility
                    + 1.8 * direct_assignment
                    + 0.55 * leadership_cue
                    + 0.35 * shared_identity
                    + 0.30 * victim_identifiability
                    + 0.25 * intervention_norm_salience
                    + 0.15 * helping_disposition,
                    1.0
                ),
                0, 10
            ))

            latent = (
                -5.0
                + 0.42 * felt_responsibility
                + 0.38 * emergency_clarity
                + 0.22 * danger_level
                + 0.24 * victim_identifiability
                + 0.26 * shared_identity
                + 0.35 * perceived_competence
                + 0.22 * intervention_norm_salience
                + 0.60 * direct_assignment
                + 0.35 * leadership_cue
                - 0.42 * diffusion_responsibility
                - 0.34 * pluralistic_ignorance
                - 0.28 * evaluation_apprehension
                - 0.30 * intervention_cost
                + 0.10 * platform_traceability
                + 0.15 * moderation_visibility
            )

            intervention_prob = float(logistic(latent))
            actual_intervention = int(rng.random() < intervention_prob)
            intervention_likelihood = float(np.clip(100 * intervention_prob + rng.normal(0, 6), 0, 100))

            response_confidence = float(np.clip(
                rng.normal(
                    1.5
                    + 0.35 * emergency_clarity
                    + 0.35 * perceived_competence
                    + 0.20 * felt_responsibility
                    - 0.25 * pluralistic_ignorance,
                    1.0
                ),
                0, 10
            ))

            intervention_latency_ms = int(np.clip(np.exp(
                math.log(2600)
                + 0.055 * perceived_bystander_count
                + 0.06 * pluralistic_ignorance
                + 0.055 * evaluation_apprehension
                + 0.045 * intervention_cost
                - 0.065 * emergency_clarity
                - 0.070 * direct_assignment
                - 0.045 * perceived_competence
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "condition": condition,
                "context_type": context_type,
                "trial": t,
                "actual_bystander_count": actual_bystander_count,
                "perceived_bystander_count": perceived_bystander_count,
                "emergency_clarity": round(emergency_clarity, 3),
                "danger_level": round(danger_level, 3),
                "victim_identifiability": round(victim_identifiability, 3),
                "shared_identity": round(shared_identity, 3),
                "felt_responsibility": round(felt_responsibility, 3),
                "diffusion_responsibility": round(diffusion_responsibility, 3),
                "pluralistic_ignorance": round(pluralistic_ignorance, 3),
                "evaluation_apprehension": round(evaluation_apprehension, 3),
                "perceived_competence": round(perceived_competence, 3),
                "intervention_cost": round(intervention_cost, 3),
                "direct_assignment": direct_assignment,
                "leadership_cue": leadership_cue,
                "intervention_norm_salience": round(intervention_norm_salience, 3),
                "online_context": online_context,
                "platform_traceability": round(platform_traceability, 3),
                "moderation_visibility": round(moderation_visibility, 3),
                "intervention_likelihood": round(intervention_likelihood, 3),
                "actual_intervention": actual_intervention,
                "intervention_latency_ms": intervention_latency_ms,
                "response_confidence": round(response_confidence, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["log_perceived_bystanders"] = np.log1p(data["perceived_bystander_count"])
    data["responsibility_assignment_index"] = (
        data["felt_responsibility"]
        + 2.0 * data["direct_assignment"]
        + 1.4 * data["leadership_cue"]
        + data["intervention_norm_salience"]
    ) / 4.0
    data["ambiguity_index"] = (
        data["pluralistic_ignorance"]
        + data["evaluation_apprehension"]
        + (10 - data["emergency_clarity"])
    ) / 3.0
    data["helping_capacity_index"] = (
        data["perceived_competence"]
        + data["response_confidence"]
        + data["intervention_norm_salience"]
        - data["intervention_cost"]
    ) / 3.0
    data["log_latency"] = np.log(data["intervention_latency_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "context_type"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_perceived_bystanders=("perceived_bystander_count", "mean"),
            intervention_rate=("actual_intervention", "mean"),
            mean_intervention_likelihood=("intervention_likelihood", "mean"),
            mean_latency=("intervention_latency_ms", "mean"),
            mean_responsibility=("felt_responsibility", "mean"),
            mean_diffusion=("diffusion_responsibility", "mean"),
            mean_pluralistic_ignorance=("pluralistic_ignorance", "mean"),
            mean_evaluation_apprehension=("evaluation_apprehension", "mean"),
            mean_clarity=("emergency_clarity", "mean"),
            mean_competence=("perceived_competence", "mean"),
            mean_assignment_index=("responsibility_assignment_index", "mean"),
        )
        .reset_index()
    )

    bystander_summary = (
        data.assign(
            bystander_band=pd.cut(
                data["perceived_bystander_count"],
                bins=[-0.1, 0, 3, 10, 10000],
                labels=["alone", "small_group", "medium_group", "large_group"]
            )
        )
        .groupby(["condition", "bystander_band"], observed=True)
        .agg(
            n=("participant", "size"),
            intervention_rate=("actual_intervention", "mean"),
            mean_likelihood=("intervention_likelihood", "mean"),
            mean_latency=("intervention_latency_ms", "mean"),
            mean_responsibility=("felt_responsibility", "mean"),
            mean_diffusion=("diffusion_responsibility", "mean"),
            mean_ambiguity=("ambiguity_index", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    bystander_summary.to_csv(outputs / "summary_by_condition_bystander_band.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "intervention_model": "actual_intervention ~ log_perceived_bystanders + emergency_clarity + danger_level + victim_identifiability + shared_identity + felt_responsibility + diffusion_responsibility + pluralistic_ignorance + evaluation_apprehension + perceived_competence + intervention_cost + direct_assignment + leadership_cue + intervention_norm_salience + online_context + platform_traceability + moderation_visibility + condition + context_type",
        "likelihood_model": "intervention_likelihood ~ log_perceived_bystanders + emergency_clarity + danger_level + victim_identifiability + shared_identity + felt_responsibility + diffusion_responsibility + pluralistic_ignorance + evaluation_apprehension + perceived_competence + intervention_cost + direct_assignment + leadership_cue + condition + context_type",
        "responsibility_model": "felt_responsibility ~ log_perceived_bystanders + direct_assignment + leadership_cue + shared_identity + victim_identifiability + emergency_clarity + intervention_norm_salience + diffusion_responsibility + condition + context_type",
        "latency_model": "log_latency ~ log_perceived_bystanders + emergency_clarity + pluralistic_ignorance + evaluation_apprehension + intervention_cost + direct_assignment + leadership_cue + perceived_competence + actual_intervention + condition + context_type",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name == "intervention_model":
            model = smf.glm(formula, data=data, family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": data["participant"]}
            )
        else:
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


def simulate_bystander_threshold(outputs: Path, n_cases: int = 8000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    for condition in ["alone", "large_group", "direct_assignment", "shared_identity", "trained_bystander", "online_harassment"]:
        for _ in range(n_cases):
            perceived_bystanders = {
                "alone": 0,
                "large_group": 12,
                "direct_assignment": 12,
                "shared_identity": 10,
                "trained_bystander": 30,
                "online_harassment": 30,
            }[condition]

            emergency_clarity = {
                "alone": 8.0,
                "large_group": 7.5,
                "direct_assignment": 8.5,
                "shared_identity": 7.5,
                "trained_bystander": 7.5,
                "online_harassment": 6.2,
            }[condition] + rng.normal(0, 0.8)

            direct_assignment = 1 if condition in ["direct_assignment", "trained_bystander"] else 0
            shared_identity = 8.0 if condition == "shared_identity" else 6.0 if condition == "trained_bystander" else 4.0
            competence = 8.5 if condition == "trained_bystander" else 6.0
            eval_app = 6.2 if condition == "online_harassment" else 3.0
            diffusion = np.clip(1 + 1.25 * np.log1p(perceived_bystanders) - 2.5 * direct_assignment - 0.4 * shared_identity, 0, 10)
            responsibility = np.clip(8.5 - 0.80 * diffusion + 1.8 * direct_assignment + 0.35 * shared_identity, 0, 10)
            latent = -4.0 + 0.55 * responsibility + 0.35 * emergency_clarity + 0.30 * competence - 0.35 * eval_app - 0.40 * diffusion
            prob = float(logistic(latent))
            intervention = int(rng.random() < prob)

            rows.append({
                "condition": condition,
                "perceived_bystanders": perceived_bystanders,
                "emergency_clarity": emergency_clarity,
                "direct_assignment": direct_assignment,
                "shared_identity": shared_identity,
                "perceived_competence": competence,
                "evaluation_apprehension": eval_app,
                "diffusion_responsibility": diffusion,
                "felt_responsibility": responsibility,
                "intervention_probability": prob,
                "actual_intervention": intervention,
            })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby("condition")
        .agg(
            n=("condition", "size"),
            mean_bystanders=("perceived_bystanders", "mean"),
            mean_responsibility=("felt_responsibility", "mean"),
            mean_diffusion=("diffusion_responsibility", "mean"),
            mean_probability=("intervention_probability", "mean"),
            intervention_rate=("actual_intervention", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "bystander_threshold_simulation.csv", index=False)
    summary.to_csv(outputs / "bystander_threshold_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/bystander_effect_trials.csv"))
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
        default_input = Path("data/bystander_effect_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_bystander_threshold(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
