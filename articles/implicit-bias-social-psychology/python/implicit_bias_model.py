#!/usr/bin/env python3
"""
Implicit bias model.

This script can:
1. Generate synthetic IAT-style trial data.
2. Compute participant-level D-scores.
3. Estimate latency, judgment, behavioral-outcome, and intervention models.
4. Simulate cumulative institutional disparity from repeated small decision asymmetries.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "control", "cognitive_load", "time_pressure", "accountability",
    "counter_stereotypical_exposure", "perspective_taking",
    "structured_decision_support", "delayed_followup"
]

CONTEXTS = [
    "laboratory", "education", "employment", "healthcare",
    "criminal_justice", "public_policy", "platform", "organization"
]


def generate_dataset(n_participants: int = 600, trials_per_participant: int = 80, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"load": 3, "acct": 3, "time": 4, "counter": 1, "persp": 1, "struct": 2, "bias": 145},
        "cognitive_load": {"load": 9, "acct": 2, "time": 7, "counter": 1, "persp": 1, "struct": 1, "bias": 205},
        "time_pressure": {"load": 4, "acct": 2, "time": 9, "counter": 1, "persp": 1, "struct": 2, "bias": 220},
        "accountability": {"load": 4, "acct": 9, "time": 4, "counter": 1, "persp": 2, "struct": 5, "bias": 95},
        "counter_stereotypical_exposure": {"load": 3, "acct": 5, "time": 4, "counter": 9, "persp": 3, "struct": 5, "bias": 70},
        "perspective_taking": {"load": 3, "acct": 5, "time": 4, "counter": 4, "persp": 9, "struct": 5, "bias": 82},
        "structured_decision_support": {"load": 4, "acct": 8, "time": 3, "counter": 3, "persp": 3, "struct": 9, "bias": 55},
        "delayed_followup": {"load": 3, "acct": 5, "time": 4, "counter": 5, "persp": 5, "struct": 5, "bias": 115},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 100):03d}"
        site_id = f"S{rng.integers(1, 35):02d}"
        implicit_trait_ms = rng.normal(125, 65)
        explicit_attitude = float(np.clip(rng.normal(5, 30), -100, 100))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context = rng.choice(CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 160):03d}"
            eff = condition_effects[condition]

            congruent = int(rng.random() < 0.5)
            load = float(np.clip(rng.normal(eff["load"], 1), 0, 10))
            accountability = float(np.clip(rng.normal(eff["acct"], 1), 0, 10))
            time_pressure = float(np.clip(rng.normal(eff["time"], 1), 0, 10))
            counter = float(np.clip(rng.normal(eff["counter"], 1), 0, 10))
            perspective = float(np.clip(rng.normal(eff["persp"], 1), 0, 10))
            structured = float(np.clip(rng.normal(eff["struct"], 1), 0, 10))
            followup_days = 0 if condition != "delayed_followup" else int(rng.integers(1, 45))

            base_rt = 650 + rng.normal(0, 90)
            incongruent_penalty = (eff["bias"] + implicit_trait_ms + 12 * load + 10 * time_pressure - 11 * accountability - 10 * counter - 8 * structured)
            rt = base_rt + (0 if congruent else incongruent_penalty) + rng.normal(0, 70)
            rt = int(np.clip(rt, 250, 5000))

            accuracy_prob = 0.96 - 0.015 * load - 0.010 * time_pressure + 0.006 * structured
            accuracy = int(rng.random() < np.clip(accuracy_prob, 0.50, 0.99))

            latent_bias = (incongruent_penalty / 220.0) + 0.025 * time_pressure + 0.020 * load - 0.025 * accountability - 0.030 * structured
            judgment_score = float(np.clip(75 - 8 * latent_bias + 0.10 * explicit_attitude + rng.normal(0, 9), 0, 100))
            behavioral_outcome = float(np.clip(judgment_score - 5 * latent_bias + rng.normal(0, 8), 0, 100))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "condition": condition,
                "trial": t,
                "target_category": "group_a" if rng.random() < 0.5 else "group_b",
                "attribute_category": "positive" if congruent else "negative",
                "congruent_block": congruent,
                "response_time_ms": rt,
                "accuracy": accuracy,
                "explicit_attitude": round(explicit_attitude, 3),
                "judgment_score": round(judgment_score, 3),
                "behavioral_outcome": round(behavioral_outcome, 3),
                "cognitive_load": round(load, 3),
                "accountability": round(accountability, 3),
                "time_pressure": round(time_pressure, 3),
                "counter_stereotypical_exposure": round(counter, 3),
                "perspective_taking": round(perspective, 3),
                "structured_decision_support": round(structured, 3),
                "followup_days": followup_days,
            })

    return pd.DataFrame(rows)


def compute_d_scores(df: pd.DataFrame) -> pd.DataFrame:
    valid = df[(df["response_time_ms"] >= 250) & (df["accuracy"] == 1)].copy()
    grouped = (
        valid.groupby(["participant", "condition", "congruent_block"], observed=True)["response_time_ms"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    wide = grouped.pivot_table(index=["participant", "condition"], columns="congruent_block", values="mean").reset_index()
    wide.columns = ["participant", "condition", "mean_incongruent" if c == 0 else "mean_congruent" if c == 1 else c for c in wide.columns]
    sd = valid.groupby(["participant", "condition"], observed=True)["response_time_ms"].std().reset_index(name="pooled_sd")
    wide = wide.merge(sd, on=["participant", "condition"], how="left")
    wide["d_score"] = (wide["mean_incongruent"] - wide["mean_congruent"]) / wide["pooled_sd"].replace(0, np.nan)
    return wide


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["log_response_time"] = np.log(data["response_time_ms"])
    data["automaticity_risk_index"] = (
        data["cognitive_load"]
        + data["time_pressure"]
        - data["accountability"]
        - data["structured_decision_support"]
    ) / 4.0
    data["mitigation_index"] = (
        data["accountability"]
        + data["counter_stereotypical_exposure"]
        + data["perspective_taking"]
        + data["structured_decision_support"]
    ) / 4.0
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)
    d_scores = compute_d_scores(data)

    summary = (
        data.groupby(["condition", "institution_context"], observed=True)
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_rt=("response_time_ms", "mean"),
            accuracy_rate=("accuracy", "mean"),
            mean_explicit_attitude=("explicit_attitude", "mean"),
            mean_judgment=("judgment_score", "mean"),
            mean_behavioral_outcome=("behavioral_outcome", "mean"),
            mean_automaticity_risk=("automaticity_risk_index", "mean"),
            mean_mitigation=("mitigation_index", "mean"),
        )
        .reset_index()
    )

    d_summary = (
        d_scores.groupby("condition", observed=True)
        .agg(
            n=("participant", "count"),
            mean_d_score=("d_score", "mean"),
            sd_d_score=("d_score", "std"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    d_scores.to_csv(outputs / "participant_d_scores.csv", index=False)
    d_summary.to_csv(outputs / "d_score_summary_by_condition.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    valid = data[(data["response_time_ms"] >= 250) & (data["accuracy"] == 1)].copy()

    formulas = {
        "latency_model": (
            "log_response_time ~ congruent_block + explicit_attitude + cognitive_load "
            "+ accountability + time_pressure + counter_stereotypical_exposure "
            "+ perspective_taking + structured_decision_support + condition + institution_context"
        ),
        "judgment_model": (
            "judgment_score ~ congruent_block + explicit_attitude + automaticity_risk_index "
            "+ mitigation_index + condition + institution_context"
        ),
        "behavioral_outcome_model": (
            "behavioral_outcome ~ congruent_block + explicit_attitude + judgment_score "
            "+ automaticity_risk_index + mitigation_index + condition + institution_context"
        ),
        "accuracy_model": (
            "accuracy ~ congruent_block + cognitive_load + time_pressure "
            "+ accountability + structured_decision_support + condition + institution_context"
        ),
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name == "accuracy_model":
            model = smf.glm(formula, data=data, family=sm.families.Binomial()).fit(
                cov_type="cluster", cov_kwds={"groups": data["participant"]}
            )
        elif name == "latency_model":
            model = smf.ols(formula, data=valid).fit(
                cov_type="cluster", cov_kwds={"groups": valid["participant"]}
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


def simulate_institutional_disparity(outputs: Path, decisions: int = 10000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []
    scenarios = ["unstructured_discretion", "time_pressure", "accountability", "structured_decision_support", "combined_mitigation"]

    for scenario in scenarios:
        cumulative = 0.0
        for decision in range(1, decisions + 1):
            if scenario == "unstructured_discretion":
                bias = rng.normal(0.018, 0.060)
            elif scenario == "time_pressure":
                bias = rng.normal(0.032, 0.070)
            elif scenario == "accountability":
                bias = rng.normal(0.010, 0.050)
            elif scenario == "structured_decision_support":
                bias = rng.normal(0.004, 0.040)
            else:
                bias = rng.normal(0.002, 0.035)

            cumulative += bias
            if decision % 100 == 0:
                rows.append({
                    "scenario": scenario,
                    "decision": decision,
                    "mean_bias_contribution": bias,
                    "cumulative_disparity": cumulative,
                })

    pd.DataFrame(rows).to_csv(outputs / "institutional_disparity_simulation.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/implicit_bias_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=600)
    parser.add_argument("--trials", type=int, default=80)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulate:
        df = generate_dataset(args.participants, args.trials, args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote simulated dataset: {args.output}")
    elif args.input:
        df = pd.read_csv(args.input)
    else:
        default_input = Path("data/implicit_bias_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_disparity(args.outputs, seed=args.seed)
    print(f"Wrote outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
