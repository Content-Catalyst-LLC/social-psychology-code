#!/usr/bin/env python3
"""
Diffusion of responsibility research model.

This script can:
1. Generate synthetic diffusion-of-responsibility data.
2. Estimate intervention, reporting, perceived responsibility, delay, and response-time models.
3. Compute pluralistic ignorance and responsibility diffusion scores.
4. Simulate organizational fragmentation and collective inaction over time.
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
    "alone", "small_group", "large_group", "ambiguous", "clear_emergency",
    "direct_appeal", "role_assigned", "evaluation_high", "leadership_cue",
    "organizational_fragmentation"
]
DOMAINS = ["emergency", "workplace", "school", "public_safety", "healthcare", "technology", "environment", "governance"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 600, trials_per_participant: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "alone": {"bystanders": 0, "ambiguity": -1.5, "role": 1.5, "evaluation": -1.2, "leader": 0, "fragment": -2, "direct": 0},
        "small_group": {"bystanders": 2, "ambiguity": 0.0, "role": 0.2, "evaluation": 0.5, "leader": 0, "fragment": 0, "direct": 0},
        "large_group": {"bystanders": 8, "ambiguity": 0.8, "role": -0.8, "evaluation": 1.0, "leader": -0.2, "fragment": 1.5, "direct": 0},
        "ambiguous": {"bystanders": 5, "ambiguity": 3.0, "role": -1.0, "evaluation": 1.0, "leader": -0.4, "fragment": 1.0, "direct": 0},
        "clear_emergency": {"bystanders": 6, "ambiguity": -3.0, "role": 0.8, "evaluation": -0.2, "leader": 0.2, "fragment": 0.0, "direct": 0},
        "direct_appeal": {"bystanders": 7, "ambiguity": -0.8, "role": 2.4, "evaluation": -0.5, "leader": 0.8, "fragment": -1.0, "direct": 3.0},
        "role_assigned": {"bystanders": 10, "ambiguity": -0.4, "role": 3.2, "evaluation": -0.2, "leader": 1.0, "fragment": -1.2, "direct": 2.0},
        "evaluation_high": {"bystanders": 4, "ambiguity": 0.8, "role": -0.2, "evaluation": 3.4, "leader": -0.2, "fragment": 0.8, "direct": 0},
        "leadership_cue": {"bystanders": 8, "ambiguity": -0.6, "role": 1.8, "evaluation": -0.4, "leader": 3.4, "fragment": -0.8, "direct": 1.0},
        "organizational_fragmentation": {"bystanders": 12, "ambiguity": 1.2, "role": -1.6, "evaluation": 0.8, "leader": -0.4, "fragment": 3.4, "direct": 0},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        prosocial_orientation = rng.normal(6.0, 1.1)
        efficacy_trait = rng.normal(5.8, 1.0)
        social_anxiety = rng.normal(4.5, 1.2)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            domain = rng.choice(DOMAINS)
            e = effects[condition]

            bystander_count = max(0, int(round(rng.normal(e["bystanders"], 1.2))))
            group_size = bystander_count + 1

            ambiguity_level = float(np.clip(rng.normal(4.8 + e["ambiguity"], 1.0), 0, 10))
            private_concern = float(np.clip(rng.normal(6.6 + 0.7 * (domain in ["emergency", "healthcare", "public_safety"]) - 0.18 * ambiguity_level, 1.0), 0, 10))
            perceived_group_concern = float(np.clip(rng.normal(private_concern - 0.35 * ambiguity_level - 0.18 * bystander_count + 0.25 * e["leader"], 1.0), 0, 10))
            evaluation_apprehension = float(np.clip(rng.normal(social_anxiety + e["evaluation"] + 0.18 * bystander_count + 0.20 * ambiguity_level, 1.0), 0, 10))
            role_clarity = float(np.clip(rng.normal(5.0 + e["role"] + 0.30 * e["direct"], 1.0), 0, 10))
            intervention_efficacy = float(np.clip(rng.normal(efficacy_trait + 0.25 * role_clarity - 0.15 * ambiguity_level, 1.0), 0, 10))
            social_visibility = float(np.clip(rng.normal(4.0 + 0.22 * bystander_count + 0.30 * role_clarity, 1.0), 0, 10))
            leadership_cue = float(np.clip(rng.normal(3.5 + e["leader"], 1.0), 0, 10))
            accountability_assignment = float(np.clip(rng.normal(4.0 + e["role"] + e["direct"] + 0.25 * leadership_cue, 1.0), 0, 10))
            organizational_fragmentation = float(np.clip(rng.normal(3.5 + e["fragment"] + 0.18 * bystander_count, 1.0), 0, 10))

            pluralistic_ignorance_gap = private_concern - perceived_group_concern
            diffusion_pressure = math.log1p(bystander_count) + 0.30 * organizational_fragmentation + 0.20 * ambiguity_level

            perceived_responsibility = float(np.clip(rng.normal(
                6.5
                + 0.40 * role_clarity
                + 0.35 * accountability_assignment
                + 0.25 * leadership_cue
                + 0.20 * social_visibility
                - 0.55 * math.log1p(bystander_count)
                - 0.25 * ambiguity_level
                - 0.20 * evaluation_apprehension
                - 0.25 * organizational_fragmentation,
                1.0
            ) / 2.0, 0, 10))

            intervention_probability = logistic(
                -4.0
                + 0.48 * perceived_responsibility
                + 0.32 * role_clarity
                + 0.30 * intervention_efficacy
                + 0.28 * private_concern
                + 0.18 * accountability_assignment
                + 0.16 * leadership_cue
                - 0.32 * ambiguity_level
                - 0.24 * evaluation_apprehension
                - 0.30 * math.log1p(bystander_count)
                - 0.22 * organizational_fragmentation
            )
            intervention_decision = int(rng.random() < intervention_probability)

            reporting_probability = logistic(
                -3.5
                + 0.38 * perceived_responsibility
                + 0.35 * role_clarity
                + 0.35 * accountability_assignment
                + 0.22 * leadership_cue
                + 0.18 * private_concern
                - 0.22 * organizational_fragmentation
                - 0.18 * evaluation_apprehension
            )
            reporting_decision = int(rng.random() < reporting_probability)

            delay = float(np.clip(np.exp(
                math.log(45)
                + 0.07 * bystander_count
                + 0.08 * ambiguity_level
                + 0.05 * evaluation_apprehension
                + 0.04 * organizational_fragmentation
                - 0.06 * role_clarity
                - 0.05 * perceived_responsibility
                + rng.normal(0, 0.30)
            ), 0, 900))

            response_time_ms = int(np.clip(np.exp(
                math.log(1050)
                + 0.04 * ambiguity_level
                + 0.04 * evaluation_apprehension
                + 0.03 * diffusion_pressure
                - 0.03 * role_clarity
                + rng.normal(0, 0.18)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "trial": trial,
                "scenario_domain": domain,
                "bystander_count": bystander_count,
                "group_size": group_size,
                "ambiguity_level": round(ambiguity_level, 3),
                "private_concern": round(private_concern, 3),
                "perceived_group_concern": round(perceived_group_concern, 3),
                "evaluation_apprehension": round(evaluation_apprehension, 3),
                "perceived_responsibility": round(perceived_responsibility, 3),
                "role_clarity": round(role_clarity, 3),
                "intervention_efficacy": round(intervention_efficacy, 3),
                "social_visibility": round(social_visibility, 3),
                "leadership_cue": round(leadership_cue, 3),
                "accountability_assignment": round(accountability_assignment, 3),
                "organizational_fragmentation": round(organizational_fragmentation, 3),
                "intervention_decision": intervention_decision,
                "reporting_decision": reporting_decision,
                "intervention_delay_seconds": round(delay, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["pluralistic_ignorance_gap"] = data["private_concern"] - data["perceived_group_concern"]
    data["diffusion_pressure"] = np.log1p(data["bystander_count"]) + 0.30 * data["organizational_fragmentation"] + 0.20 * data["ambiguity_level"]
    data["responsibility_clarity_index"] = (data["role_clarity"] + data["accountability_assignment"] + data["leadership_cue"]) / 3
    data["log_delay"] = np.log1p(data["intervention_delay_seconds"])
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "scenario_domain"])
        .agg(
            n=("intervention_decision", "size"),
            participants=("participant", "nunique"),
            mean_bystanders=("bystander_count", "mean"),
            intervention_rate=("intervention_decision", "mean"),
            reporting_rate=("reporting_decision", "mean"),
            mean_delay=("intervention_delay_seconds", "mean"),
            mean_responsibility=("perceived_responsibility", "mean"),
            mean_role_clarity=("role_clarity", "mean"),
            mean_ambiguity=("ambiguity_level", "mean"),
            mean_evaluation=("evaluation_apprehension", "mean"),
            mean_pluralistic_gap=("pluralistic_ignorance_gap", "mean"),
            mean_diffusion_pressure=("diffusion_pressure", "mean"),
        )
        .reset_index()
    )

    group_summary = (
        data.assign(
            bystander_band=pd.cut(data["bystander_count"], bins=[-0.1, 0, 2, 6, 100], labels=["alone", "small", "medium", "large"])
        )
        .groupby("bystander_band", observed=True)
        .agg(
            n=("intervention_decision", "size"),
            intervention_rate=("intervention_decision", "mean"),
            reporting_rate=("reporting_decision", "mean"),
            mean_responsibility=("perceived_responsibility", "mean"),
            mean_delay=("intervention_delay_seconds", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_domain.csv", index=False)
    group_summary.to_csv(outputs / "summary_by_bystander_band.csv", index=False)


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
        "intervention_model": "intervention_decision ~ bystander_count + ambiguity_level + evaluation_apprehension + private_concern + perceived_responsibility + role_clarity + intervention_efficacy + accountability_assignment + leadership_cue + organizational_fragmentation + condition + scenario_domain",
        "reporting_model": "reporting_decision ~ bystander_count + ambiguity_level + evaluation_apprehension + private_concern + perceived_responsibility + role_clarity + accountability_assignment + leadership_cue + organizational_fragmentation + condition + scenario_domain",
    }

    ols_formulas = {
        "responsibility_model": "perceived_responsibility ~ bystander_count + ambiguity_level + evaluation_apprehension + role_clarity + accountability_assignment + leadership_cue + social_visibility + organizational_fragmentation + condition + scenario_domain",
        "delay_model": "log_delay ~ bystander_count + ambiguity_level + evaluation_apprehension + perceived_responsibility + role_clarity + intervention_efficacy + organizational_fragmentation + condition + scenario_domain",
        "pluralistic_gap_model": "pluralistic_ignorance_gap ~ bystander_count + ambiguity_level + evaluation_apprehension + leadership_cue + role_clarity + condition + scenario_domain",
        "response_time_model": "log_response_time ~ bystander_count + ambiguity_level + evaluation_apprehension + perceived_responsibility + role_clarity + diffusion_pressure + condition + scenario_domain",
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


def simulate_organizational_fragmentation(outputs: Path, n_orgs: int = 300, periods: int = 36, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    inaction_norm = rng.uniform(0.5, 2.0, n_orgs)
    accountability_clarity = rng.uniform(2, 8, n_orgs)
    leadership_signal = rng.uniform(1, 8, n_orgs)
    fragmentation = rng.uniform(2, 9, n_orgs)
    ambiguity = rng.uniform(2, 8, n_orgs)

    for period in range(1, periods + 1):
        responsibility = np.clip(
            7.0 + 0.45 * accountability_clarity + 0.30 * leadership_signal
            - 0.45 * fragmentation - 0.32 * ambiguity - 0.25 * inaction_norm
            + rng.normal(0, 0.65, n_orgs),
            0, 10
        )

        intervention_rate = logistic(
            -2.8 + 0.55 * responsibility + 0.28 * leadership_signal
            - 0.30 * fragmentation - 0.25 * ambiguity
        )

        inaction_norm = np.clip(
            inaction_norm + 0.22 * fragmentation + 0.18 * ambiguity
            - 0.26 * accountability_clarity - 0.22 * leadership_signal
            + rng.normal(0, 0.35, n_orgs),
            0, 10
        )

        for i in range(n_orgs):
            rows.append({
                "organization_id": f"O{i+1:04d}",
                "period": period,
                "fragmentation": fragmentation[i],
                "ambiguity": ambiguity[i],
                "accountability_clarity": accountability_clarity[i],
                "leadership_signal": leadership_signal[i],
                "perceived_responsibility": responsibility[i],
                "intervention_rate": intervention_rate[i],
                "inaction_norm": inaction_norm[i],
            })

    sim = pd.DataFrame(rows)
    period_summary = (
        sim.groupby("period")
        .agg(
            mean_fragmentation=("fragmentation", "mean"),
            mean_accountability=("accountability_clarity", "mean"),
            mean_responsibility=("perceived_responsibility", "mean"),
            mean_intervention_rate=("intervention_rate", "mean"),
            mean_inaction_norm=("inaction_norm", "mean"),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "organizational_fragmentation_simulation.csv", index=False)
    period_summary.to_csv(outputs / "organizational_fragmentation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/diffusion_responsibility_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=600)
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
        default_input = Path("data/diffusion_responsibility_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_organizational_fragmentation(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
