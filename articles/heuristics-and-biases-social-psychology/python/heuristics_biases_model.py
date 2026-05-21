#!/usr/bin/env python3
"""
Heuristics and biases model.

This script can:
1. Generate synthetic judgment-under-uncertainty data.
2. Estimate anchoring, calibration, availability, representativeness, framing, affect, and debiasing models.
3. Simulate institutional bias accumulation and debiasing dynamics.
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


HEURISTICS = [
    "anchoring", "availability", "representativeness", "affect",
    "framing", "confirmation", "overconfidence", "base_rate", "mixed"
]

CONDITIONS = [
    "control", "low_anchor", "high_anchor", "base_rate_prompt", "vivid_case",
    "neutral_case", "gain_frame", "loss_frame", "accountability",
    "calibration_feedback", "consider_opposite", "structured_decision"
]

CONTEXTS = ["laboratory", "medicine", "law", "finance", "public_policy", "organization", "platform", "education"]
DOMAINS = ["risk", "health", "legal", "financial", "social", "political", "organizational", "consumer", "environmental"]


def generate_dataset(n_participants: int = 800, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    profiles: Dict[str, Dict[str, float]] = {
        "control": {"anchor_shift": 0, "salience": 4, "affect": 0, "debias": 1, "account": 3, "feedback": 4, "confirm": 4, "disconfirm": 4, "confidence": 65},
        "low_anchor": {"anchor_shift": -40, "salience": 4, "affect": 0, "debias": 1, "account": 3, "feedback": 4, "confirm": 5, "disconfirm": 4, "confidence": 70},
        "high_anchor": {"anchor_shift": 40, "salience": 4, "affect": 0, "debias": 1, "account": 3, "feedback": 4, "confirm": 5, "disconfirm": 4, "confidence": 75},
        "base_rate_prompt": {"anchor_shift": 0, "salience": 5, "affect": 0, "debias": 8, "account": 7, "feedback": 6, "confirm": 5, "disconfirm": 6, "confidence": 70},
        "vivid_case": {"anchor_shift": 0, "salience": 9, "affect": -6, "debias": 1, "account": 4, "feedback": 4, "confirm": 6, "disconfirm": 3, "confidence": 78},
        "neutral_case": {"anchor_shift": 0, "salience": 3, "affect": 0, "debias": 2, "account": 5, "feedback": 5, "confirm": 4, "disconfirm": 5, "confidence": 62},
        "gain_frame": {"anchor_shift": 0, "salience": 5, "affect": 2, "debias": 3, "account": 5, "feedback": 5, "confirm": 4, "disconfirm": 5, "confidence": 68},
        "loss_frame": {"anchor_shift": 0, "salience": 7, "affect": -8, "debias": 1, "account": 3, "feedback": 4, "confirm": 7, "disconfirm": 3, "confidence": 82},
        "accountability": {"anchor_shift": 0, "salience": 5, "affect": 0, "debias": 6, "account": 9, "feedback": 6, "confirm": 3, "disconfirm": 7, "confidence": 66},
        "calibration_feedback": {"anchor_shift": 0, "salience": 4, "affect": 0, "debias": 7, "account": 6, "feedback": 9, "confirm": 3, "disconfirm": 7, "confidence": 58},
        "consider_opposite": {"anchor_shift": 0, "salience": 5, "affect": 0, "debias": 8, "account": 8, "feedback": 8, "confirm": 3, "disconfirm": 8, "confidence": 60},
        "structured_decision": {"anchor_shift": 0, "salience": 4, "affect": 0, "debias": 9, "account": 9, "feedback": 8, "confirm": 3, "disconfirm": 8, "confidence": 62},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 160):03d}"
        site_id = f"S{rng.integers(1, 55):02d}"
        cognitive_style = rng.normal(0, 1)

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            heuristic = rng.choice(HEURISTICS)
            context = rng.choice(CONTEXTS)
            domain = rng.choice(DOMAINS)
            scenario_id = f"SC{rng.integers(1, 220):03d}"
            profile = profiles[condition]

            true_value = float(np.clip(rng.normal(50, 18), -1000, 1000))
            anchor_value = float(np.clip(true_value + profile["anchor_shift"] + rng.normal(0, 12), -1000, 1000))
            base_rate = float(np.clip(rng.beta(2.2, 4.5), 0, 1))
            individuating = float(np.clip(rng.normal(6 if heuristic == "representativeness" else 4.5, 1.5), 0, 10))
            representativeness = float(np.clip(rng.normal(7 if heuristic == "representativeness" else 5, 1.5), 0, 10))
            availability = float(np.clip(rng.normal(profile["salience"], 1.2), 0, 10))
            affect = float(np.clip(rng.normal(profile["affect"], 2.0), -10, 10))
            debias = float(np.clip(rng.normal(profile["debias"], 1.0), 0, 10))
            accountability = float(np.clip(rng.normal(profile["account"], 1.0), 0, 10))
            feedback = float(np.clip(rng.normal(profile["feedback"], 1.0), 0, 10))
            confirmation = float(np.clip(rng.normal(profile["confirm"], 1.0), 0, 10))
            disconfirming = float(np.clip(rng.normal(profile["disconfirm"], 1.0), 0, 10))

            anchor_weight = 0.35 + 0.03 * (10 - debias) - 0.02 * accountability
            representativeness_bias = 1.8 * representativeness - 12.0 * base_rate + 0.8 * individuating
            availability_bias = 2.8 * availability if heuristic in {"availability", "mixed"} else 0.8 * availability
            affect_bias = -2.5 * affect if heuristic in {"affect", "framing", "mixed"} else -0.8 * affect
            confirmation_bias = 1.4 * confirmation - 1.6 * disconfirming

            estimate = (
                (1 - anchor_weight) * true_value
                + anchor_weight * anchor_value
                + 0.35 * representativeness_bias
                + 0.20 * availability_bias
                + 0.25 * affect_bias
                + 0.25 * confirmation_bias
                - 1.2 * debias
                - 0.8 * accountability
                + rng.normal(0, 8)
            )
            estimate = float(np.clip(estimate, -1000, 1000))

            frame_type = "gain" if condition == "gain_frame" else "loss" if condition == "loss_frame" else "neutral"

            perceived_risk = float(np.clip(
                50
                + 3.2 * availability
                - 3.0 * affect
                + 1.2 * confirmation
                - 1.4 * debias
                + rng.normal(0, 10),
                0, 100
            ))
            perceived_benefit = float(np.clip(
                50
                + 3.0 * affect
                - 1.8 * perceived_risk / 10
                + 0.8 * debias
                + rng.normal(0, 10),
                0, 100
            ))

            choice_latent = (
                -0.4
                + 0.04 * perceived_benefit
                - 0.03 * perceived_risk
                + (0.4 if frame_type == "gain" else -0.4 if frame_type == "loss" else 0)
                + rng.normal(0, 0.4)
            )
            choice_prob = 1 / (1 + np.exp(-choice_latent))
            choice_binary = int(rng.random() < choice_prob)

            actual_accuracy = float(np.clip(100 - abs(estimate - true_value) + rng.normal(0, 4), 0, 100))
            confidence = float(np.clip(
                rng.normal(profile["confidence"], 8)
                + 1.5 * confirmation
                - 1.5 * feedback
                - 1.2 * debias
                + 0.8 * cognitive_style,
                0, 100
            ))
            overconfidence = float(np.clip(confidence - actual_accuracy, -100, 100))

            decision_quality = float(np.clip(
                actual_accuracy
                - 0.35 * abs(overconfidence)
                + 1.8 * debias
                + 1.5 * accountability
                + 1.4 * feedback
                - 1.2 * confirmation
                + rng.normal(0, 5),
                0, 100
            ))

            response_time = int(np.clip(np.exp(
                math.log(800)
                + 0.030 * (10 - debias)
                + 0.020 * availability
                + 0.015 * abs(anchor_value - true_value) / 10
                - 0.020 * accountability
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "judgment_domain": domain,
                "heuristic_type": heuristic,
                "condition": condition,
                "trial": t,
                "anchor_value": round(anchor_value, 3),
                "true_value": round(true_value, 3),
                "estimate": round(estimate, 3),
                "base_rate": round(base_rate, 4),
                "individuating_information_strength": round(individuating, 3),
                "representativeness_rating": round(representativeness, 3),
                "availability_salience": round(availability, 3),
                "affect_valence": round(affect, 3),
                "perceived_risk": round(perceived_risk, 3),
                "perceived_benefit": round(perceived_benefit, 3),
                "frame_type": frame_type,
                "choice_binary": choice_binary,
                "confidence_rating": round(confidence, 3),
                "actual_accuracy": round(actual_accuracy, 3),
                "confirmation_tendency": round(confirmation, 3),
                "disconfirming_evidence_exposure": round(disconfirming, 3),
                "overconfidence_score": round(overconfidence, 3),
                "response_time_ms": response_time,
                "debiasing_intervention_strength": round(debias, 3),
                "institutional_accountability": round(accountability, 3),
                "feedback_quality": round(feedback, 3),
                "decision_quality": round(decision_quality, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["anchoring_error"] = data["estimate"] - data["true_value"]
    data["absolute_error"] = np.abs(data["anchoring_error"])
    data["calibration_error"] = np.abs(data["confidence_rating"] - data["actual_accuracy"])
    data["log_response_time"] = np.log(data["response_time_ms"])
    data["bias_pressure_index"] = (
        data["availability_salience"]
        + data["representativeness_rating"]
        + data["confirmation_tendency"]
        + np.abs(data["affect_valence"])
        - data["debiasing_intervention_strength"]
        - data["institutional_accountability"]
        - data["feedback_quality"]
    ) / 4.0
    data["evidence_discipline_index"] = (
        data["debiasing_intervention_strength"]
        + data["institutional_accountability"]
        + data["feedback_quality"]
        + data["disconfirming_evidence_exposure"]
    ) / 4.0
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["heuristic_type", "condition"], observed=True)
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_estimate=("estimate", "mean"),
            mean_true_value=("true_value", "mean"),
            mean_anchoring_error=("anchoring_error", "mean"),
            mean_absolute_error=("absolute_error", "mean"),
            mean_calibration_error=("calibration_error", "mean"),
            mean_overconfidence=("overconfidence_score", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
            mean_bias_pressure=("bias_pressure_index", "mean"),
            mean_evidence_discipline=("evidence_discipline_index", "mean"),
        )
        .reset_index()
    )

    context_summary = (
        data.groupby(["institution_context", "judgment_domain"], observed=True)
        .agg(
            n=("participant", "size"),
            mean_absolute_error=("absolute_error", "mean"),
            mean_calibration_error=("calibration_error", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_heuristic_condition.csv", index=False)
    context_summary.to_csv(outputs / "summary_by_context_domain.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "anchoring_model": (
            "anchoring_error ~ anchor_value + true_value + heuristic_type + condition "
            "+ debiasing_intervention_strength + institutional_accountability"
        ),
        "calibration_model": (
            "calibration_error ~ confidence_rating + actual_accuracy + heuristic_type + condition "
            "+ feedback_quality + debiasing_intervention_strength"
        ),
        "risk_model": (
            "perceived_risk ~ availability_salience + affect_valence + representativeness_rating "
            "+ confirmation_tendency + debiasing_intervention_strength + condition + judgment_domain"
        ),
        "decision_quality_model": (
            "decision_quality ~ absolute_error + calibration_error + debiasing_intervention_strength "
            "+ institutional_accountability + feedback_quality + disconfirming_evidence_exposure "
            "+ condition + institution_context"
        ),
        "choice_model": (
            "choice_binary ~ perceived_risk + perceived_benefit + frame_type + affect_valence "
            "+ condition + judgment_domain"
        ),
        "response_time_model": (
            "log_response_time ~ availability_salience + absolute_error + debiasing_intervention_strength "
            "+ institutional_accountability + condition"
        ),
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


def simulate_institutional_bias(outputs: Path, steps: int = 80, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    scenarios = [
        "unstructured_judgment",
        "high_accountability",
        "calibration_feedback",
        "base_rate_prompting",
        "structured_decision_protocol",
    ]

    for scenario in scenarios:
        accumulated_error = 0.0
        calibration_error = 0.25

        for step in range(1, steps + 1):
            if scenario == "unstructured_judgment":
                bias_pressure, discipline = 0.85, 0.15
            elif scenario == "high_accountability":
                bias_pressure, discipline = 0.55, 0.65
            elif scenario == "calibration_feedback":
                bias_pressure, discipline = 0.50, 0.75
            elif scenario == "base_rate_prompting":
                bias_pressure, discipline = 0.45, 0.80
            else:
                bias_pressure, discipline = 0.35, 0.90

            decision_error = rng.normal(0.02 + 0.10 * bias_pressure - 0.08 * discipline, 0.05)
            accumulated_error += decision_error
            calibration_error = np.clip(calibration_error + 0.04 * bias_pressure - 0.05 * discipline + rng.normal(0, 0.01), 0, 1)
            decision_quality = np.clip(1 - abs(decision_error) - calibration_error / 2 + 0.25 * discipline, 0, 1)

            rows.append({
                "scenario": scenario,
                "step": step,
                "decision_error": decision_error,
                "accumulated_error": accumulated_error,
                "calibration_error": calibration_error,
                "decision_quality": decision_quality,
                "bias_pressure": bias_pressure,
                "evidence_discipline": discipline,
            })

    pd.DataFrame(rows).to_csv(outputs / "institutional_bias_simulation.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/heuristics_biases_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=800)
    parser.add_argument("--trials", type=int, default=6)
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
        default_input = Path("data/heuristics_biases_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_bias(args.outputs, seed=args.seed)
    print(f"Wrote outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
