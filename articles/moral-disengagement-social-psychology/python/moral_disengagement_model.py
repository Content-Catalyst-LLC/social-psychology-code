#!/usr/bin/env python3
"""
Moral disengagement research model.

This script can:
1. Generate synthetic moral-disengagement data.
2. Estimate harmful-decision, policy-endorsement, unethical-intention,
   empathy, guilt, agency, and response-time models.
3. Compute global and mechanism-specific disengagement indices.
4. Simulate institutional normalization of harmful practice over time.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

try:
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "control", "moral_justification", "euphemistic_labeling",
    "advantageous_comparison", "authority_pressure", "diffusion",
    "low_harm_visibility", "dehumanization", "victim_blame", "accountability"
]
DOMAINS = ["organization", "politics", "war", "environment", "technology", "school", "healthcare", "public_policy"]

MECHANISMS: List[str] = [
    "moral_justification", "euphemistic_labeling", "advantageous_comparison",
    "displaced_responsibility", "diffused_responsibility", "consequence_distortion",
    "dehumanization", "blame_attribution"
]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 600, trials_per_participant: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"mj": 0, "el": 0, "ac": 0, "dr": 0, "df": 0, "cd": 0, "dh": 0, "vb": 0, "account": 0, "visible": 0},
        "moral_justification": {"mj": 3.2, "el": 0.4, "ac": 0.6, "dr": 0.3, "df": 0.3, "cd": 0.4, "dh": 0.2, "vb": 0.2, "account": -0.4, "visible": -0.3},
        "euphemistic_labeling": {"mj": 0.4, "el": 3.2, "ac": 0.4, "dr": 0.4, "df": 0.5, "cd": 1.0, "dh": 0.2, "vb": 0.1, "account": -0.4, "visible": -0.6},
        "advantageous_comparison": {"mj": 0.8, "el": 0.6, "ac": 3.0, "dr": 0.3, "df": 0.3, "cd": 0.5, "dh": 0.3, "vb": 0.2, "account": -0.2, "visible": -0.2},
        "authority_pressure": {"mj": 0.8, "el": 0.8, "ac": 0.8, "dr": 3.2, "df": 1.4, "cd": 0.8, "dh": 0.8, "vb": 0.5, "account": -0.6, "visible": -0.5},
        "diffusion": {"mj": 0.5, "el": 0.8, "ac": 0.5, "dr": 1.2, "df": 3.4, "cd": 1.0, "dh": 0.4, "vb": 0.4, "account": -0.5, "visible": -0.6},
        "low_harm_visibility": {"mj": 0.6, "el": 1.2, "ac": 0.7, "dr": 0.7, "df": 1.2, "cd": 3.4, "dh": 0.4, "vb": 0.3, "account": -0.8, "visible": -3.0},
        "dehumanization": {"mj": 0.8, "el": 0.7, "ac": 0.8, "dr": 0.8, "df": 0.8, "cd": 1.0, "dh": 3.4, "vb": 1.6, "account": -0.5, "visible": -0.8},
        "victim_blame": {"mj": 0.8, "el": 0.6, "ac": 0.7, "dr": 0.5, "df": 0.6, "cd": 0.8, "dh": 1.5, "vb": 3.4, "account": -0.4, "visible": -0.4},
        "accountability": {"mj": -1.2, "el": -1.1, "ac": -1.0, "dr": -1.1, "df": -1.1, "cd": -1.2, "dh": -1.0, "vb": -1.0, "account": 3.4, "visible": 2.0},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        trait_disengagement = rng.normal(4.2, 1.3)
        moral_identity = rng.normal(6.2, 1.1)
        empathy_trait = rng.normal(6.0, 1.2)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            ce = condition_effects[condition]
            domain = rng.choice(DOMAINS)

            institutional_pressure = float(np.clip(rng.normal(4.5 + 0.9 * (domain in ["organization", "technology", "public_policy"]) - 0.2 * ce["account"], 1.0), 0, 10))
            authority_pressure = float(np.clip(rng.normal(3.8 + ce["dr"] * 0.55 + 1.1 * (domain in ["war", "organization", "healthcare"]), 1.0), 0, 10))
            group_norm_strength = float(np.clip(rng.normal(4.0 + 0.35 * institutional_pressure + 0.25 * authority_pressure, 1.0), 0, 10))
            victim_distance = float(np.clip(rng.normal(4.2 - ce["visible"] + 0.9 * (domain in ["environment", "technology", "war"]), 1.0), 0, 10))
            harm_visibility = float(np.clip(rng.normal(5.5 + ce["visible"] - 0.35 * victim_distance, 1.0), 0, 10))
            responsibility_clarity = float(np.clip(rng.normal(5.2 + ce["account"] - 0.25 * institutional_pressure - 0.22 * group_norm_strength, 1.0), 0, 10))

            moral_justification = float(np.clip(rng.normal(trait_disengagement + ce["mj"] + 0.22 * group_norm_strength, 1.0), 0, 10))
            euphemistic_labeling = float(np.clip(rng.normal(trait_disengagement + ce["el"] + 0.20 * institutional_pressure, 1.0), 0, 10))
            advantageous_comparison = float(np.clip(rng.normal(trait_disengagement + ce["ac"], 1.0), 0, 10))
            displaced_responsibility = float(np.clip(rng.normal(trait_disengagement + ce["dr"] + 0.35 * authority_pressure, 1.0), 0, 10))
            diffused_responsibility = float(np.clip(rng.normal(trait_disengagement + ce["df"] + 0.35 * group_norm_strength, 1.0), 0, 10))
            consequence_distortion = float(np.clip(rng.normal(trait_disengagement + ce["cd"] + 0.35 * victim_distance - 0.28 * harm_visibility, 1.0), 0, 10))
            dehumanization = float(np.clip(rng.normal(trait_disengagement + ce["dh"] + 0.22 * victim_distance, 1.0), 0, 10))
            blame_attribution = float(np.clip(rng.normal(trait_disengagement + ce["vb"] + 0.28 * dehumanization, 1.0), 0, 10))

            md_index = np.mean([
                moral_justification, euphemistic_labeling, advantageous_comparison,
                displaced_responsibility, diffused_responsibility, consequence_distortion,
                dehumanization, blame_attribution
            ])

            perceived_agency = float(np.clip(rng.normal(
                6.5
                - 0.30 * displaced_responsibility
                - 0.25 * diffused_responsibility
                - 0.25 * authority_pressure
                + 0.30 * responsibility_clarity,
                1.0
            ), 0, 10))

            empathy = float(np.clip(rng.normal(
                empathy_trait
                - 0.35 * dehumanization
                - 0.20 * blame_attribution
                + 0.25 * harm_visibility
                - 0.10 * victim_distance,
                1.0
            ), 0, 10))

            guilt = float(np.clip(rng.normal(
                moral_identity
                - 0.45 * md_index
                + 0.35 * harm_visibility
                + 0.25 * perceived_agency
                + 0.25 * responsibility_clarity
                + 0.18 * empathy,
                1.0
            ), 0, 10))

            harmful_probability = logistic(
                -4.0
                + 0.42 * md_index
                + 0.18 * institutional_pressure
                + 0.16 * authority_pressure
                + 0.18 * group_norm_strength
                - 0.24 * empathy
                - 0.20 * guilt
                - 0.18 * harm_visibility
                - 0.18 * responsibility_clarity
            )
            harmful_decision = int(rng.random() < harmful_probability)

            policy_endorsement = float(np.clip(rng.normal(
                2.0
                + 0.55 * md_index
                + 0.22 * institutional_pressure
                + 0.20 * group_norm_strength
                - 0.25 * empathy
                - 0.22 * guilt,
                1.0
            ), 0, 10))

            unethical_intention = float(np.clip(rng.normal(
                1.8
                + 0.50 * md_index
                + 0.24 * institutional_pressure
                + 0.18 * authority_pressure
                - 0.25 * guilt
                - 0.20 * responsibility_clarity,
                1.0
            ), 0, 10))

            response_time_ms = int(np.clip(np.exp(
                math.log(1100)
                + 0.04 * moral_identity
                + 0.04 * responsibility_clarity
                - 0.035 * md_index
                + rng.normal(0, 0.18)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "trial": trial,
                "scenario_domain": domain,
                "moral_justification": round(moral_justification, 3),
                "euphemistic_labeling": round(euphemistic_labeling, 3),
                "advantageous_comparison": round(advantageous_comparison, 3),
                "displaced_responsibility": round(displaced_responsibility, 3),
                "diffused_responsibility": round(diffused_responsibility, 3),
                "consequence_distortion": round(consequence_distortion, 3),
                "dehumanization": round(dehumanization, 3),
                "blame_attribution": round(blame_attribution, 3),
                "harm_visibility": round(harm_visibility, 3),
                "perceived_agency": round(perceived_agency, 3),
                "responsibility_clarity": round(responsibility_clarity, 3),
                "institutional_pressure": round(institutional_pressure, 3),
                "authority_pressure": round(authority_pressure, 3),
                "group_norm_strength": round(group_norm_strength, 3),
                "victim_distance": round(victim_distance, 3),
                "empathy": round(empathy, 3),
                "guilt": round(guilt, 3),
                "harmful_decision": harmful_decision,
                "policy_endorsement": round(policy_endorsement, 3),
                "unethical_intention": round(unethical_intention, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["md_index"] = data[MECHANISMS].mean(axis=1)
    data["agency_reduction_index"] = (data["displaced_responsibility"] + data["diffused_responsibility"]) / 2
    data["harm_obscuration_index"] = (data["consequence_distortion"] + data["victim_distance"] - data["harm_visibility"]) / 3
    data["target_denigration_index"] = (data["dehumanization"] + data["blame_attribution"]) / 2
    data["self_sanction_index"] = data["guilt"] + data["empathy"] + data["responsibility_clarity"]
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "scenario_domain"])
        .agg(
            n=("md_index", "size"),
            participants=("participant", "nunique"),
            mean_md_index=("md_index", "mean"),
            harmful_rate=("harmful_decision", "mean"),
            mean_policy_endorsement=("policy_endorsement", "mean"),
            mean_unethical_intention=("unethical_intention", "mean"),
            mean_empathy=("empathy", "mean"),
            mean_guilt=("guilt", "mean"),
            mean_harm_visibility=("harm_visibility", "mean"),
            mean_responsibility_clarity=("responsibility_clarity", "mean"),
            mean_institutional_pressure=("institutional_pressure", "mean"),
            mean_authority_pressure=("authority_pressure", "mean"),
        )
        .reset_index()
    )

    mechanism_summary = (
        data.groupby("condition")[MECHANISMS + [
            "md_index", "empathy", "guilt", "harmful_decision",
            "policy_endorsement", "unethical_intention"
        ]]
        .mean()
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_domain.csv", index=False)
    mechanism_summary.to_csv(outputs / "mechanism_summary_by_condition.csv", index=False)


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
        "harmful_decision_model": "harmful_decision ~ md_index + empathy + guilt + harm_visibility + responsibility_clarity + institutional_pressure + authority_pressure + group_norm_strength + condition + scenario_domain",
    }

    ols_formulas = {
        "policy_endorsement_model": "policy_endorsement ~ md_index + empathy + guilt + harm_visibility + responsibility_clarity + institutional_pressure + authority_pressure + group_norm_strength + condition + scenario_domain",
        "unethical_intention_model": "unethical_intention ~ md_index + empathy + guilt + perceived_agency + responsibility_clarity + institutional_pressure + authority_pressure + condition + scenario_domain",
        "empathy_model": "empathy ~ dehumanization + blame_attribution + harm_visibility + victim_distance + condition + scenario_domain",
        "guilt_model": "guilt ~ md_index + empathy + harm_visibility + perceived_agency + responsibility_clarity + condition + scenario_domain",
        "agency_model": "perceived_agency ~ displaced_responsibility + diffused_responsibility + authority_pressure + responsibility_clarity + institutional_pressure + condition",
        "response_time_model": "log_response_time ~ md_index + guilt + responsibility_clarity + harmful_decision + condition + scenario_domain",
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


def simulate_institutional_normalization(outputs: Path, n_institutions: int = 250, periods: int = 40, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    normalized_harm = rng.uniform(0.5, 2.0, n_institutions)
    accountability = rng.uniform(2, 8, n_institutions)
    dissent_protection = rng.uniform(2, 8, n_institutions)
    reward_for_harm = rng.uniform(1, 8, n_institutions)

    for t in range(1, periods + 1):
        md = np.clip(
            2.5
            + 0.35 * normalized_harm
            + 0.35 * reward_for_harm
            - 0.25 * accountability
            - 0.25 * dissent_protection
            + rng.normal(0, 0.8, n_institutions),
            0,
            10
        )

        harmful_rate = logistic(-3.0 + 0.55 * md + 0.25 * reward_for_harm - 0.28 * accountability)
        normalized_harm = np.clip(
            normalized_harm
            + 0.18 * md
            + 0.22 * reward_for_harm
            - 0.25 * accountability
            - 0.20 * dissent_protection
            + rng.normal(0, 0.45, n_institutions),
            0,
            10
        )

        for i in range(n_institutions):
            rows.append({
                "institution_id": f"I{i+1:04d}",
                "period": t,
                "moral_disengagement": md[i],
                "harmful_rate": harmful_rate[i],
                "normalized_harm": normalized_harm[i],
                "accountability": accountability[i],
                "dissent_protection": dissent_protection[i],
                "reward_for_harm": reward_for_harm[i],
            })

    sim = pd.DataFrame(rows)
    summary = (
        sim.groupby("period")
        .agg(
            mean_md=("moral_disengagement", "mean"),
            mean_harmful_rate=("harmful_rate", "mean"),
            mean_normalized_harm=("normalized_harm", "mean"),
            mean_accountability=("accountability", "mean"),
            mean_dissent_protection=("dissent_protection", "mean"),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "institutional_normalization_simulation.csv", index=False)
    summary.to_csv(outputs / "institutional_normalization_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/moral_disengagement_trials.csv"))
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
        default_input = Path("data/moral_disengagement_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_normalization(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
