#!/usr/bin/env python3
"""
Cognitive dissonance model.

This script can:
1. Generate synthetic dissonance study data.
2. Estimate attitude-change, spreading-of-alternatives, effort-justification, belief-disconfirmation, and institutional-escalation models.
3. Simulate institutional rationalization and policy reversal dynamics.
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


PARADIGMS = [
    "forced_compliance",
    "free_choice",
    "effort_justification",
    "belief_disconfirmation",
    "self_affirmation",
    "action_based",
    "institutional_escalation",
]

CONDITIONS = [
    "control", "low_choice", "high_choice", "low_reward", "high_reward",
    "mild_effort", "severe_effort", "affirmation", "no_affirmation",
    "public_commitment", "private_commitment", "strong_disconfirmation",
    "weak_disconfirmation",
]

CONTEXTS = [
    "laboratory", "politics", "organization", "consumer",
    "religion", "education", "public_policy", "platform"
]


def generate_dataset(n_participants: int = 700, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_profile: Dict[str, Dict[str, float]] = {
        "control": {"choice": 2, "responsibility": 2, "identity": 2, "affirm": 0, "just": 6, "public": 1, "effort": 0, "disc": 0, "commit": 2, "inst": 0, "sunk": 0, "evidence": 0, "acct": 3},
        "low_choice": {"choice": 2, "responsibility": 3, "identity": 4, "affirm": 0, "just": 2, "public": 4, "effort": 0, "disc": 0, "commit": 4, "inst": 0, "sunk": 0, "evidence": 0, "acct": 4},
        "high_choice": {"choice": 9, "responsibility": 8, "identity": 7, "affirm": 0, "just": 1, "public": 7, "effort": 0, "disc": 0, "commit": 7, "inst": 0, "sunk": 0, "evidence": 0, "acct": 4},
        "low_reward": {"choice": 8, "responsibility": 7, "identity": 7, "affirm": 0, "just": 1, "public": 6, "effort": 0, "disc": 0, "commit": 7, "inst": 0, "sunk": 0, "evidence": 0, "acct": 4},
        "high_reward": {"choice": 8, "responsibility": 7, "identity": 6, "affirm": 0, "just": 9, "public": 6, "effort": 0, "disc": 0, "commit": 6, "inst": 0, "sunk": 0, "evidence": 0, "acct": 4},
        "mild_effort": {"choice": 6, "responsibility": 6, "identity": 3, "affirm": 0, "just": 2, "public": 5, "effort": 2, "disc": 0, "commit": 4, "inst": 2, "sunk": 3, "evidence": 3, "acct": 5},
        "severe_effort": {"choice": 8, "responsibility": 8, "identity": 7, "affirm": 0, "just": 2, "public": 8, "effort": 9, "disc": 0, "commit": 8, "inst": 4, "sunk": 6, "evidence": 3, "acct": 4},
        "affirmation": {"choice": 7, "responsibility": 7, "identity": 5, "affirm": 9, "just": 2, "public": 5, "effort": 5, "disc": 8, "commit": 8, "inst": 4, "sunk": 6, "evidence": 8, "acct": 6},
        "no_affirmation": {"choice": 7, "responsibility": 7, "identity": 8, "affirm": 0, "just": 2, "public": 6, "effort": 5, "disc": 8, "commit": 8, "inst": 5, "sunk": 6, "evidence": 8, "acct": 4},
        "public_commitment": {"choice": 8, "responsibility": 8, "identity": 8, "affirm": 0, "just": 2, "public": 10, "effort": 8, "disc": 8, "commit": 9, "inst": 9, "sunk": 9, "evidence": 8, "acct": 3},
        "private_commitment": {"choice": 5, "responsibility": 5, "identity": 4, "affirm": 0, "just": 2, "public": 3, "effort": 6, "disc": 8, "commit": 6, "inst": 4, "sunk": 7, "evidence": 8, "acct": 8},
        "strong_disconfirmation": {"choice": 7, "responsibility": 8, "identity": 9, "affirm": 0, "just": 2, "public": 9, "effort": 6, "disc": 9, "commit": 9, "inst": 6, "sunk": 8, "evidence": 9, "acct": 3},
        "weak_disconfirmation": {"choice": 6, "responsibility": 6, "identity": 5, "affirm": 0, "just": 2, "public": 5, "effort": 4, "disc": 4, "commit": 6, "inst": 3, "sunk": 5, "evidence": 4, "acct": 5},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 120):03d}"
        site_id = f"S{rng.integers(1, 40):02d}"
        consistency_need = rng.normal(0, 1)

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            paradigm = rng.choice(PARADIGMS)
            context = rng.choice(CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 180):03d}"
            profile = condition_profile[condition]

            pre_attitude = float(np.clip(rng.normal(25 if paradigm != "belief_disconfirmation" else 70, 25), -100, 100))
            counter = float(np.clip(rng.normal(8 if paradigm == "forced_compliance" else 1, 1.2), 0, 10))
            perceived_choice = float(np.clip(rng.normal(profile["choice"], 1), 0, 10))
            responsibility = float(np.clip(rng.normal(profile["responsibility"], 1), 0, 10))
            identity_threat = float(np.clip(rng.normal(profile["identity"] + 0.4 * consistency_need, 1), 0, 10))
            self_affirmation = float(np.clip(rng.normal(profile["affirm"], 1), 0, 10))
            external_justification = float(np.clip(rng.normal(profile["just"], 1), 0, 10))
            public_commitment = float(np.clip(rng.normal(profile["public"], 1), 0, 10))
            effort_cost = float(np.clip(rng.normal(profile["effort"], 1), 0, 10))
            disconfirmation = float(np.clip(rng.normal(profile["disc"], 1), 0, 10))
            commitment = float(np.clip(rng.normal(profile["commit"], 1), 0, 10))
            institutional_identity_threat = float(np.clip(rng.normal(profile["inst"], 1), 0, 10))
            sunk_cost = float(np.clip(rng.normal(profile["sunk"], 1), 0, 10))
            evidence_strength = float(np.clip(rng.normal(profile["evidence"], 1), 0, 10))
            accountability = float(np.clip(rng.normal(profile["acct"], 1), 0, 10))

            dissonance_pressure = (
                0.24 * counter
                + 0.22 * perceived_choice
                + 0.20 * responsibility
                + 0.28 * identity_threat
                + 0.22 * public_commitment
                + 0.16 * effort_cost
                + 0.18 * disconfirmation
                + 0.12 * commitment
                - 0.22 * external_justification
                - 0.20 * self_affirmation
                + rng.normal(0, 0.8)
            )
            dissonance_pressure = float(np.clip(dissonance_pressure, 0, 10))

            attitude_change = (
                1.8 * dissonance_pressure
                + 1.2 * perceived_choice
                + 1.0 * identity_threat
                - 1.3 * external_justification
                - 1.4 * self_affirmation
                + rng.normal(0, 8)
            )
            post_attitude = float(np.clip(pre_attitude + attitude_change, -100, 100))

            chosen_pre = float(np.clip(rng.normal(60, 12), 0, 100))
            rejected_pre = float(np.clip(chosen_pre + rng.normal(0, 5), 0, 100))
            spread_boost = 1.8 * perceived_choice + 1.4 * public_commitment + 0.8 * identity_threat
            chosen_post = float(np.clip(chosen_pre + spread_boost / 2 + rng.normal(0, 6), 0, 100))
            rejected_post = float(np.clip(rejected_pre - spread_boost / 2 + rng.normal(0, 6), 0, 100))

            outcome_value = float(np.clip(
                45
                + 3.2 * effort_cost
                + 2.0 * commitment
                + 1.1 * public_commitment
                - 1.0 * self_affirmation
                + rng.normal(0, 9),
                0, 100
            ))

            proselytizing = float(np.clip(
                8
                + 6.0 * disconfirmation
                + 4.5 * commitment
                + 2.0 * public_commitment
                - 4.0 * self_affirmation
                + rng.normal(0, 10),
                0, 100
            ))

            response_time = int(np.clip(np.exp(
                math.log(780)
                + 0.035 * dissonance_pressure
                + 0.030 * identity_threat
                + 0.025 * disconfirmation
                - 0.015 * self_affirmation
                + rng.normal(0, 0.22)
            ), 150, 120000))

            reversal = float(np.clip(
                80
                + 4.0 * evidence_strength
                + 3.5 * accountability
                - 4.5 * sunk_cost
                - 4.0 * public_commitment
                - 3.5 * institutional_identity_threat
                + rng.normal(0, 10),
                0, 100
            ))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "paradigm": paradigm,
                "condition": condition,
                "trial": t,
                "pre_attitude": round(pre_attitude, 3),
                "post_attitude": round(post_attitude, 3),
                "counter_attitudinal_behavior": round(counter, 3),
                "perceived_choice": round(perceived_choice, 3),
                "perceived_responsibility": round(responsibility, 3),
                "identity_threat": round(identity_threat, 3),
                "self_affirmation": round(self_affirmation, 3),
                "external_justification": round(external_justification, 3),
                "public_commitment": round(public_commitment, 3),
                "effort_cost": round(effort_cost, 3),
                "outcome_value": round(outcome_value, 3),
                "chosen_pre_value": round(chosen_pre, 3),
                "chosen_post_value": round(chosen_post, 3),
                "rejected_pre_value": round(rejected_pre, 3),
                "rejected_post_value": round(rejected_post, 3),
                "belief_disconfirmation_strength": round(disconfirmation, 3),
                "commitment_strength": round(commitment, 3),
                "proselytizing_intensity": round(proselytizing, 3),
                "coherence_pressure": round(dissonance_pressure, 3),
                "dissonance_discomfort": round(np.clip(dissonance_pressure + rng.normal(0, 1), 0, 10), 3),
                "response_time_ms": response_time,
                "institutional_identity_threat": round(institutional_identity_threat, 3),
                "sunk_cost": round(sunk_cost, 3),
                "evidence_strength": round(evidence_strength, 3),
                "accountability": round(accountability, 3),
                "policy_reversal_willingness": round(reversal, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["attitude_change"] = data["post_attitude"] - data["pre_attitude"]
    data["spreading_of_alternatives"] = (
        (data["chosen_post_value"] - data["chosen_pre_value"])
        - (data["rejected_post_value"] - data["rejected_pre_value"])
    )
    data["log_response_time"] = np.log(data["response_time_ms"])
    data["dissonance_magnitude_index"] = (
        data["counter_attitudinal_behavior"]
        + data["perceived_choice"]
        + data["perceived_responsibility"]
        + data["identity_threat"]
        + data["public_commitment"]
        - data["external_justification"]
        - data["self_affirmation"]
    ) / 5.0
    data["institutional_escalation_index"] = (
        data["sunk_cost"]
        + data["public_commitment"]
        + data["institutional_identity_threat"]
        - data["evidence_strength"]
        - data["accountability"]
    ) / 3.0
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["paradigm", "condition"], observed=True)
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_attitude_change=("attitude_change", "mean"),
            mean_spreading=("spreading_of_alternatives", "mean"),
            mean_outcome_value=("outcome_value", "mean"),
            mean_proselytizing=("proselytizing_intensity", "mean"),
            mean_coherence_pressure=("coherence_pressure", "mean"),
            mean_discomfort=("dissonance_discomfort", "mean"),
            mean_policy_reversal=("policy_reversal_willingness", "mean"),
        )
        .reset_index()
    )

    context_summary = (
        data.groupby(["institution_context", "paradigm"], observed=True)
        .agg(
            n=("participant", "size"),
            mean_dissonance_magnitude=("dissonance_magnitude_index", "mean"),
            mean_attitude_change=("attitude_change", "mean"),
            mean_institutional_escalation=("institutional_escalation_index", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_paradigm_condition.csv", index=False)
    context_summary.to_csv(outputs / "summary_by_context_paradigm.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "attitude_change_model": (
            "attitude_change ~ paradigm + condition + counter_attitudinal_behavior "
            "+ perceived_choice + perceived_responsibility + identity_threat "
            "+ self_affirmation + external_justification + public_commitment"
        ),
        "spreading_model": (
            "spreading_of_alternatives ~ perceived_choice + public_commitment "
            "+ identity_threat + self_affirmation + external_justification + condition"
        ),
        "effort_justification_model": (
            "outcome_value ~ effort_cost + commitment_strength + public_commitment "
            "+ identity_threat + self_affirmation + condition"
        ),
        "belief_disconfirmation_model": (
            "proselytizing_intensity ~ belief_disconfirmation_strength + commitment_strength "
            "+ public_commitment + identity_threat + self_affirmation + condition"
        ),
        "response_time_model": (
            "log_response_time ~ coherence_pressure + identity_threat "
            "+ belief_disconfirmation_strength + self_affirmation + condition"
        ),
        "institutional_reversal_model": (
            "policy_reversal_willingness ~ evidence_strength + accountability "
            "+ sunk_cost + public_commitment + institutional_identity_threat + condition"
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


def simulate_institutional_escalation(outputs: Path, steps: int = 80, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    scenarios = [
        "low_sunk_cost_high_accountability",
        "high_sunk_cost_low_accountability",
        "public_commitment_high_identity_threat",
        "evidence_review_with_oversight",
        "face_saving_reversal_pathway",
    ]

    for scenario in scenarios:
        commitment = 0.45

        for step in range(1, steps + 1):
            if scenario == "low_sunk_cost_high_accountability":
                sunk, public, threat, evidence, accountability = 0.2, 0.2, 0.2, 0.8, 0.9
            elif scenario == "high_sunk_cost_low_accountability":
                sunk, public, threat, evidence, accountability = 0.9, 0.8, 0.7, 0.8, 0.2
            elif scenario == "public_commitment_high_identity_threat":
                sunk, public, threat, evidence, accountability = 0.7, 0.95, 0.95, 0.8, 0.3
            elif scenario == "evidence_review_with_oversight":
                sunk, public, threat, evidence, accountability = 0.5, 0.5, 0.4, 0.9, 0.9
            else:
                sunk, public, threat, evidence, accountability = 0.7, 0.8, 0.8, 0.8, 0.7

            rationalization_pressure = sunk + public + threat - evidence - accountability
            commitment = commitment + 0.06 * rationalization_pressure + rng.normal(0, 0.025)
            commitment = float(np.clip(commitment, 0, 1))

            reversal_probability = 1 / (1 + np.exp(4.0 * (commitment - 0.5)))

            rows.append({
                "scenario": scenario,
                "step": step,
                "commitment_escalation": commitment,
                "rationalization_pressure": rationalization_pressure,
                "reversal_probability": reversal_probability,
                "sunk_cost": sunk,
                "public_commitment": public,
                "identity_threat": threat,
                "evidence_strength": evidence,
                "accountability": accountability,
            })

    pd.DataFrame(rows).to_csv(outputs / "institutional_escalation_simulation.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/dissonance_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=700)
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
        default_input = Path("data/dissonance_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_escalation(args.outputs, seed=args.seed)
    print(f"Wrote outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
