#!/usr/bin/env python3
"""
Group polarization and collective judgment model.

This script can:
1. Generate synthetic group-discussion data.
2. Estimate attitude-shift, confidence, decision-quality, collective-accuracy, and response-time models.
3. Test persuasive arguments, argument diversity, informational homogeneity, social comparison, identity salience, norm enforcement, dissent quality, deliberation structure, algorithmic reinforcement, and cross-cutting exposure effects.
4. Simulate repeated discussion under homogeneous, heterogeneous, platform-reinforced, and structured-deliberation conditions.
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
    "control", "homogeneous_discussion", "heterogeneous_discussion",
    "persuasive_arguments", "social_comparison", "identity_salience",
    "norm_enforcement", "dissent_present", "structured_deliberation",
    "algorithmic_reinforcement", "cross_cutting_exposure", "high_stakes"
]

PLATFORM_CONTEXTS = [
    "laboratory", "online_forum", "jury", "organization",
    "legislature", "classroom", "platform_feed", "boardroom"
]


def generate_dataset(n_participants: int = 720, trials_per_participant: int = 4, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "control": {"arg": 4.0, "div": 5.5, "hom": 4.0, "soc": 3.5, "ids": 4.0, "gid": 4.8, "norm": 3.0, "diss": 1, "dq": 5.0, "mvp": 5.0, "struct": 4.5, "mod": 5.0, "alg": 2.0, "cross": 4.5, "leg": 5.5, "quality": 62, "acc": 60},
        "homogeneous_discussion": {"arg": 7.5, "div": 2.5, "hom": 8.0, "soc": 6.5, "ids": 6.5, "gid": 6.8, "norm": 6.0, "diss": 0, "dq": 1.5, "mvp": 2.0, "struct": 2.5, "mod": 3.0, "alg": 3.5, "cross": 1.8, "leg": 4.0, "quality": 48, "acc": 46},
        "heterogeneous_discussion": {"arg": 5.0, "div": 8.0, "hom": 3.5, "soc": 3.5, "ids": 4.0, "gid": 4.5, "norm": 3.0, "diss": 1, "dq": 7.8, "mvp": 8.0, "struct": 7.5, "mod": 7.2, "alg": 1.5, "cross": 8.0, "leg": 8.0, "quality": 80, "acc": 82},
        "persuasive_arguments": {"arg": 9.0, "div": 2.2, "hom": 8.5, "soc": 5.8, "ids": 6.2, "gid": 6.5, "norm": 5.2, "diss": 0, "dq": 1.0, "mvp": 1.5, "struct": 2.0, "mod": 3.0, "alg": 5.0, "cross": 1.5, "leg": 4.2, "quality": 44, "acc": 42},
        "social_comparison": {"arg": 6.0, "div": 3.0, "hom": 7.0, "soc": 9.0, "ids": 6.8, "gid": 7.2, "norm": 7.0, "diss": 0, "dq": 1.8, "mvp": 2.0, "struct": 2.2, "mod": 3.0, "alg": 4.0, "cross": 2.0, "leg": 4.0, "quality": 46, "acc": 45},
        "identity_salience": {"arg": 6.5, "div": 3.0, "hom": 7.2, "soc": 7.0, "ids": 9.0, "gid": 8.5, "norm": 7.5, "diss": 0, "dq": 2.0, "mvp": 2.0, "struct": 2.5, "mod": 3.5, "alg": 3.5, "cross": 2.0, "leg": 4.5, "quality": 42, "acc": 40},
        "norm_enforcement": {"arg": 6.8, "div": 2.5, "hom": 8.0, "soc": 8.5, "ids": 7.5, "gid": 8.0, "norm": 9.0, "diss": 0, "dq": 1.5, "mvp": 1.5, "struct": 2.0, "mod": 2.8, "alg": 4.0, "cross": 1.5, "leg": 3.5, "quality": 38, "acc": 36},
        "dissent_present": {"arg": 5.0, "div": 6.8, "hom": 4.5, "soc": 4.2, "ids": 4.8, "gid": 5.2, "norm": 3.5, "diss": 1, "dq": 8.0, "mvp": 7.5, "struct": 6.5, "mod": 6.8, "alg": 2.0, "cross": 6.5, "leg": 7.0, "quality": 72, "acc": 74},
        "structured_deliberation": {"arg": 4.8, "div": 8.2, "hom": 3.5, "soc": 3.0, "ids": 4.0, "gid": 4.5, "norm": 2.5, "diss": 1, "dq": 8.5, "mvp": 8.5, "struct": 9.0, "mod": 8.5, "alg": 1.5, "cross": 8.0, "leg": 8.5, "quality": 84, "acc": 86},
        "algorithmic_reinforcement": {"arg": 8.8, "div": 1.5, "hom": 9.5, "soc": 7.5, "ids": 8.0, "gid": 8.2, "norm": 7.8, "diss": 0, "dq": 1.0, "mvp": 1.2, "struct": 1.8, "mod": 2.0, "alg": 9.5, "cross": 1.0, "leg": 3.0, "quality": 34, "acc": 30},
        "cross_cutting_exposure": {"arg": 5.0, "div": 8.5, "hom": 3.0, "soc": 3.0, "ids": 4.2, "gid": 4.8, "norm": 2.8, "diss": 1, "dq": 7.5, "mvp": 8.0, "struct": 7.5, "mod": 7.0, "alg": 2.0, "cross": 9.0, "leg": 7.8, "quality": 78, "acc": 80},
        "high_stakes": {"arg": 8.0, "div": 2.0, "hom": 8.8, "soc": 8.0, "ids": 8.5, "gid": 8.8, "norm": 8.5, "diss": 0, "dq": 1.0, "mvp": 1.5, "struct": 2.5, "mod": 2.5, "alg": 5.0, "cross": 1.5, "leg": 3.2, "quality": 32, "acc": 28},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 121):03d}"
        site_id = f"S{rng.integers(1, 41):02d}"
        extremity_trait = float(np.clip(rng.normal(0.0, 18.0), -45, 45))
        confidence_trait = float(np.clip(rng.normal(60, 12), 0, 100))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            platform_context = rng.choice(PLATFORM_CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 140):03d}"
            e = effects[condition]

            initial_direction = rng.choice([-1, 1])
            pre_attitude = float(np.clip(initial_direction * abs(rng.normal(25, 18)) + 0.25 * extremity_trait, -100, 100))
            pre_confidence = float(np.clip(rng.normal(confidence_trait, 10), 0, 100))

            argument_exposure = float(np.clip(rng.normal(e["arg"], 1.0), 0, 10))
            argument_diversity = float(np.clip(rng.normal(e["div"], 1.0), 0, 10))
            informational_homogeneity = float(np.clip(rng.normal(e["hom"], 1.0), 0, 10))
            social_comparison_pressure = float(np.clip(rng.normal(e["soc"], 1.0), 0, 10))
            identity_salience = float(np.clip(rng.normal(e["ids"], 1.0), 0, 10))
            group_identification = float(np.clip(rng.normal(e["gid"], 1.0), 0, 10))
            norm_enforcement = float(np.clip(rng.normal(e["norm"], 1.0), 0, 10))
            dissent_presence = int(e["diss"])
            dissent_quality = float(np.clip(rng.normal(e["dq"], 1.0), 0, 10))
            minority_view_protection = float(np.clip(rng.normal(e["mvp"], 1.0), 0, 10))
            deliberation_structure = float(np.clip(rng.normal(e["struct"], 1.0), 0, 10))
            moderation_quality = float(np.clip(rng.normal(e["mod"], 1.0), 0, 10))
            algorithmic_reinforcement = float(np.clip(rng.normal(e["alg"], 1.0), 0, 10))
            cross_cutting_exposure = float(np.clip(rng.normal(e["cross"], 1.0), 0, 10))
            perceived_legitimacy = float(np.clip(rng.normal(e["leg"], 1.0), 0, 10))

            amplification = (
                0.75 * argument_exposure
                - 0.70 * argument_diversity
                + 0.80 * informational_homogeneity
                + 0.70 * social_comparison_pressure
                + 0.60 * identity_salience
                + 0.45 * group_identification
                + 0.65 * norm_enforcement
                + 0.65 * algorithmic_reinforcement
                - 0.85 * dissent_quality
                - 0.70 * minority_view_protection
                - 0.70 * deliberation_structure
                - 0.55 * moderation_quality
                - 0.80 * cross_cutting_exposure
            )

            shift = initial_direction * (amplification + rng.normal(0, 5))
            post_attitude = float(np.clip(pre_attitude + shift, -100, 100))

            confidence_shift = (
                1.2 * argument_exposure
                + 1.0 * informational_homogeneity
                + 0.9 * perceived_legitimacy
                + 0.9 * social_comparison_pressure
                + 0.8 * identity_salience
                - 0.7 * argument_diversity
                - 0.8 * dissent_quality
                - 0.7 * cross_cutting_exposure
                + rng.normal(0, 5)
            )
            post_confidence = float(np.clip(pre_confidence + confidence_shift, 0, 100))

            perceived_consensus = float(np.clip(
                40
                + 3.5 * informational_homogeneity
                + 3.0 * norm_enforcement
                + 2.0 * social_comparison_pressure
                + 2.0 * identity_salience
                - 2.5 * dissent_quality
                - 2.0 * argument_diversity
                + rng.normal(0, 7),
                0, 100
            ))

            decision_quality = float(np.clip(
                e["quality"]
                + 2.6 * argument_diversity
                + 2.4 * dissent_quality
                + 2.5 * minority_view_protection
                + 2.6 * deliberation_structure
                + 1.8 * moderation_quality
                + 1.4 * cross_cutting_exposure
                + 1.2 * perceived_legitimacy
                - 2.0 * informational_homogeneity
                - 1.8 * norm_enforcement
                - 1.8 * algorithmic_reinforcement
                - 0.18 * abs(post_attitude)
                + rng.normal(0, 7),
                0, 100
            ))

            collective_judgment_accuracy = float(np.clip(
                e["acc"]
                + 2.8 * argument_diversity
                + 2.5 * dissent_quality
                + 2.4 * deliberation_structure
                + 1.8 * cross_cutting_exposure
                - 2.2 * informational_homogeneity
                - 1.6 * social_comparison_pressure
                - 1.8 * norm_enforcement
                - 1.6 * algorithmic_reinforcement
                - 0.22 * abs(post_attitude)
                + rng.normal(0, 7),
                0, 100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(900)
                + 0.004 * abs(post_attitude)
                + 0.035 * identity_salience
                + 0.035 * social_comparison_pressure
                - 0.030 * deliberation_structure
                - 0.025 * argument_diversity
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "platform_context": platform_context,
                "condition": condition,
                "trial": t,
                "pre_attitude": round(pre_attitude, 3),
                "post_attitude": round(post_attitude, 3),
                "pre_confidence": round(pre_confidence, 3),
                "post_confidence": round(post_confidence, 3),
                "argument_exposure": round(argument_exposure, 3),
                "argument_diversity": round(argument_diversity, 3),
                "informational_homogeneity": round(informational_homogeneity, 3),
                "social_comparison_pressure": round(social_comparison_pressure, 3),
                "identity_salience": round(identity_salience, 3),
                "group_identification": round(group_identification, 3),
                "norm_enforcement": round(norm_enforcement, 3),
                "dissent_presence": dissent_presence,
                "dissent_quality": round(dissent_quality, 3),
                "minority_view_protection": round(minority_view_protection, 3),
                "deliberation_structure": round(deliberation_structure, 3),
                "moderation_quality": round(moderation_quality, 3),
                "algorithmic_reinforcement": round(algorithmic_reinforcement, 3),
                "cross_cutting_exposure": round(cross_cutting_exposure, 3),
                "perceived_consensus": round(perceived_consensus, 3),
                "perceived_legitimacy": round(perceived_legitimacy, 3),
                "decision_quality": round(decision_quality, 3),
                "collective_judgment_accuracy": round(collective_judgment_accuracy, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["attitude_shift"] = data["post_attitude"] - data["pre_attitude"]
    data["extremity_shift"] = data["post_attitude"].abs() - data["pre_attitude"].abs()
    data["confidence_shift"] = data["post_confidence"] - data["pre_confidence"]
    data["directional_polarization"] = (
        (data["post_attitude"].abs() > data["pre_attitude"].abs()) &
        (np.sign(data["post_attitude"]) == np.sign(data["pre_attitude"]))
    ).astype(int)
    data["polarization_risk_index"] = (
        data["argument_exposure"]
        + data["informational_homogeneity"]
        + data["social_comparison_pressure"]
        + data["identity_salience"]
        + data["group_identification"]
        + data["norm_enforcement"]
        + data["algorithmic_reinforcement"]
        - data["argument_diversity"]
        - data["dissent_quality"]
        - data["minority_view_protection"]
        - data["deliberation_structure"]
        - data["cross_cutting_exposure"]
    ) / 6.0
    data["deliberative_safeguard_index"] = (
        data["argument_diversity"]
        + data["dissent_quality"]
        + data["minority_view_protection"]
        + data["deliberation_structure"]
        + data["moderation_quality"]
        + data["cross_cutting_exposure"]
        + data["perceived_legitimacy"]
    ) / 7.0
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "platform_context"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            groups=("group_id", "nunique"),
            mean_pre_attitude=("pre_attitude", "mean"),
            mean_post_attitude=("post_attitude", "mean"),
            mean_shift=("attitude_shift", "mean"),
            mean_extremity_shift=("extremity_shift", "mean"),
            directional_polarization_rate=("directional_polarization", "mean"),
            mean_confidence_shift=("confidence_shift", "mean"),
            mean_argument_exposure=("argument_exposure", "mean"),
            mean_argument_diversity=("argument_diversity", "mean"),
            mean_homogeneity=("informational_homogeneity", "mean"),
            mean_identity_salience=("identity_salience", "mean"),
            mean_dissent_quality=("dissent_quality", "mean"),
            mean_safeguards=("deliberative_safeguard_index", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
            mean_accuracy=("collective_judgment_accuracy", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby("condition")
        .agg(
            n=("participant", "size"),
            mean_extremity_shift=("extremity_shift", "mean"),
            directional_polarization_rate=("directional_polarization", "mean"),
            mean_confidence_shift=("confidence_shift", "mean"),
            mean_decision_quality=("decision_quality", "mean"),
            mean_accuracy=("collective_judgment_accuracy", "mean"),
            mean_risk=("polarization_risk_index", "mean"),
            mean_safeguards=("deliberative_safeguard_index", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    condition_summary.to_csv(outputs / "summary_by_condition.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "extremity_shift_model": "extremity_shift ~ argument_exposure + argument_diversity + informational_homogeneity + social_comparison_pressure + identity_salience + group_identification + norm_enforcement + dissent_presence + dissent_quality + minority_view_protection + deliberation_structure + moderation_quality + algorithmic_reinforcement + cross_cutting_exposure + perceived_legitimacy + condition + platform_context",
        "confidence_shift_model": "confidence_shift ~ argument_exposure + informational_homogeneity + social_comparison_pressure + identity_salience + group_identification + norm_enforcement + argument_diversity + dissent_quality + deliberation_structure + cross_cutting_exposure + condition + platform_context",
        "decision_quality_model": "decision_quality ~ polarization_risk_index + deliberative_safeguard_index + argument_diversity + dissent_quality + minority_view_protection + deliberation_structure + algorithmic_reinforcement + cross_cutting_exposure + perceived_legitimacy + abs(post_attitude) + condition + platform_context",
        "accuracy_model": "collective_judgment_accuracy ~ polarization_risk_index + deliberative_safeguard_index + informational_homogeneity + norm_enforcement + algorithmic_reinforcement + cross_cutting_exposure + perceived_legitimacy + abs(post_attitude) + condition + platform_context",
        "response_time_model": "log_response_time ~ abs(post_attitude) + identity_salience + social_comparison_pressure + informational_homogeneity + deliberation_structure + argument_diversity + dissent_quality + condition + platform_context",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        model = smf.ols(formula, data=data).fit(
            cov_type="cluster", cov_kwds={"groups": data["group_id"]}
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


def simulate_repeated_discussion(outputs: Path, n_groups: int = 1000, periods: int = 18, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    scenarios = ["homogeneous_discussion", "algorithmic_reinforcement", "cross_cutting_exposure", "structured_deliberation", "dissent_protected"]

    for scenario in scenarios:
        for group in range(1, n_groups + 1):
            attitude = rng.choice([-1, 1]) * abs(rng.normal(25, 12))
            confidence = np.clip(rng.normal(60, 10), 0, 100)

            if scenario == "homogeneous_discussion":
                homogeneity, identity, enforcement, safeguards, cross_cutting = 8.0, 6.5, 6.0, 3.0, 2.0
            elif scenario == "algorithmic_reinforcement":
                homogeneity, identity, enforcement, safeguards, cross_cutting = 9.5, 8.0, 7.5, 2.0, 1.0
            elif scenario == "cross_cutting_exposure":
                homogeneity, identity, enforcement, safeguards, cross_cutting = 3.0, 4.5, 3.0, 7.5, 9.0
            elif scenario == "structured_deliberation":
                homogeneity, identity, enforcement, safeguards, cross_cutting = 3.5, 4.0, 2.5, 9.0, 8.0
            else:
                homogeneity, identity, enforcement, safeguards, cross_cutting = 4.5, 5.0, 3.5, 8.2, 6.5

            for period in range(1, periods + 1):
                direction = np.sign(attitude) if attitude != 0 else rng.choice([-1, 1])
                amplification = (
                    0.60 * homogeneity
                    + 0.45 * identity
                    + 0.50 * enforcement
                    - 0.65 * safeguards
                    - 0.55 * cross_cutting
                    + rng.normal(0, 2)
                )
                attitude = np.clip(attitude + direction * amplification, -100, 100)
                confidence = np.clip(confidence + 0.8 * homogeneity + 0.6 * enforcement - 0.7 * safeguards + rng.normal(0, 3), 0, 100)
                quality = np.clip(80 + 3.0 * safeguards + 2.0 * cross_cutting - 2.5 * homogeneity - 2.0 * enforcement - 0.20 * abs(attitude) + rng.normal(0, 5), 0, 100)

                rows.append({
                    "scenario": scenario,
                    "group": group,
                    "period": period,
                    "mean_attitude": attitude,
                    "mean_extremity": abs(attitude),
                    "mean_confidence": confidence,
                    "decision_quality": quality,
                    "informational_homogeneity": homogeneity,
                    "identity_salience": identity,
                    "norm_enforcement": enforcement,
                    "deliberative_safeguards": safeguards,
                    "cross_cutting_exposure": cross_cutting,
                })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby(["scenario", "period"])
        .agg(
            mean_attitude=("mean_attitude", "mean"),
            mean_extremity=("mean_extremity", "mean"),
            mean_confidence=("mean_confidence", "mean"),
            mean_quality=("decision_quality", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "repeated_discussion_simulation.csv", index=False)
    summary.to_csv(outputs / "repeated_discussion_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/group_polarization_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=720)
    parser.add_argument("--trials", type=int, default=4)
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
        default_input = Path("data/group_polarization_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_repeated_discussion(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
