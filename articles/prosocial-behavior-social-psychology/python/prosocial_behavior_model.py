#!/usr/bin/env python3
"""
Prosocial behavior research model.

This script can:
1. Generate synthetic prosocial behavior data.
2. Estimate helping, donation, volunteering, cooperation, emotional-support, and response-time models.
3. Test empathy, norms, reciprocity, efficacy, cost, bystander count, responsibility, identity, trust, reputation, and institutional legitimacy effects.
4. Simulate public-goods and bystander-suppression dynamics.
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
    "baseline", "high_empathy", "strong_norm", "high_efficacy", "high_cost",
    "high_bystander", "shared_identity", "public_helping", "anonymous_helping",
    "public_goods", "organizational_citizenship", "low_institutional_trust"
]

CONTEXT_TYPES = ["laboratory", "online", "field", "organization", "public_health", "public_goods", "donation", "volunteer"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 560, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "baseline": {"empathy": 5.8, "perspective": 5.5, "norm": 5.0, "recip": 3.0, "efficacy": 6.0, "cost": 4.0, "risk": 3.0, "bystanders": 1, "identity": 3.5, "group": 4.0, "trust": 5.5, "reputation": 2.0, "legitimacy": 5.5},
        "high_empathy": {"empathy": 8.7, "perspective": 7.5, "norm": 5.5, "recip": 3.0, "efficacy": 6.5, "cost": 4.0, "risk": 3.0, "bystanders": 1, "identity": 5.5, "group": 5.5, "trust": 6.0, "reputation": 2.0, "legitimacy": 5.5},
        "strong_norm": {"empathy": 6.0, "perspective": 5.8, "norm": 8.8, "recip": 4.0, "efficacy": 6.5, "cost": 4.0, "risk": 3.0, "bystanders": 2, "identity": 4.5, "group": 6.0, "trust": 6.0, "reputation": 4.0, "legitimacy": 6.5},
        "high_efficacy": {"empathy": 6.5, "perspective": 6.0, "norm": 6.5, "recip": 3.5, "efficacy": 9.0, "cost": 4.0, "risk": 2.5, "bystanders": 3, "identity": 4.0, "group": 6.5, "trust": 6.5, "reputation": 3.0, "legitimacy": 7.5},
        "high_cost": {"empathy": 7.2, "perspective": 6.5, "norm": 6.0, "recip": 3.5, "efficacy": 6.5, "cost": 8.8, "risk": 7.5, "bystanders": 2, "identity": 4.5, "group": 5.5, "trust": 5.5, "reputation": 2.5, "legitimacy": 5.5},
        "high_bystander": {"empathy": 7.0, "perspective": 6.0, "norm": 5.5, "recip": 3.0, "efficacy": 6.0, "cost": 4.0, "risk": 3.0, "bystanders": 10, "identity": 4.0, "group": 5.0, "trust": 5.5, "reputation": 2.0, "legitimacy": 5.5},
        "shared_identity": {"empathy": 7.0, "perspective": 6.8, "norm": 7.0, "recip": 4.5, "efficacy": 7.0, "cost": 4.0, "risk": 2.5, "bystanders": 3, "identity": 8.5, "group": 8.0, "trust": 7.0, "reputation": 3.0, "legitimacy": 7.0},
        "public_helping": {"empathy": 6.2, "perspective": 5.5, "norm": 7.0, "recip": 4.0, "efficacy": 6.5, "cost": 3.5, "risk": 2.5, "bystanders": 2, "identity": 4.0, "group": 5.5, "trust": 6.0, "reputation": 8.5, "legitimacy": 6.0},
        "anonymous_helping": {"empathy": 7.5, "perspective": 6.5, "norm": 5.5, "recip": 2.0, "efficacy": 7.5, "cost": 3.5, "risk": 2.5, "bystanders": 1, "identity": 4.5, "group": 5.0, "trust": 6.0, "reputation": 0.5, "legitimacy": 6.0},
        "public_goods": {"empathy": 6.0, "perspective": 5.8, "norm": 8.0, "recip": 5.5, "efficacy": 8.8, "cost": 4.0, "risk": 2.5, "bystanders": 5, "identity": 5.5, "group": 8.0, "trust": 7.5, "reputation": 5.0, "legitimacy": 8.0},
        "organizational_citizenship": {"empathy": 6.5, "perspective": 6.8, "norm": 7.5, "recip": 5.5, "efficacy": 7.0, "cost": 3.5, "risk": 2.0, "bystanders": 4, "identity": 6.5, "group": 8.5, "trust": 7.0, "reputation": 4.0, "legitimacy": 7.5},
        "low_institutional_trust": {"empathy": 6.2, "perspective": 5.5, "norm": 5.0, "recip": 3.0, "efficacy": 5.5, "cost": 4.0, "risk": 3.0, "bystanders": 5, "identity": 4.0, "group": 4.5, "trust": 3.0, "reputation": 2.0, "legitimacy": 2.2},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        moral_identity_trait = float(np.clip(rng.normal(6.2, 1.5), 0, 10))
        prosocial_trait = float(np.clip(rng.normal(5.8, 1.4), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context_type = rng.choice(CONTEXT_TYPES)
            recipient_id = f"R{rng.integers(1, 220):03d}"
            scenario_id = f"SC{rng.integers(1, 95):03d}"
            e = effects[condition]

            empathy_score = float(np.clip(rng.normal(e["empathy"], 1.0), 0, 10))
            perspective_taking = float(np.clip(rng.normal(e["perspective"], 1.0), 0, 10))
            norm_salience = float(np.clip(rng.normal(e["norm"], 1.0), 0, 10))
            reciprocity_expectation = float(np.clip(rng.normal(e["recip"], 1.1), 0, 10))
            efficacy_belief = float(np.clip(rng.normal(e["efficacy"], 1.0), 0, 10))
            helping_cost = float(np.clip(rng.normal(e["cost"], 1.0), 0, 10))
            intervention_risk = float(np.clip(rng.normal(e["risk"], 1.0), 0, 10))
            bystander_count = int(max(0, round(rng.normal(e["bystanders"], max(1.0, e["bystanders"] * 0.15)))))
            identity_overlap = float(np.clip(rng.normal(e["identity"], 1.1), 0, 10))
            group_identification = float(np.clip(rng.normal(e["group"], 1.1), 0, 10))
            trust_level = float(np.clip(rng.normal(e["trust"], 1.0), 0, 10))
            moral_identity = float(np.clip(rng.normal(0.60 * moral_identity_trait + 0.40 * e["norm"], 1.0), 0, 10))
            reputation_visibility = float(np.clip(rng.normal(e["reputation"], 1.0), 0, 10))
            institutional_legitimacy = float(np.clip(rng.normal(e["legitimacy"], 1.0), 0, 10))

            felt_responsibility = float(np.clip(
                rng.normal(
                    3.5
                    + 0.35 * empathy_score
                    + 0.28 * norm_salience
                    + 0.24 * identity_overlap
                    + 0.22 * institutional_legitimacy
                    - 0.65 * math.log1p(bystander_count),
                    1.0
                ),
                0, 10
            ))

            latent = (
                -4.6
                + 0.26 * empathy_score
                + 0.18 * perspective_taking
                + 0.28 * norm_salience
                + 0.14 * reciprocity_expectation
                + 0.34 * efficacy_belief
                + 0.42 * felt_responsibility
                + 0.18 * identity_overlap
                + 0.16 * group_identification
                + 0.18 * trust_level
                + 0.24 * moral_identity
                + 0.10 * reputation_visibility
                + 0.22 * institutional_legitimacy
                + 0.08 * prosocial_trait
                - 0.36 * helping_cost
                - 0.28 * intervention_risk
                - 0.30 * math.log1p(bystander_count)
            )

            helping_prob = float(logistic(latent))
            helping_decision = int(rng.random() < helping_prob)

            donation_amount = float(np.clip(
                5
                + 8.0 * helping_decision
                + 3.6 * empathy_score
                + 2.4 * norm_salience
                + 2.6 * efficacy_belief
                + 1.6 * reputation_visibility
                + 1.8 * moral_identity
                - 2.6 * helping_cost
                - 1.5 * intervention_risk
                + rng.normal(0, 7),
                0, 100
            ))

            volunteer_minutes = float(np.clip(
                3
                + 8.0 * helping_decision
                + 3.0 * empathy_score
                + 2.2 * norm_salience
                + 2.0 * felt_responsibility
                + 2.0 * institutional_legitimacy
                - 2.8 * helping_cost
                - 1.6 * intervention_risk
                + rng.normal(0, 8),
                0, 180
            ))

            cooperation_contribution = float(np.clip(
                5
                + 5.0 * helping_decision
                + 3.2 * norm_salience
                + 3.2 * efficacy_belief
                + 2.5 * group_identification
                + 2.2 * trust_level
                + 2.5 * institutional_legitimacy
                + 1.5 * reciprocity_expectation
                - 2.0 * helping_cost
                + rng.normal(0, 7),
                0, 100
            ))

            emotional_support_prob = float(logistic(
                -3.0
                + 0.35 * empathy_score
                + 0.25 * perspective_taking
                + 0.18 * identity_overlap
                + 0.16 * norm_salience
                - 0.20 * intervention_risk
            ))
            emotional_support = int(rng.random() < emotional_support_prob)

            response_time_ms = int(np.clip(np.exp(
                math.log(900)
                + 0.040 * helping_cost
                + 0.035 * intervention_risk
                + 0.045 * math.log1p(bystander_count)
                - 0.035 * felt_responsibility
                - 0.030 * efficacy_belief
                + rng.normal(0, 0.20)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "recipient_id": recipient_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "condition": condition,
                "context_type": context_type,
                "trial": t,
                "empathy_score": round(empathy_score, 3),
                "perspective_taking": round(perspective_taking, 3),
                "norm_salience": round(norm_salience, 3),
                "reciprocity_expectation": round(reciprocity_expectation, 3),
                "efficacy_belief": round(efficacy_belief, 3),
                "helping_cost": round(helping_cost, 3),
                "intervention_risk": round(intervention_risk, 3),
                "bystander_count": bystander_count,
                "felt_responsibility": round(felt_responsibility, 3),
                "identity_overlap": round(identity_overlap, 3),
                "group_identification": round(group_identification, 3),
                "trust_level": round(trust_level, 3),
                "moral_identity": round(moral_identity, 3),
                "reputation_visibility": round(reputation_visibility, 3),
                "institutional_legitimacy": round(institutional_legitimacy, 3),
                "helping_decision": helping_decision,
                "donation_amount": round(donation_amount, 3),
                "volunteer_minutes": round(volunteer_minutes, 3),
                "cooperation_contribution": round(cooperation_contribution, 3),
                "emotional_support": emotional_support,
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["log_bystanders"] = np.log1p(data["bystander_count"])
    data["prosocial_motivation_index"] = (
        data["empathy_score"]
        + data["perspective_taking"]
        + data["norm_salience"]
        + data["efficacy_belief"]
        + data["felt_responsibility"]
        + data["moral_identity"]
        - data["helping_cost"]
        - data["intervention_risk"]
    ) / 6.0
    data["social_embeddedness_index"] = (
        data["identity_overlap"]
        + data["group_identification"]
        + data["trust_level"]
        + data["institutional_legitimacy"]
        + data["reciprocity_expectation"]
    ) / 5.0
    data["cost_pressure_index"] = (data["helping_cost"] + data["intervention_risk"] + data["log_bystanders"]) / 3.0
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "context_type"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            helping_rate=("helping_decision", "mean"),
            emotional_support_rate=("emotional_support", "mean"),
            mean_donation=("donation_amount", "mean"),
            mean_volunteer_minutes=("volunteer_minutes", "mean"),
            mean_cooperation=("cooperation_contribution", "mean"),
            mean_empathy=("empathy_score", "mean"),
            mean_norms=("norm_salience", "mean"),
            mean_efficacy=("efficacy_belief", "mean"),
            mean_cost=("helping_cost", "mean"),
            mean_bystanders=("bystander_count", "mean"),
            mean_responsibility=("felt_responsibility", "mean"),
            mean_identity=("identity_overlap", "mean"),
            mean_legitimacy=("institutional_legitimacy", "mean"),
            mean_prosocial_motivation=("prosocial_motivation_index", "mean"),
            mean_social_embeddedness=("social_embeddedness_index", "mean"),
        )
        .reset_index()
    )

    cost_summary = (
        data.assign(
            cost_band=pd.cut(
                data["helping_cost"],
                bins=[-0.1, 2.5, 5, 7.5, 10.1],
                labels=["low_cost", "moderate_cost", "high_cost", "very_high_cost"]
            )
        )
        .groupby(["condition", "cost_band"], observed=True)
        .agg(
            n=("participant", "size"),
            helping_rate=("helping_decision", "mean"),
            mean_donation=("donation_amount", "mean"),
            mean_cooperation=("cooperation_contribution", "mean"),
            mean_efficacy=("efficacy_belief", "mean"),
            mean_responsibility=("felt_responsibility", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    cost_summary.to_csv(outputs / "summary_by_condition_cost_band.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "helping_model": "helping_decision ~ empathy_score + perspective_taking + norm_salience + reciprocity_expectation + efficacy_belief + helping_cost + intervention_risk + log_bystanders + felt_responsibility + identity_overlap + group_identification + trust_level + moral_identity + reputation_visibility + institutional_legitimacy + condition + context_type",
        "donation_model": "donation_amount ~ empathy_score + norm_salience + efficacy_belief + helping_cost + intervention_risk + felt_responsibility + identity_overlap + moral_identity + reputation_visibility + institutional_legitimacy + helping_decision + condition + context_type",
        "cooperation_model": "cooperation_contribution ~ norm_salience + efficacy_belief + reciprocity_expectation + group_identification + trust_level + institutional_legitimacy + helping_cost + helping_decision + condition + context_type",
        "emotional_support_model": "emotional_support ~ empathy_score + perspective_taking + norm_salience + identity_overlap + intervention_risk + condition + context_type",
        "response_time_model": "log_response_time ~ empathy_score + norm_salience + efficacy_belief + helping_cost + intervention_risk + log_bystanders + felt_responsibility + helping_decision + condition + context_type",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name in ["helping_model", "emotional_support_model"]:
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


def simulate_public_goods(outputs: Path, n_cases: int = 8000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    for condition in ["weak_norm_low_trust", "strong_norm_high_trust", "high_efficacy", "low_legitimacy", "shared_identity"]:
        for _ in range(n_cases):
            empathy = 6.0 + rng.normal(0, 0.8)
            norms = {"weak_norm_low_trust": 3.0, "strong_norm_high_trust": 8.5, "high_efficacy": 7.0, "low_legitimacy": 5.0, "shared_identity": 7.0}[condition] + rng.normal(0, 0.7)
            efficacy = {"high_efficacy": 9.0, "low_legitimacy": 5.0}.get(condition, 7.0) + rng.normal(0, 0.7)
            trust = {"weak_norm_low_trust": 3.0, "strong_norm_high_trust": 8.0, "low_legitimacy": 3.0}.get(condition, 6.5) + rng.normal(0, 0.7)
            legitimacy = {"weak_norm_low_trust": 3.0, "strong_norm_high_trust": 8.0, "low_legitimacy": 2.5}.get(condition, 7.0) + rng.normal(0, 0.7)
            identity = {"shared_identity": 8.5}.get(condition, 5.0) + rng.normal(0, 0.7)
            cost = 4.0 + rng.normal(0, 0.7)

            latent = -4.0 + 0.20 * empathy + 0.35 * norms + 0.38 * efficacy + 0.25 * trust + 0.30 * legitimacy + 0.22 * identity - 0.35 * cost
            probability = float(logistic(latent))
            helping = int(rng.random() < probability)
            contribution = float(np.clip(8 + 8 * helping + 3.0 * norms + 3.2 * efficacy + 2.4 * trust + 2.8 * legitimacy + 2.0 * identity - 2.0 * cost + rng.normal(0, 7), 0, 100))

            rows.append({
                "condition": condition,
                "empathy_score": empathy,
                "norm_salience": norms,
                "efficacy_belief": efficacy,
                "trust_level": trust,
                "institutional_legitimacy": legitimacy,
                "identity_overlap": identity,
                "helping_cost": cost,
                "helping_probability": probability,
                "helping_decision": helping,
                "cooperation_contribution": contribution,
            })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby("condition")
        .agg(
            n=("condition", "size"),
            mean_norms=("norm_salience", "mean"),
            mean_efficacy=("efficacy_belief", "mean"),
            mean_legitimacy=("institutional_legitimacy", "mean"),
            helping_rate=("helping_decision", "mean"),
            mean_contribution=("cooperation_contribution", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "public_goods_prosocial_simulation.csv", index=False)
    summary.to_csv(outputs / "public_goods_prosocial_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/prosocial_behavior_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=560)
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
        default_input = Path("data/prosocial_behavior_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_public_goods(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
