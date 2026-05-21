#!/usr/bin/env python3
"""
Conformity and social influence model.

This script can:
1. Generate synthetic conformity data for Asch-style, Sherif-style, digital, and institutional conditions.
2. Estimate conformity, dissent, confidence-shift, and response-time models.
3. Simulate network diffusion and digital social-proof effects.
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
    "control", "ambiguous_task", "unanimous_majority", "broken_unanimity",
    "public_response", "private_response", "high_cohesion", "high_status_majority",
    "visible_ally", "consistent_minority", "digital_social_proof", "algorithmic_amplification"
]

CONTEXTS = ["laboratory", "classroom", "workplace", "organization", "platform", "public_opinion", "network_simulation"]


def logistic(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def generate_dataset(n_participants: int = 800, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "control": {"amb": 4.5, "maj": 3, "uni": 5.0, "dis": 3.5, "coh": 5.0, "norm": 4.2, "info": 4.5, "stat": 4.0, "pub": 1, "priv": 0, "gid": 5.0, "sid": 4.8, "minor": 2.0, "net": 2.5, "proof": 2.0, "alg": 1.0},
        "ambiguous_task": {"amb": 8.5, "maj": 3, "uni": 6.5, "dis": 2.5, "coh": 5.2, "norm": 5.0, "info": 8.8, "stat": 5.0, "pub": 1, "priv": 0, "gid": 5.5, "sid": 5.0, "minor": 2.0, "net": 3.0, "proof": 2.0, "alg": 1.0},
        "unanimous_majority": {"amb": 4.0, "maj": 5, "uni": 9.5, "dis": 0.5, "coh": 6.0, "norm": 8.0, "info": 5.0, "stat": 6.0, "pub": 1, "priv": 0, "gid": 6.5, "sid": 6.2, "minor": 0.0, "net": 3.5, "proof": 2.5, "alg": 1.0},
        "broken_unanimity": {"amb": 4.0, "maj": 5, "uni": 5.0, "dis": 8.5, "coh": 6.0, "norm": 4.5, "info": 4.5, "stat": 6.0, "pub": 1, "priv": 0, "gid": 6.0, "sid": 6.0, "minor": 7.5, "net": 3.0, "proof": 2.0, "alg": 1.0},
        "public_response": {"amb": 5.0, "maj": 4, "uni": 8.5, "dis": 1.0, "coh": 7.0, "norm": 8.5, "info": 5.0, "stat": 5.8, "pub": 1, "priv": 0, "gid": 7.2, "sid": 7.0, "minor": 1.0, "net": 4.0, "proof": 3.0, "alg": 1.5},
        "private_response": {"amb": 5.0, "maj": 4, "uni": 8.5, "dis": 1.0, "coh": 7.0, "norm": 4.0, "info": 5.0, "stat": 5.8, "pub": 0, "priv": 1, "gid": 7.2, "sid": 7.0, "minor": 1.0, "net": 4.0, "proof": 3.0, "alg": 1.5},
        "high_cohesion": {"amb": 5.5, "maj": 4, "uni": 8.0, "dis": 1.0, "coh": 9.0, "norm": 8.0, "info": 5.2, "stat": 6.5, "pub": 1, "priv": 0, "gid": 8.8, "sid": 8.5, "minor": 2.0, "net": 5.0, "proof": 4.0, "alg": 2.0},
        "high_status_majority": {"amb": 5.0, "maj": 4, "uni": 8.0, "dis": 1.0, "coh": 6.8, "norm": 7.0, "info": 5.5, "stat": 9.0, "pub": 1, "priv": 0, "gid": 7.0, "sid": 6.8, "minor": 1.5, "net": 4.5, "proof": 4.0, "alg": 2.0},
        "visible_ally": {"amb": 4.5, "maj": 4, "uni": 4.5, "dis": 9.0, "coh": 6.0, "norm": 3.5, "info": 4.0, "stat": 5.5, "pub": 1, "priv": 0, "gid": 5.5, "sid": 5.5, "minor": 8.5, "net": 3.0, "proof": 2.0, "alg": 1.0},
        "consistent_minority": {"amb": 5.5, "maj": 4, "uni": 5.0, "dis": 7.5, "coh": 5.5, "norm": 4.0, "info": 5.5, "stat": 5.5, "pub": 1, "priv": 0, "gid": 5.5, "sid": 5.0, "minor": 9.0, "net": 3.0, "proof": 2.5, "alg": 1.0},
        "digital_social_proof": {"amb": 6.0, "maj": 100, "uni": 8.5, "dis": 1.5, "coh": 5.0, "norm": 7.5, "info": 6.0, "stat": 5.5, "pub": 1, "priv": 0, "gid": 5.0, "sid": 5.0, "minor": 2.0, "net": 9.0, "proof": 9.2, "alg": 6.5},
        "algorithmic_amplification": {"amb": 6.5, "maj": 100, "uni": 9.0, "dis": 1.0, "coh": 5.5, "norm": 8.0, "info": 6.5, "stat": 6.0, "pub": 1, "priv": 0, "gid": 5.2, "sid": 5.4, "minor": 2.0, "net": 9.2, "proof": 9.5, "alg": 9.0},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 121):03d}"
        site_id = f"S{rng.integers(1, 41):02d}"
        independence_trait = float(np.clip(rng.normal(5.0, 1.5), 0, 10))
        affiliation_trait = float(np.clip(rng.normal(5.0, 1.5), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context = rng.choice(CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 140):03d}"
            e = effects[condition]

            ambiguity = float(np.clip(rng.normal(e["amb"], 1.0), 0, 10))
            majority_size = int(max(0, rng.normal(e["maj"], max(1, 0.15 * e["maj"]))))
            unanimity = float(np.clip(rng.normal(e["uni"], 1.0), 0, 10))
            visible_dissent = float(np.clip(rng.normal(e["dis"] + 0.15 * independence_trait, 1.0), 0, 10))
            cohesion = float(np.clip(rng.normal(e["coh"], 1.0), 0, 10))
            normative_pressure = float(np.clip(rng.normal(0.75 * e["norm"] + 0.25 * affiliation_trait, 1.0), 0, 10))
            informational_uncertainty = float(np.clip(rng.normal(e["info"], 1.0), 0, 10))
            status_strength = float(np.clip(rng.normal(e["stat"], 1.0), 0, 10))
            public_response = int(e["pub"])
            private_response = int(e["priv"])
            group_identification = float(np.clip(rng.normal(e["gid"], 1.0), 0, 10))
            social_identity_salience = float(np.clip(rng.normal(e["sid"], 1.0), 0, 10))
            minority_consistency = float(np.clip(rng.normal(e["minor"], 1.0), 0, 10))
            network_exposure = float(np.clip(rng.normal(e["net"], 1.0), 0, 10))
            social_proof_metrics = float(np.clip(rng.normal(e["proof"], 1.0), 0, 10))
            algorithmic_amplification = float(np.clip(rng.normal(e["alg"], 1.0), 0, 10))

            latent_conformity = (
                -3.0
                + 0.25 * ambiguity
                + 0.35 * normative_pressure
                + 0.28 * informational_uncertainty
                + 0.35 * unanimity
                + 0.18 * cohesion
                + 0.22 * status_strength
                + 0.45 * public_response
                - 0.40 * private_response
                + 0.18 * group_identification
                + 0.15 * social_identity_salience
                + 0.20 * social_proof_metrics
                + 0.16 * algorithmic_amplification
                - 0.45 * visible_dissent
                - 0.22 * minority_consistency
            )

            p_conform = logistic(latent_conformity)
            conformed = int(rng.random() < p_conform)

            latent_dissent = (
                -1.5
                + 0.45 * visible_dissent
                + 0.30 * minority_consistency
                + 0.25 * private_response
                - 0.32 * normative_pressure
                - 0.25 * unanimity
                - 0.20 * cohesion
                + 0.18 * independence_trait
            )
            p_dissent = logistic(latent_dissent)
            dissented = int((rng.random() < p_dissent) and not conformed)

            confidence_pre = float(np.clip(rng.normal(65, 12), 0, 100))
            confidence_post = float(np.clip(
                confidence_pre
                + 1.7 * informational_uncertainty
                + 1.2 * social_proof_metrics
                + 0.8 * status_strength
                - 1.3 * visible_dissent
                + rng.normal(0, 7),
                0,
                100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(850)
                + 0.040 * ambiguity
                + 0.035 * visible_dissent
                + 0.030 * normative_pressure
                - 0.025 * unanimity
                + rng.normal(0, 0.25)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "context": context,
                "condition": condition,
                "trial": t,
                "ambiguity": round(ambiguity, 3),
                "majority_size": majority_size,
                "unanimity": round(unanimity, 3),
                "visible_dissent": round(visible_dissent, 3),
                "cohesion": round(cohesion, 3),
                "normative_pressure": round(normative_pressure, 3),
                "informational_uncertainty": round(informational_uncertainty, 3),
                "status_strength": round(status_strength, 3),
                "public_response": public_response,
                "private_response": private_response,
                "group_identification": round(group_identification, 3),
                "social_identity_salience": round(social_identity_salience, 3),
                "minority_consistency": round(minority_consistency, 3),
                "network_exposure": round(network_exposure, 3),
                "social_proof_metrics": round(social_proof_metrics, 3),
                "algorithmic_amplification": round(algorithmic_amplification, 3),
                "conformed": conformed,
                "dissented": dissented,
                "confidence_pre": round(confidence_pre, 3),
                "confidence_post": round(confidence_post, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["confidence_shift"] = data["confidence_post"] - data["confidence_pre"]
    data["normative_influence_index"] = (
        data["normative_pressure"]
        + data["unanimity"]
        + data["cohesion"]
        + data["status_strength"]
        + data["public_response"] * 10
        + data["group_identification"]
        - data["visible_dissent"]
    ) / 6.0
    data["informational_influence_index"] = (
        data["ambiguity"]
        + data["informational_uncertainty"]
        + data["status_strength"]
        + data["social_proof_metrics"]
        - data["visible_dissent"]
    ) / 4.0
    data["digital_social_proof_index"] = (
        data["network_exposure"]
        + data["social_proof_metrics"]
        + data["algorithmic_amplification"]
    ) / 3.0
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "context"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            groups=("group_id", "nunique"),
            conformity_rate=("conformed", "mean"),
            dissent_rate=("dissented", "mean"),
            mean_confidence_shift=("confidence_shift", "mean"),
            mean_normative_influence=("normative_influence_index", "mean"),
            mean_informational_influence=("informational_influence_index", "mean"),
            mean_digital_social_proof=("digital_social_proof_index", "mean"),
            mean_response_time=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby("condition")
        .agg(
            n=("participant", "size"),
            conformity_rate=("conformed", "mean"),
            dissent_rate=("dissented", "mean"),
            mean_visible_dissent=("visible_dissent", "mean"),
            mean_unanimity=("unanimity", "mean"),
            mean_confidence_shift=("confidence_shift", "mean"),
            mean_response_time=("response_time_ms", "mean"),
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
        "conformity_model": (
            "conformed ~ ambiguity + majority_size + unanimity + visible_dissent "
            "+ cohesion + normative_pressure + informational_uncertainty "
            "+ status_strength + public_response + private_response "
            "+ group_identification + social_identity_salience + minority_consistency "
            "+ network_exposure + social_proof_metrics + algorithmic_amplification "
            "+ condition + context"
        ),
        "dissent_model": (
            "dissented ~ visible_dissent + minority_consistency + private_response "
            "+ normative_pressure + unanimity + cohesion + public_response "
            "+ condition + context"
        ),
        "confidence_shift_model": (
            "confidence_shift ~ ambiguity + informational_uncertainty + status_strength "
            "+ unanimity + visible_dissent + social_proof_metrics "
            "+ algorithmic_amplification + condition + context"
        ),
        "response_time_model": (
            "log_response_time ~ ambiguity + unanimity + visible_dissent "
            "+ normative_pressure + informational_uncertainty + conformed "
            "+ condition + context"
        ),
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name in {"conformity_model", "dissent_model"}:
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


def simulate_network_conformity(outputs: Path, n_agents: int = 500, steps: int = 30, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    scenarios = ["low_social_proof", "high_social_proof", "visible_dissent", "algorithmic_amplification", "consistent_minority"]

    for scenario in scenarios:
        beliefs = rng.normal(0, 1, size=n_agents)
        for step in range(1, steps + 1):
            mean_belief = float(np.mean(beliefs))
            if scenario == "low_social_proof":
                influence, dissent = 0.10, 0.30
            elif scenario == "high_social_proof":
                influence, dissent = 0.35, 0.10
            elif scenario == "visible_dissent":
                influence, dissent = 0.18, 0.55
            elif scenario == "algorithmic_amplification":
                influence, dissent = 0.48, 0.08
            else:
                influence, dissent = 0.20, 0.45

            minority_signal = -1.0 if scenario == "consistent_minority" else 0.0
            noise = rng.normal(0, 0.10, size=n_agents)
            beliefs = (
                (1 - influence) * beliefs
                + influence * mean_belief
                + 0.12 * minority_signal * dissent
                + noise
            )

            conformity_index = 1.0 / (1.0 + np.var(beliefs))
            rows.append({
                "scenario": scenario,
                "step": step,
                "mean_belief": float(np.mean(beliefs)),
                "belief_variance": float(np.var(beliefs)),
                "conformity_index": float(conformity_index),
                "influence_weight": influence,
                "dissent_visibility": dissent,
            })

    simulation = pd.DataFrame(rows)
    simulation.to_csv(outputs / "network_conformity_simulation.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/conformity_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=800)
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
        default_input = Path("data/conformity_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_network_conformity(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulations to: {args.outputs}")


if __name__ == "__main__":
    main()
