#!/usr/bin/env python3
"""
Social norms research model.

This script can:
1. Generate synthetic social-norms data.
2. Estimate norm-compliance, intention, contribution, reporting, and response-time models.
3. Test descriptive norm, injunctive norm, empirical expectation, normative expectation, sanction, reference-group, legitimacy, dynamic-norm, and pluralistic-ignorance effects.
4. Simulate norm-message effects, boomerang risk, and threshold/tipping dynamics.
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
    "control", "descriptive_norm", "injunctive_norm", "combined_norm",
    "dynamic_norm", "misperception_correction", "high_sanction", "low_sanction",
    "high_legitimacy", "low_legitimacy", "pluralistic_ignorance", "threshold_exposure"
]

POLICY_DOMAINS = [
    "environment", "public_health", "workplace", "education",
    "digital_platform", "civic", "common_pool", "safety"
]

REFERENCE_GROUPS = [
    "neighbors", "work_team", "students", "platform_users",
    "citizens", "peers", "community", "profession"
]

MESSAGE_TYPES = ["none", "descriptive", "injunctive", "combined", "dynamic", "correction"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 640, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "control": {"desc": 48, "inj": 56, "emp": 50, "norm": 54, "att": 62, "sal": 4.5, "san": 2.5, "sev": 2.0, "rew": 3.0, "id": 5.0, "leg": 5.5, "trust": 5.2, "trend": 0, "message": "none"},
        "descriptive_norm": {"desc": 72, "inj": 56, "emp": 70, "norm": 55, "att": 62, "sal": 6.5, "san": 2.5, "sev": 2.0, "rew": 3.5, "id": 5.2, "leg": 5.5, "trust": 5.2, "trend": 4, "message": "descriptive"},
        "injunctive_norm": {"desc": 48, "inj": 84, "emp": 50, "norm": 82, "att": 66, "sal": 6.8, "san": 4.8, "sev": 4.0, "rew": 5.5, "id": 5.8, "leg": 6.0, "trust": 5.8, "trend": 2, "message": "injunctive"},
        "combined_norm": {"desc": 76, "inj": 88, "emp": 74, "norm": 86, "att": 70, "sal": 8.5, "san": 5.0, "sev": 4.5, "rew": 6.0, "id": 7.5, "leg": 7.0, "trust": 7.2, "trend": 8, "message": "combined"},
        "dynamic_norm": {"desc": 42, "inj": 60, "emp": 45, "norm": 62, "att": 68, "sal": 7.0, "san": 3.0, "sev": 3.0, "rew": 5.2, "id": 6.0, "leg": 6.5, "trust": 6.0, "trend": 42, "message": "dynamic"},
        "misperception_correction": {"desc": 38, "inj": 72, "emp": 40, "norm": 74, "att": 78, "sal": 7.5, "san": 3.8, "sev": 3.5, "rew": 4.5, "id": 5.5, "leg": 5.8, "trust": 5.6, "trend": 24, "message": "correction"},
        "high_sanction": {"desc": 60, "inj": 78, "emp": 62, "norm": 80, "att": 65, "sal": 7.2, "san": 8.5, "sev": 8.0, "rew": 4.0, "id": 6.5, "leg": 6.0, "trust": 5.8, "trend": 5, "message": "injunctive"},
        "low_sanction": {"desc": 55, "inj": 70, "emp": 56, "norm": 68, "att": 72, "sal": 5.8, "san": 1.5, "sev": 1.0, "rew": 3.0, "id": 5.5, "leg": 6.5, "trust": 6.0, "trend": 5, "message": "descriptive"},
        "high_legitimacy": {"desc": 64, "inj": 82, "emp": 66, "norm": 84, "att": 78, "sal": 7.8, "san": 4.5, "sev": 4.0, "rew": 5.8, "id": 6.8, "leg": 8.8, "trust": 8.5, "trend": 12, "message": "combined"},
        "low_legitimacy": {"desc": 64, "inj": 82, "emp": 66, "norm": 84, "att": 78, "sal": 5.0, "san": 3.5, "sev": 3.0, "rew": 3.2, "id": 5.0, "leg": 2.2, "trust": 2.5, "trend": 12, "message": "combined"},
        "pluralistic_ignorance": {"desc": 78, "inj": 35, "emp": 76, "norm": 38, "att": 72, "sal": 6.5, "san": 4.0, "sev": 4.0, "rew": 3.0, "id": 7.0, "leg": 5.5, "trust": 5.4, "trend": -8, "message": "none"},
        "threshold_exposure": {"desc": 52, "inj": 66, "emp": 54, "norm": 68, "att": 70, "sal": 7.5, "san": 4.5, "sev": 4.0, "rew": 5.5, "id": 7.0, "leg": 7.5, "trust": 7.0, "trend": 38, "message": "dynamic"},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        site_id = f"S{rng.integers(1, 41):02d}"
        norm_sensitivity = float(np.clip(rng.normal(5.8, 1.6), 0, 10))
        sanction_sensitivity = float(np.clip(rng.normal(5.5, 1.7), 0, 10))
        trust_trait = float(np.clip(rng.normal(5.5, 1.5), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            scenario_id = f"SC{rng.integers(1, 110):03d}"
            reference_group = rng.choice(REFERENCE_GROUPS)
            policy_domain = rng.choice(POLICY_DOMAINS)
            e = effects[condition]

            descriptive_norm = float(np.clip(rng.normal(e["desc"], 9), 0, 100))
            injunctive_norm = float(np.clip(rng.normal(e["inj"], 8), 0, 100))
            empirical_expectation = float(np.clip(rng.normal(e["emp"], 8), 0, 100))
            normative_expectation = float(np.clip(rng.normal(e["norm"], 8), 0, 100))
            personal_attitude = float(np.clip(rng.normal(e["att"], 10), 0, 100))
            norm_salience = float(np.clip(rng.normal(e["sal"], 1.0), 0, 10))
            sanction_salience = float(np.clip(rng.normal(e["san"], 1.0), 0, 10))
            sanction_severity = float(np.clip(rng.normal(e["sev"], 1.0), 0, 10))
            reward_salience = float(np.clip(rng.normal(e["rew"], 1.0), 0, 10))
            reference_group_identification = float(np.clip(rng.normal(e["id"], 1.1), 0, 10))
            institutional_legitimacy = float(np.clip(rng.normal(0.65 * e["leg"] + 0.35 * trust_trait, 1.0), 0, 10))
            trust_in_institution = float(np.clip(rng.normal(0.60 * e["trust"] + 0.40 * trust_trait, 1.0), 0, 10))
            dynamic_norm_trend = float(np.clip(rng.normal(e["trend"], 10), -100, 100))
            message_type = e["message"]

            pluralistic_ignorance = float(np.clip(abs(personal_attitude - injunctive_norm), 0, 100))
            norm_threshold = float(np.clip(rng.normal(55 - 1.5 * norm_sensitivity + 0.7 * sanction_sensitivity, 10), 0, 100))
            tipping_exposure = float(np.clip(rng.normal(max(0, dynamic_norm_trend) + 0.35 * descriptive_norm, 12), 0, 100))

            latent = (
                -5.6
                + 0.022 * descriptive_norm
                + 0.026 * injunctive_norm
                + 0.024 * empirical_expectation
                + 0.028 * normative_expectation
                + 0.018 * personal_attitude
                + 0.22 * norm_salience
                + 0.18 * sanction_salience
                + 0.12 * sanction_severity
                + 0.16 * reward_salience
                + 0.20 * reference_group_identification
                + 0.20 * institutional_legitimacy
                + 0.14 * trust_in_institution
                + 0.012 * dynamic_norm_trend
                + 0.09 * norm_sensitivity
                - 0.010 * pluralistic_ignorance
                + 0.018 * (tipping_exposure - norm_threshold)
            )

            compliance_prob = float(logistic(latent))
            complied = int(rng.random() < compliance_prob)

            compliance_intention = float(np.clip(
                100 * compliance_prob + rng.normal(0, 7),
                0, 100
            ))

            contribution_amount = float(np.clip(
                5
                + 0.50 * compliance_intention
                + 1.1 * institutional_legitimacy
                + 0.8 * trust_in_institution
                + 0.5 * reward_salience
                - 0.15 * pluralistic_ignorance
                + rng.normal(0, 8),
                0, 100
            ))

            report_latent = (
                -4.5
                + 0.030 * injunctive_norm
                + 0.030 * normative_expectation
                + 0.25 * sanction_salience
                + 0.20 * sanction_severity
                + 0.18 * institutional_legitimacy
                + 0.12 * reference_group_identification
                - 0.010 * pluralistic_ignorance
            )
            reported_violation = int(rng.random() < float(logistic(report_latent)))

            post_message_norm_perception = float(np.clip(
                0.35 * descriptive_norm
                + 0.35 * injunctive_norm
                + 0.20 * empirical_expectation
                + 0.10 * normative_expectation
                + 0.20 * max(0, dynamic_norm_trend)
                + rng.normal(0, 7),
                0, 100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(950)
                + 0.004 * pluralistic_ignorance
                + 0.025 * (10 - norm_salience)
                + 0.018 * (10 - institutional_legitimacy)
                - 0.006 * compliance_intention
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "reference_group": reference_group,
                "policy_domain": policy_domain,
                "condition": condition,
                "trial": t,
                "descriptive_norm": round(descriptive_norm, 3),
                "injunctive_norm": round(injunctive_norm, 3),
                "empirical_expectation": round(empirical_expectation, 3),
                "normative_expectation": round(normative_expectation, 3),
                "personal_attitude": round(personal_attitude, 3),
                "norm_salience": round(norm_salience, 3),
                "sanction_salience": round(sanction_salience, 3),
                "sanction_severity": round(sanction_severity, 3),
                "reward_salience": round(reward_salience, 3),
                "reference_group_identification": round(reference_group_identification, 3),
                "institutional_legitimacy": round(institutional_legitimacy, 3),
                "trust_in_institution": round(trust_in_institution, 3),
                "pluralistic_ignorance": round(pluralistic_ignorance, 3),
                "dynamic_norm_trend": round(dynamic_norm_trend, 3),
                "message_type": message_type,
                "complied": complied,
                "compliance_intention": round(compliance_intention, 3),
                "contribution_amount": round(contribution_amount, 3),
                "reported_violation": reported_violation,
                "response_time_ms": response_time_ms,
                "norm_threshold": round(norm_threshold, 3),
                "tipping_exposure": round(tipping_exposure, 3),
                "post_message_norm_perception": round(post_message_norm_perception, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["norm_strength_index"] = (
        data["descriptive_norm"]
        + data["injunctive_norm"]
        + data["empirical_expectation"]
        + data["normative_expectation"]
    ) / 4.0
    data["enforcement_index"] = (
        data["sanction_salience"]
        + data["sanction_severity"]
        + data["reward_salience"]
    ) / 3.0
    data["legitimacy_trust_index"] = (
        data["institutional_legitimacy"]
        + data["trust_in_institution"]
    ) / 2.0
    data["tipping_margin"] = data["tipping_exposure"] - data["norm_threshold"]
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "policy_domain", "message_type"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            compliance_rate=("complied", "mean"),
            reporting_rate=("reported_violation", "mean"),
            mean_intention=("compliance_intention", "mean"),
            mean_contribution=("contribution_amount", "mean"),
            mean_descriptive=("descriptive_norm", "mean"),
            mean_injunctive=("injunctive_norm", "mean"),
            mean_empirical=("empirical_expectation", "mean"),
            mean_normative=("normative_expectation", "mean"),
            mean_personal_attitude=("personal_attitude", "mean"),
            mean_pluralistic_ignorance=("pluralistic_ignorance", "mean"),
            mean_norm_strength=("norm_strength_index", "mean"),
            mean_enforcement=("enforcement_index", "mean"),
            mean_legitimacy_trust=("legitimacy_trust_index", "mean"),
            mean_tipping_margin=("tipping_margin", "mean"),
            mean_response_time=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    message_summary = (
        data.groupby(["message_type"])
        .agg(
            n=("participant", "size"),
            compliance_rate=("complied", "mean"),
            reporting_rate=("reported_violation", "mean"),
            mean_intention=("compliance_intention", "mean"),
            mean_post_norm=("post_message_norm_perception", "mean"),
            mean_contribution=("contribution_amount", "mean"),
            mean_tipping_margin=("tipping_margin", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_domain_message.csv", index=False)
    message_summary.to_csv(outputs / "summary_by_message_type.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "compliance_model": "complied ~ descriptive_norm + injunctive_norm + empirical_expectation + normative_expectation + personal_attitude + norm_salience + sanction_salience + sanction_severity + reward_salience + reference_group_identification + institutional_legitimacy + trust_in_institution + pluralistic_ignorance + dynamic_norm_trend + tipping_margin + condition + policy_domain + message_type",
        "intention_model": "compliance_intention ~ descriptive_norm + injunctive_norm + empirical_expectation + normative_expectation + personal_attitude + norm_salience + sanction_salience + reference_group_identification + institutional_legitimacy + trust_in_institution + pluralistic_ignorance + dynamic_norm_trend + condition + policy_domain + message_type",
        "contribution_model": "contribution_amount ~ norm_strength_index + enforcement_index + legitimacy_trust_index + reference_group_identification + personal_attitude + pluralistic_ignorance + dynamic_norm_trend + complied + condition + policy_domain + message_type",
        "reporting_model": "reported_violation ~ injunctive_norm + normative_expectation + sanction_salience + sanction_severity + institutional_legitimacy + reference_group_identification + pluralistic_ignorance + condition + policy_domain + message_type",
        "response_time_model": "log_response_time ~ norm_strength_index + norm_salience + pluralistic_ignorance + legitimacy_trust_index + tipping_margin + complied + condition + policy_domain + message_type",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name in ["compliance_model", "reporting_model"]:
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


def simulate_thresholds(outputs: Path, n_cases: int = 10000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    for scenario in ["stable_low_norm", "stable_high_norm", "dynamic_growth", "injunctive_boost", "boomerang_risk", "legitimacy_loss"]:
        for _ in range(n_cases):
            if scenario == "stable_low_norm":
                perceived_compliance = rng.normal(35, 8)
                approval = rng.normal(42, 8)
                trend = rng.normal(0, 5)
                legitimacy = rng.normal(5.5, 1)
            elif scenario == "stable_high_norm":
                perceived_compliance = rng.normal(78, 8)
                approval = rng.normal(84, 6)
                trend = rng.normal(2, 5)
                legitimacy = rng.normal(7.0, 1)
            elif scenario == "dynamic_growth":
                perceived_compliance = rng.normal(46, 8)
                approval = rng.normal(62, 7)
                trend = rng.normal(40, 8)
                legitimacy = rng.normal(6.5, 1)
            elif scenario == "injunctive_boost":
                perceived_compliance = rng.normal(50, 8)
                approval = rng.normal(88, 6)
                trend = rng.normal(8, 5)
                legitimacy = rng.normal(7.0, 1)
            elif scenario == "boomerang_risk":
                perceived_compliance = rng.normal(45, 8)
                approval = rng.normal(35, 8)
                trend = rng.normal(-10, 6)
                legitimacy = rng.normal(5.0, 1)
            else:
                perceived_compliance = rng.normal(70, 8)
                approval = rng.normal(80, 6)
                trend = rng.normal(8, 5)
                legitimacy = rng.normal(2.5, 1)

            threshold = np.clip(rng.normal(55, 12), 0, 100)
            tipping_exposure = np.clip(perceived_compliance + 0.45 * max(0, trend) + 0.20 * approval + rng.normal(0, 8), 0, 100)
            compliance_pressure = tipping_exposure - threshold

            latent = -3.0 + 0.030 * perceived_compliance + 0.030 * approval + 0.020 * trend + 0.25 * legitimacy + 0.035 * compliance_pressure
            prob = float(logistic(latent))
            complied = int(rng.random() < prob)

            rows.append({
                "scenario": scenario,
                "perceived_compliance": perceived_compliance,
                "perceived_approval": approval,
                "dynamic_norm_trend": trend,
                "institutional_legitimacy": legitimacy,
                "norm_threshold": threshold,
                "tipping_exposure": tipping_exposure,
                "tipping_margin": compliance_pressure,
                "compliance_probability": prob,
                "complied": complied,
            })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby("scenario")
        .agg(
            n=("scenario", "size"),
            mean_perceived_compliance=("perceived_compliance", "mean"),
            mean_approval=("perceived_approval", "mean"),
            mean_trend=("dynamic_norm_trend", "mean"),
            mean_legitimacy=("institutional_legitimacy", "mean"),
            mean_tipping_margin=("tipping_margin", "mean"),
            mean_probability=("compliance_probability", "mean"),
            compliance_rate=("complied", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "norm_threshold_simulation.csv", index=False)
    summary.to_csv(outputs / "norm_threshold_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/social_norms_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=640)
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
        default_input = Path("data/social_norms_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_thresholds(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
