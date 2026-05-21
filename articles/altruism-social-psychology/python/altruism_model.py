#!/usr/bin/env python3
"""
Altruism research model.

This script can:
1. Generate synthetic altruism data.
2. Estimate altruistic-decision, donation, volunteering, public-goods, and punishment models.
3. Test empathy, cost, recipient need, identity overlap, kinship, reciprocity, reputation, warm-glow, moral identity, and efficacy effects.
4. Simulate empathy-altruism, Hamilton-rule, reciprocal-altruism, public-goods, and altruistic-punishment dynamics.
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
    "baseline", "high_empathy", "low_empathy", "high_cost", "low_cost",
    "anonymous_helping", "public_helping", "kin_recipient", "stranger_recipient",
    "reciprocity_expected", "public_goods", "altruistic_punishment"
]

CONTEXT_TYPES = ["laboratory", "online", "field", "organization", "public_goods", "donation", "volunteer"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 520, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "baseline": {"empathy": 5.5, "distress": 4.0, "cost": 4.0, "need": 6.0, "close": 3.0, "identity": 3.2, "kin": 0.0, "recip": 2.0, "rep": 2.0, "norm": 5.0, "warm": 5.0, "eff": 6.0, "risk": 3.0},
        "high_empathy": {"empathy": 8.6, "distress": 4.8, "cost": 4.0, "need": 7.5, "close": 5.0, "identity": 6.0, "kin": 0.0, "recip": 2.5, "rep": 2.0, "norm": 6.0, "warm": 6.0, "eff": 7.0, "risk": 3.0},
        "low_empathy": {"empathy": 2.2, "distress": 3.5, "cost": 4.0, "need": 6.5, "close": 2.0, "identity": 2.0, "kin": 0.0, "recip": 2.0, "rep": 2.0, "norm": 4.0, "warm": 3.0, "eff": 5.0, "risk": 3.5},
        "high_cost": {"empathy": 7.0, "distress": 5.0, "cost": 8.5, "need": 8.0, "close": 4.0, "identity": 4.0, "kin": 0.0, "recip": 2.0, "rep": 2.0, "norm": 6.0, "warm": 6.0, "eff": 6.5, "risk": 7.5},
        "low_cost": {"empathy": 7.0, "distress": 4.5, "cost": 1.5, "need": 7.0, "close": 4.0, "identity": 4.5, "kin": 0.0, "recip": 2.5, "rep": 2.0, "norm": 6.0, "warm": 6.5, "eff": 7.0, "risk": 2.0},
        "anonymous_helping": {"empathy": 7.5, "distress": 4.0, "cost": 3.5, "need": 8.0, "close": 4.0, "identity": 4.2, "kin": 0.0, "recip": 1.5, "rep": 0.5, "norm": 5.5, "warm": 5.8, "eff": 8.0, "risk": 2.5},
        "public_helping": {"empathy": 6.2, "distress": 4.0, "cost": 3.5, "need": 7.0, "close": 3.5, "identity": 3.5, "kin": 0.0, "recip": 2.5, "rep": 8.5, "norm": 7.0, "warm": 7.5, "eff": 6.5, "risk": 2.5},
        "kin_recipient": {"empathy": 7.0, "distress": 4.8, "cost": 5.5, "need": 8.0, "close": 9.0, "identity": 8.5, "kin": 0.5, "recip": 4.5, "rep": 2.0, "norm": 6.0, "warm": 6.5, "eff": 7.0, "risk": 4.0},
        "stranger_recipient": {"empathy": 6.5, "distress": 4.5, "cost": 5.5, "need": 8.0, "close": 1.0, "identity": 2.0, "kin": 0.0, "recip": 1.5, "rep": 2.0, "norm": 5.0, "warm": 5.2, "eff": 6.5, "risk": 4.5},
        "reciprocity_expected": {"empathy": 5.8, "distress": 3.8, "cost": 4.0, "need": 5.5, "close": 4.5, "identity": 4.5, "kin": 0.0, "recip": 8.5, "rep": 5.0, "norm": 6.0, "warm": 6.0, "eff": 6.0, "risk": 3.0},
        "public_goods": {"empathy": 6.0, "distress": 3.5, "cost": 4.0, "need": 7.0, "close": 4.0, "identity": 5.0, "kin": 0.0, "recip": 4.0, "rep": 5.5, "norm": 8.0, "warm": 6.8, "eff": 8.5, "risk": 2.5},
        "altruistic_punishment": {"empathy": 5.5, "distress": 5.0, "cost": 5.0, "need": 6.0, "close": 3.0, "identity": 5.0, "kin": 0.0, "recip": 2.0, "rep": 3.0, "norm": 8.5, "warm": 5.5, "eff": 6.0, "risk": 4.0},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        moral_identity_trait = float(np.clip(rng.normal(6.2, 1.6), 0, 10))
        cooperativeness_trait = float(np.clip(rng.normal(5.8, 1.5), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context_type = rng.choice(CONTEXT_TYPES)
            recipient_id = f"R{rng.integers(1, 200):03d}"
            scenario_id = f"SC{rng.integers(1, 90):03d}"
            e = effects[condition]

            empathy_score = float(np.clip(rng.normal(e["empathy"], 1.0), 0, 10))
            personal_distress = float(np.clip(rng.normal(e["distress"], 1.1), 0, 10))
            helping_cost = float(np.clip(rng.normal(e["cost"], 1.0), 0, 10))
            recipient_need = float(np.clip(rng.normal(e["need"], 1.0), 0, 10))
            recipient_closeness = float(np.clip(rng.normal(e["close"], 1.1), 0, 10))
            identity_overlap = float(np.clip(rng.normal(e["identity"], 1.1), 0, 10))
            kinship_coefficient = float(np.clip(rng.normal(e["kin"], 0.06), 0, 1))
            reciprocity_expectation = float(np.clip(rng.normal(e["recip"], 1.1), 0, 10))
            reputation_visibility = float(np.clip(rng.normal(e["rep"], 1.0), 0, 10))
            moral_identity = float(np.clip(rng.normal(0.55 * moral_identity_trait + 0.45 * e["norm"], 1.0), 0, 10))
            social_norm_salience = float(np.clip(rng.normal(e["norm"], 1.0), 0, 10))
            warm_glow_expectation = float(np.clip(rng.normal(e["warm"] + 0.20 * empathy_score + 0.10 * moral_identity - 0.10 * helping_cost, 1.0), 0, 10))
            perceived_efficacy = float(np.clip(rng.normal(e["eff"], 1.0), 0, 10))
            intervention_risk = float(np.clip(rng.normal(e["risk"], 1.0), 0, 10))

            latent = (
                -4.2
                + 0.34 * empathy_score
                + 0.20 * recipient_need
                + 0.22 * recipient_closeness
                + 0.25 * identity_overlap
                + 1.40 * kinship_coefficient
                + 0.16 * reciprocity_expectation
                + 0.10 * reputation_visibility
                + 0.28 * moral_identity
                + 0.20 * social_norm_salience
                + 0.18 * warm_glow_expectation
                + 0.30 * perceived_efficacy
                + 0.10 * cooperativeness_trait
                - 0.36 * helping_cost
                - 0.18 * personal_distress
                - 0.24 * intervention_risk
            )

            altruism_prob = float(logistic(latent))
            altruistic_decision = int(rng.random() < altruism_prob)

            donation_amount = float(np.clip(
                4
                + 8.5 * altruistic_decision
                + 4.2 * empathy_score
                + 2.2 * moral_identity
                + 2.0 * perceived_efficacy
                + 1.7 * warm_glow_expectation
                + 1.2 * reputation_visibility
                - 3.0 * helping_cost
                - 1.5 * intervention_risk
                + rng.normal(0, 7),
                0, 100
            ))

            time_volunteered_minutes = float(np.clip(
                5
                + 7.0 * altruistic_decision
                + 4.0 * empathy_score
                + 2.0 * identity_overlap
                + 2.4 * moral_identity
                + 2.0 * perceived_efficacy
                - 2.8 * helping_cost
                - 1.8 * intervention_risk
                + rng.normal(0, 8),
                0, 180
            ))

            punishment_latent = (
                -5.5
                + 0.22 * social_norm_salience
                + 0.35 * moral_identity
                + 0.16 * identity_overlap
                + 0.25 * personal_distress
                + 0.20 * perceived_efficacy
                - 0.32 * helping_cost
                - 0.20 * intervention_risk
                + 1.2 * (condition == "altruistic_punishment")
            )
            punishment_prob = float(logistic(punishment_latent))
            altruistic_punishment = int(rng.random() < punishment_prob)

            punishment_cost = float(np.clip(
                altruistic_punishment * (4 + 2.2 * moral_identity + 1.8 * social_norm_salience - 1.5 * helping_cost + rng.normal(0, 4)),
                0, 100
            ))

            public_goods_contribution = float(np.clip(
                5
                + 5.0 * altruistic_decision
                + 3.5 * social_norm_salience
                + 3.0 * perceived_efficacy
                + 2.8 * moral_identity
                + 1.8 * warm_glow_expectation
                + 1.4 * reciprocity_expectation
                - 2.2 * helping_cost
                + 10.0 * (condition == "public_goods")
                + rng.normal(0, 7),
                0, 100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(950)
                + 0.04 * helping_cost
                + 0.03 * personal_distress
                + 0.03 * intervention_risk
                - 0.03 * empathy_score
                - 0.03 * perceived_efficacy
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
                "personal_distress": round(personal_distress, 3),
                "helping_cost": round(helping_cost, 3),
                "recipient_need": round(recipient_need, 3),
                "recipient_closeness": round(recipient_closeness, 3),
                "identity_overlap": round(identity_overlap, 3),
                "kinship_coefficient": round(kinship_coefficient, 3),
                "reciprocity_expectation": round(reciprocity_expectation, 3),
                "reputation_visibility": round(reputation_visibility, 3),
                "moral_identity": round(moral_identity, 3),
                "social_norm_salience": round(social_norm_salience, 3),
                "warm_glow_expectation": round(warm_glow_expectation, 3),
                "perceived_efficacy": round(perceived_efficacy, 3),
                "intervention_risk": round(intervention_risk, 3),
                "altruistic_decision": altruistic_decision,
                "donation_amount": round(donation_amount, 3),
                "time_volunteered_minutes": round(time_volunteered_minutes, 3),
                "altruistic_punishment": altruistic_punishment,
                "punishment_cost": round(punishment_cost, 3),
                "public_goods_contribution": round(public_goods_contribution, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["other_regarding_weight"] = (
        data["empathy_score"]
        + data["recipient_need"]
        + data["identity_overlap"]
        + data["moral_identity"]
        + data["perceived_efficacy"]
        - data["helping_cost"]
        - data["intervention_risk"]
    ) / 5.0
    data["egoistic_reward_index"] = (
        data["reciprocity_expectation"]
        + data["reputation_visibility"]
        + data["warm_glow_expectation"]
    ) / 3.0
    data["cost_pressure_index"] = (
        data["helping_cost"]
        + data["intervention_risk"]
        + data["personal_distress"]
    ) / 3.0
    data["inclusive_fitness_score"] = data["kinship_coefficient"] * data["recipient_need"] - data["helping_cost"] / 10.0
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
            altruism_rate=("altruistic_decision", "mean"),
            punishment_rate=("altruistic_punishment", "mean"),
            mean_donation=("donation_amount", "mean"),
            mean_volunteer_minutes=("time_volunteered_minutes", "mean"),
            mean_public_goods=("public_goods_contribution", "mean"),
            mean_empathy=("empathy_score", "mean"),
            mean_cost=("helping_cost", "mean"),
            mean_recipient_need=("recipient_need", "mean"),
            mean_identity_overlap=("identity_overlap", "mean"),
            mean_moral_identity=("moral_identity", "mean"),
            mean_efficacy=("perceived_efficacy", "mean"),
            mean_other_regarding_weight=("other_regarding_weight", "mean"),
            mean_egoistic_reward=("egoistic_reward_index", "mean"),
            mean_response_time=("response_time_ms", "mean"),
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
            altruism_rate=("altruistic_decision", "mean"),
            mean_donation=("donation_amount", "mean"),
            mean_public_goods=("public_goods_contribution", "mean"),
            mean_empathy=("empathy_score", "mean"),
            mean_efficacy=("perceived_efficacy", "mean"),
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
        "altruistic_decision_model": "altruistic_decision ~ empathy_score + personal_distress + helping_cost + recipient_need + recipient_closeness + identity_overlap + kinship_coefficient + reciprocity_expectation + reputation_visibility + moral_identity + social_norm_salience + warm_glow_expectation + perceived_efficacy + intervention_risk + condition + context_type",
        "donation_model": "donation_amount ~ empathy_score + helping_cost + recipient_need + recipient_closeness + identity_overlap + reciprocity_expectation + reputation_visibility + moral_identity + social_norm_salience + warm_glow_expectation + perceived_efficacy + intervention_risk + altruistic_decision + condition + context_type",
        "public_goods_model": "public_goods_contribution ~ social_norm_salience + perceived_efficacy + moral_identity + reciprocity_expectation + reputation_visibility + warm_glow_expectation + helping_cost + altruistic_decision + condition + context_type",
        "punishment_model": "altruistic_punishment ~ social_norm_salience + moral_identity + identity_overlap + personal_distress + perceived_efficacy + punishment_cost + helping_cost + intervention_risk + condition + context_type",
        "response_time_model": "log_response_time ~ empathy_score + helping_cost + personal_distress + recipient_need + perceived_efficacy + intervention_risk + altruistic_decision + condition + context_type",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name in ["altruistic_decision_model", "punishment_model"]:
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


def simulate_altruism(outputs: Path, n_cases: int = 8000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    for condition in ["high_empathy", "high_cost", "anonymous_helping", "public_helping", "kin_recipient", "public_goods", "altruistic_punishment"]:
        for _ in range(n_cases):
            empathy = {"high_empathy": 8.5, "high_cost": 7.0, "anonymous_helping": 7.5, "public_helping": 6.2, "kin_recipient": 7.0, "public_goods": 6.0, "altruistic_punishment": 5.5}[condition] + rng.normal(0, 0.8)
            cost = {"high_empathy": 4.0, "high_cost": 8.5, "anonymous_helping": 3.5, "public_helping": 3.5, "kin_recipient": 5.5, "public_goods": 4.0, "altruistic_punishment": 5.0}[condition] + rng.normal(0, 0.8)
            need = 7.0 + rng.normal(0, 0.8)
            identity = {"kin_recipient": 8.5, "public_goods": 5.0, "altruistic_punishment": 5.0}.get(condition, 4.0) + rng.normal(0, 0.8)
            kin = 0.5 if condition == "kin_recipient" else 0.0
            reciprocity = 4.0 if condition == "public_goods" else 2.0
            reputation = 8.0 if condition == "public_helping" else 0.5 if condition == "anonymous_helping" else 3.0
            moral = 7.0 + rng.normal(0, 1.0)
            norms = 8.0 if condition in ["public_goods", "altruistic_punishment"] else 5.5
            warm = 6.0 + rng.normal(0, 0.8)
            efficacy = 8.5 if condition == "public_goods" else 6.5
            risk = {"high_cost": 7.5, "altruistic_punishment": 4.0}.get(condition, 3.0)

            latent = -4.2 + 0.34 * empathy + 0.20 * need + 0.25 * identity + 1.4 * kin + 0.16 * reciprocity + 0.10 * reputation + 0.28 * moral + 0.20 * norms + 0.18 * warm + 0.30 * efficacy - 0.36 * cost - 0.24 * risk
            prob = float(logistic(latent))
            decision = int(rng.random() < prob)
            donation = np.clip(4 + 8.5 * decision + 4.2 * empathy + 2.2 * moral + 2.0 * efficacy + 1.7 * warm + 1.2 * reputation - 3.0 * cost - 1.5 * risk + rng.normal(0, 7), 0, 100)

            rows.append({
                "condition": condition,
                "empathy_score": empathy,
                "helping_cost": cost,
                "recipient_need": need,
                "identity_overlap": identity,
                "kinship_coefficient": kin,
                "reciprocity_expectation": reciprocity,
                "reputation_visibility": reputation,
                "moral_identity": moral,
                "social_norm_salience": norms,
                "warm_glow_expectation": warm,
                "perceived_efficacy": efficacy,
                "intervention_risk": risk,
                "altruism_probability": prob,
                "altruistic_decision": decision,
                "donation_amount": donation,
            })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby("condition")
        .agg(
            n=("condition", "size"),
            mean_empathy=("empathy_score", "mean"),
            mean_cost=("helping_cost", "mean"),
            mean_probability=("altruism_probability", "mean"),
            altruism_rate=("altruistic_decision", "mean"),
            mean_donation=("donation_amount", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "altruism_simulation.csv", index=False)
    summary.to_csv(outputs / "altruism_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/altruism_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=520)
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
        default_input = Path("data/altruism_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_altruism(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
