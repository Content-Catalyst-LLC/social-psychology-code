#!/usr/bin/env python3
"""
Fundamental attribution error research model.

This script can:
1. Generate synthetic attribution data.
2. Estimate dispositional attribution, situational attribution, correspondence,
   blame, punishment, empathy, and response-time models.
3. Compute FAE, constraint-neglect, and correspondence-bias scores.
4. Simulate institutional blame dynamics under varying accountability and constraint salience.
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
    "control", "low_choice", "high_choice", "constraint_salient", "cognitive_load",
    "perspective_taking", "accountability", "organizational_blame", "legal_judgment"
]
ACTOR_ROLES = ["target", "employee", "leader", "student", "defendant", "citizen", "outgroup_member"]
OBSERVER_ROLES = ["participant", "manager", "juror", "teacher", "voter", "peer", "analyst"]
VALENCES = ["positive", "negative", "ambiguous", "norm_violation"]


def generate_dataset(n_participants: int = 500, trials_per_participant: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"constraint": 0.0, "load": 0.0, "perspective": 0.0, "accountability": 0.0, "choice": 0.0},
        "low_choice": {"constraint": 3.0, "load": 0.0, "perspective": -0.2, "accountability": 0.0, "choice": -3.0},
        "high_choice": {"constraint": -2.0, "load": 0.0, "perspective": 0.0, "accountability": 0.0, "choice": 3.0},
        "constraint_salient": {"constraint": 3.0, "load": -0.4, "perspective": 2.4, "accountability": 1.4, "choice": -2.4},
        "cognitive_load": {"constraint": 1.5, "load": 3.2, "perspective": -0.8, "accountability": -0.5, "choice": -0.5},
        "perspective_taking": {"constraint": 2.2, "load": -0.3, "perspective": 3.2, "accountability": 1.0, "choice": -1.2},
        "accountability": {"constraint": 1.4, "load": -0.2, "perspective": 1.6, "accountability": 3.0, "choice": -0.8},
        "organizational_blame": {"constraint": 1.8, "load": 1.0, "perspective": -0.2, "accountability": 0.4, "choice": -0.8},
        "legal_judgment": {"constraint": 1.6, "load": 0.6, "perspective": -0.4, "accountability": 0.2, "choice": -0.7},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        dispositionalism = rng.normal(5.8, 1.2)
        structural_tendency = rng.normal(4.5, 1.2)
        individualism = rng.normal(6.0, 1.3)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            ce = condition_effects[condition]
            actor_role = rng.choice(ACTOR_ROLES)
            observer_role = rng.choice(OBSERVER_ROLES)
            valence = rng.choice(VALENCES, p=[0.18, 0.34, 0.26, 0.22])

            actual_constraint = float(np.clip(rng.normal(5.0 + ce["constraint"], 1.2), 0, 10))
            cognitive_load = float(np.clip(rng.normal(4.2 + ce["load"], 1.0), 0, 10))
            perspective_taking = float(np.clip(rng.normal(4.2 + ce["perspective"] + 0.25 * structural_tendency, 1.0), 0, 10))
            accountability_pressure = float(np.clip(rng.normal(3.8 + ce["accountability"], 1.0), 0, 10))
            evidence_strength = float(np.clip(rng.normal(5.2 + 0.35 * accountability_pressure + 0.18 * perspective_taking, 1.0), 0, 10))
            choice_freedom = float(np.clip(rng.normal(5.0 + ce["choice"] - 0.45 * actual_constraint + 0.20 * cognitive_load, 1.0), 0, 10))

            cultural_individualism = float(np.clip(rng.normal(individualism, 0.9), 0, 10))
            structural_awareness = float(np.clip(rng.normal(structural_tendency + 0.22 * perspective_taking + 0.22 * accountability_pressure, 1.0), 0, 10))

            # Constraint neglect: cognitive load and dispositionalism reduce perceived constraint.
            perceived_constraint = float(np.clip(
                rng.normal(
                    actual_constraint
                    - 0.28 * cognitive_load
                    - 0.18 * dispositionalism
                    + 0.34 * perspective_taking
                    + 0.26 * accountability_pressure
                    + 0.24 * structural_awareness,
                    1.0
                ),
                0, 10
            ))

            negative = 1 if valence in ["negative", "norm_violation"] else 0

            dispositional_attribution = float(np.clip(
                rng.normal(
                    4.8
                    + 0.34 * dispositionalism
                    + 0.32 * choice_freedom
                    + 0.30 * cognitive_load
                    + 0.26 * cultural_individualism
                    + 0.38 * negative
                    - 0.28 * perceived_constraint
                    - 0.22 * perspective_taking
                    - 0.20 * accountability_pressure
                    - 0.18 * evidence_strength,
                    1.0
                ),
                0, 10
            ))

            situational_attribution = float(np.clip(
                rng.normal(
                    3.8
                    + 0.46 * perceived_constraint
                    + 0.30 * actual_constraint
                    + 0.26 * structural_awareness
                    + 0.22 * perspective_taking
                    + 0.22 * accountability_pressure
                    - 0.24 * choice_freedom
                    - 0.18 * cognitive_load,
                    1.0
                ),
                0, 10
            ))

            correspondence_inference = float(np.clip(
                rng.normal(
                    2.5
                    + 0.55 * dispositional_attribution
                    + 0.24 * choice_freedom
                    - 0.28 * situational_attribution
                    - 0.16 * perceived_constraint,
                    1.0
                ),
                0, 10
            ))

            empathy = float(np.clip(
                rng.normal(
                    5.5
                    + 0.30 * situational_attribution
                    + 0.24 * perspective_taking
                    - 0.22 * dispositional_attribution
                    - 0.24 * negative,
                    1.0
                ),
                0, 10
            ))

            moral_blame = float(np.clip(
                rng.normal(
                    1.6
                    + 0.55 * dispositional_attribution
                    + 0.42 * negative
                    - 0.26 * situational_attribution
                    - 0.16 * empathy,
                    1.0
                ),
                0, 10
            ))

            punishment_recommendation = float(np.clip(
                rng.normal(
                    1.5
                    + 0.50 * moral_blame
                    + 0.24 * dispositional_attribution
                    - 0.22 * situational_attribution
                    - 0.12 * empathy,
                    1.0
                ),
                0, 10
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(1050)
                + 0.04 * cognitive_load
                + 0.04 * abs(dispositional_attribution - situational_attribution)
                + 0.03 * evidence_strength
                - 0.04 * choice_freedom
                + rng.normal(0, 0.17)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "trial": trial,
                "actor_role": actor_role,
                "observer_role": observer_role,
                "behavior_valence": valence,
                "dispositional_attribution": round(dispositional_attribution, 3),
                "situational_attribution": round(situational_attribution, 3),
                "perceived_constraint": round(perceived_constraint, 3),
                "actual_constraint": round(actual_constraint, 3),
                "choice_freedom": round(choice_freedom, 3),
                "correspondence_inference": round(correspondence_inference, 3),
                "cognitive_load": round(cognitive_load, 3),
                "perspective_taking": round(perspective_taking, 3),
                "accountability_pressure": round(accountability_pressure, 3),
                "evidence_strength": round(evidence_strength, 3),
                "empathy": round(empathy, 3),
                "moral_blame": round(moral_blame, 3),
                "punishment_recommendation": round(punishment_recommendation, 3),
                "cultural_individualism": round(cultural_individualism, 3),
                "structural_awareness": round(structural_awareness, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["fae_score"] = data["dispositional_attribution"] - data["situational_attribution"]
    data["constraint_neglect"] = data["actual_constraint"] - data["perceived_constraint"]
    data["correspondence_bias_score"] = data["correspondence_inference"] - data["choice_freedom"]
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_scores(df)

    summary = (
        data.groupby(["condition", "behavior_valence"])
        .agg(
            n=("fae_score", "size"),
            participants=("participant", "nunique"),
            mean_dispositional=("dispositional_attribution", "mean"),
            mean_situational=("situational_attribution", "mean"),
            mean_fae_score=("fae_score", "mean"),
            mean_constraint_neglect=("constraint_neglect", "mean"),
            mean_correspondence_bias=("correspondence_bias_score", "mean"),
            mean_blame=("moral_blame", "mean"),
            mean_punishment=("punishment_recommendation", "mean"),
            mean_empathy=("empathy", "mean"),
            mean_accountability=("accountability_pressure", "mean"),
            mean_perspective=("perspective_taking", "mean"),
        )
        .reset_index()
    )

    role_summary = (
        data.groupby(["actor_role", "observer_role"])
        .agg(
            n=("fae_score", "size"),
            mean_fae_score=("fae_score", "mean"),
            mean_constraint_neglect=("constraint_neglect", "mean"),
            mean_blame=("moral_blame", "mean"),
            mean_punishment=("punishment_recommendation", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_valence.csv", index=False)
    role_summary.to_csv(outputs / "summary_by_actor_observer_role.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_scores(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "dispositional_attribution_model": "dispositional_attribution ~ perceived_constraint + choice_freedom + cognitive_load + perspective_taking + accountability_pressure + evidence_strength + cultural_individualism + structural_awareness + condition + behavior_valence + actor_role",
        "situational_attribution_model": "situational_attribution ~ perceived_constraint + actual_constraint + choice_freedom + cognitive_load + perspective_taking + accountability_pressure + evidence_strength + cultural_individualism + structural_awareness + condition + behavior_valence + actor_role",
        "correspondence_model": "correspondence_inference ~ dispositional_attribution + situational_attribution + perceived_constraint + choice_freedom + condition + behavior_valence",
        "fae_score_model": "fae_score ~ cognitive_load - 1 + perspective_taking + accountability_pressure + perceived_constraint + choice_freedom + cultural_individualism + structural_awareness + condition + behavior_valence",
        "blame_model": "moral_blame ~ dispositional_attribution + situational_attribution + empathy + behavior_valence + actor_role + condition",
        "punishment_model": "punishment_recommendation ~ moral_blame + dispositional_attribution + situational_attribution + empathy + accountability_pressure + condition",
        "response_time_model": "log_response_time ~ cognitive_load + evidence_strength + perceived_constraint + choice_freedom + fae_score + condition + behavior_valence",
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


def simulate_institutional_blame(outputs: Path, n_cases: int = 5000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    constraint = rng.uniform(0, 10, n_cases)
    accountability = rng.uniform(0, 10, n_cases)
    perspective = rng.uniform(0, 10, n_cases)
    cognitive_load = rng.uniform(0, 10, n_cases)
    individualism = rng.uniform(0, 10, n_cases)

    perceived_constraint = np.clip(
        constraint - 0.30 * cognitive_load + 0.30 * accountability + 0.25 * perspective,
        0, 10
    )
    disposition = np.clip(
        5.0 + 0.35 * cognitive_load + 0.25 * individualism - 0.30 * perceived_constraint - 0.20 * accountability,
        0, 10
    )
    situation = np.clip(
        3.0 + 0.50 * perceived_constraint + 0.25 * accountability + 0.25 * perspective - 0.20 * cognitive_load,
        0, 10
    )
    blame = np.clip(2.0 + 0.60 * disposition - 0.25 * situation + rng.normal(0, 1.0, n_cases), 0, 10)
    punishment = np.clip(1.5 + 0.55 * blame + 0.20 * disposition - 0.20 * situation + rng.normal(0, 1.0, n_cases), 0, 10)

    sim = pd.DataFrame({
        "case_id": np.arange(1, n_cases + 1),
        "actual_constraint": constraint,
        "perceived_constraint": perceived_constraint,
        "accountability": accountability,
        "perspective_taking": perspective,
        "cognitive_load": cognitive_load,
        "cultural_individualism": individualism,
        "dispositional_attribution": disposition,
        "situational_attribution": situation,
        "fae_score": disposition - situation,
        "moral_blame": blame,
        "punishment_recommendation": punishment,
    })

    summary = (
        sim.assign(
            accountability_band=pd.cut(sim["accountability"], bins=[-0.1, 3, 7, 10.1], labels=["low", "moderate", "high"])
        )
        .groupby("accountability_band", observed=True)
        .agg(
            n=("fae_score", "size"),
            mean_fae_score=("fae_score", "mean"),
            mean_constraint_neglect=("actual_constraint", "mean"),
            mean_blame=("moral_blame", "mean"),
            mean_punishment=("punishment_recommendation", "mean"),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "institutional_blame_simulation.csv", index=False)
    summary.to_csv(outputs / "institutional_blame_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/fundamental_attribution_error_trials.csv"))
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
        default_input = Path("data/fundamental_attribution_error_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_blame(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
