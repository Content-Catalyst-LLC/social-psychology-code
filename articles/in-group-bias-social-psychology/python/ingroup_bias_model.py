#!/usr/bin/env python3
"""
In-group bias research model.

This script can:
1. Generate synthetic in-group bias trial data.
2. Estimate trust, fairness, allocation, moral-blame, forgiveness, punishment,
   cooperation, and response-time models.
3. Simulate repeated institutional favoritism and minimal-group allocation.
4. Save researcher-readable summaries to outputs/.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except Exception:
    NETWORKX_AVAILABLE = False

try:
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False


CONDITIONS = [
    "control", "minimal_group", "identity_salience", "threat_prime",
    "fairness_norm", "superordinate_identity", "contact_prime", "scarcity", "abundance"
]
CONTEXTS = ["hiring", "promotion", "grading", "discipline", "resource", "trust_game", "moral_vignette", "minimal_group", "political_judgment"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 500, trials_per_participant: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"identity": 0.0, "threat": 0.0, "norm": 0.0, "fairness": 0.0, "superordinate": 0.0, "scarcity": 0.0},
        "minimal_group": {"identity": 1.0, "threat": 0.0, "norm": 0.3, "fairness": 0.0, "superordinate": 0.0, "scarcity": 0.0},
        "identity_salience": {"identity": 2.8, "threat": 0.4, "norm": 1.0, "fairness": -0.1, "superordinate": 0.0, "scarcity": 0.0},
        "threat_prime": {"identity": 2.2, "threat": 3.0, "norm": 1.0, "fairness": -0.3, "superordinate": 0.0, "scarcity": 0.5},
        "fairness_norm": {"identity": 0.2, "threat": -0.4, "norm": -1.0, "fairness": 2.6, "superordinate": 0.0, "scarcity": 0.0},
        "superordinate_identity": {"identity": -1.0, "threat": -0.7, "norm": -0.6, "fairness": 1.4, "superordinate": 2.8, "scarcity": 0.0},
        "contact_prime": {"identity": -0.4, "threat": -0.8, "norm": -0.4, "fairness": 1.2, "superordinate": 0.8, "scarcity": 0.0},
        "scarcity": {"identity": 1.6, "threat": 1.8, "norm": 1.0, "fairness": -0.6, "superordinate": 0.0, "scarcity": 2.4},
        "abundance": {"identity": -0.2, "threat": -0.6, "norm": -0.2, "fairness": 1.0, "superordinate": 0.6, "scarcity": -1.4},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        baseline_identification = rng.normal(6.0, 1.2)
        fairness_orientation = rng.normal(0, 0.55)
        threat_sensitivity = rng.normal(0, 0.55)
        loyalty_orientation = rng.normal(0, 0.55)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            ce = condition_effects[condition]
            ingroup_target = int(rng.random() < 0.5)
            target_relation = "ingroup" if ingroup_target == 1 else "outgroup"
            context = rng.choice(CONTEXTS)

            group_identification = float(np.clip(baseline_identification + 0.35 * ce["identity"] + rng.normal(0, 0.75), 0, 10))
            identity_salience = float(np.clip(rng.normal(4.0 + ce["identity"] + 0.25 * group_identification, 1.0), 0, 10))
            perceived_threat = float(np.clip(rng.normal(3.2 + ce["threat"] + 0.35 * threat_sensitivity + 0.25 * (1 - ingroup_target), 1.0), 0, 10))
            norm_strength = float(np.clip(rng.normal(4.0 + ce["norm"] + 0.25 * group_identification + 0.30 * loyalty_orientation - 0.35 * ce["fairness"], 1.0), 0, 10))
            status_asymmetry = float(np.clip(rng.normal(4.0 + 0.35 * perceived_threat + 0.35 * ce["scarcity"], 1.2), 0, 10))

            ingroup_advantage = (
                ingroup_target
                * (0.35 * identity_salience + 0.25 * perceived_threat + 0.22 * norm_strength + 0.20 * group_identification)
                - (1 - ingroup_target) * (0.18 * perceived_threat + 0.12 * identity_salience)
            )

            fairness_dampener = 0.35 * ce["fairness"] + 0.25 * ce["superordinate"] + 0.28 * fairness_orientation

            trust_rating = float(np.clip(rng.normal(5.0 + 0.55 * ingroup_advantage - 0.35 * fairness_dampener + 0.20 * ingroup_target, 1.0), 0, 10))
            fairness_rating = float(np.clip(rng.normal(5.2 + 0.40 * ingroup_advantage - 0.55 * fairness_dampener + 0.10 * ingroup_target, 1.0), 0, 10))
            competence_rating = float(np.clip(rng.normal(5.4 + 0.22 * ingroup_advantage - 0.20 * fairness_dampener, 0.9), 0, 10))
            warmth_rating = float(np.clip(rng.normal(5.0 + 0.48 * ingroup_advantage - 0.35 * fairness_dampener, 0.9), 0, 10))
            empathy_rating = float(np.clip(rng.normal(5.0 + 0.45 * ingroup_advantage - 0.40 * fairness_dampener - 0.15 * perceived_threat, 0.9), 0, 10))

            # Same negative act, but judged through group relation.
            moral_blame = float(np.clip(rng.normal(5.2 - 0.45 * ingroup_advantage + 0.25 * perceived_threat - 0.25 * fairness_dampener, 1.0), 0, 10))
            moral_forgiveness = float(np.clip(rng.normal(4.8 + 0.50 * ingroup_advantage - 0.25 * perceived_threat + 0.20 * fairness_dampener, 1.0), 0, 10))
            punishment_severity = float(np.clip(rng.normal(5.0 - 0.42 * ingroup_advantage + 0.28 * perceived_threat - 0.20 * fairness_dampener, 1.0), 0, 10))

            reward_allocation = float(np.clip(rng.normal(52 + 4.2 * ingroup_advantage - 2.8 * fairness_dampener + 0.8 * (condition == "scarcity"), 8), 0, 100))
            resource_allocation = float(np.clip(rng.normal(52 + 4.8 * ingroup_advantage - 3.2 * fairness_dampener + 1.2 * (condition == "scarcity"), 8), 0, 100))

            cooperation_latent = -1.5 + 0.32 * trust_rating + 0.12 * warmth_rating + 0.10 * empathy_rating - 0.12 * perceived_threat
            cooperation_choice = int(rng.random() < logistic(cooperation_latent - 2.4))

            response_time_ms = int(np.clip(np.exp(
                math.log(1050)
                + 0.05 * perceived_threat
                + 0.04 * abs(trust_rating - fairness_rating)
                + 0.08 * (abs(resource_allocation - 50) < 4)
                - 0.03 * identity_salience
                + rng.normal(0, 0.17)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "trial": trial,
                "target_group_relation": target_relation,
                "ingroup_target": ingroup_target,
                "group_identification": round(group_identification, 3),
                "identity_salience": round(identity_salience, 3),
                "perceived_threat": round(perceived_threat, 3),
                "norm_strength": round(norm_strength, 3),
                "status_asymmetry": round(status_asymmetry, 3),
                "trust_rating": round(trust_rating, 3),
                "fairness_rating": round(fairness_rating, 3),
                "competence_rating": round(competence_rating, 3),
                "warmth_rating": round(warmth_rating, 3),
                "empathy_rating": round(empathy_rating, 3),
                "moral_blame": round(moral_blame, 3),
                "moral_forgiveness": round(moral_forgiveness, 3),
                "punishment_severity": round(punishment_severity, 3),
                "reward_allocation": round(reward_allocation, 3),
                "resource_allocation": round(resource_allocation, 3),
                "cooperation_choice": cooperation_choice,
                "response_time_ms": response_time_ms,
                "institutional_context": context,
            })

    return pd.DataFrame(rows)


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)

    relation_summary = (
        df.groupby(["condition", "target_group_relation"])
        .agg(
            n=("trust_rating", "size"),
            participants=("participant", "nunique"),
            mean_trust=("trust_rating", "mean"),
            mean_fairness=("fairness_rating", "mean"),
            mean_competence=("competence_rating", "mean"),
            mean_warmth=("warmth_rating", "mean"),
            mean_empathy=("empathy_rating", "mean"),
            mean_blame=("moral_blame", "mean"),
            mean_forgiveness=("moral_forgiveness", "mean"),
            mean_punishment=("punishment_severity", "mean"),
            mean_reward=("reward_allocation", "mean"),
            mean_resource=("resource_allocation", "mean"),
            cooperation_rate=("cooperation_choice", "mean"),
            mean_response_time_ms=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    wide = relation_summary.pivot(index="condition", columns="target_group_relation")
    bias_summary = pd.DataFrame({"condition": relation_summary["condition"].unique()})
    records = []
    for condition, g in relation_summary.groupby("condition"):
        ing = g[g["target_group_relation"] == "ingroup"]
        out = g[g["target_group_relation"] == "outgroup"]
        if len(ing) and len(out):
            ing = ing.iloc[0]
            out = out.iloc[0]
            records.append({
                "condition": condition,
                "trust_bias": ing["mean_trust"] - out["mean_trust"],
                "fairness_bias": ing["mean_fairness"] - out["mean_fairness"],
                "empathy_bias": ing["mean_empathy"] - out["mean_empathy"],
                "allocation_bias": ing["mean_resource"] - out["mean_resource"],
                "moral_blame_asymmetry": out["mean_blame"] - ing["mean_blame"],
                "punishment_asymmetry": out["mean_punishment"] - ing["mean_punishment"],
                "cooperation_bias": ing["cooperation_rate"] - out["cooperation_rate"],
            })
    bias_summary = pd.DataFrame(records)

    context_summary = (
        df.groupby(["institutional_context", "target_group_relation"])
        .agg(
            n=("trust_rating", "size"),
            mean_trust=("trust_rating", "mean"),
            mean_resource=("resource_allocation", "mean"),
            mean_blame=("moral_blame", "mean"),
            mean_punishment=("punishment_severity", "mean"),
        )
        .reset_index()
    )

    relation_summary.to_csv(outputs / "summary_by_condition_target_relation.csv", index=False)
    bias_summary.to_csv(outputs / "bias_differentials_by_condition.csv", index=False)
    context_summary.to_csv(outputs / "summary_by_context_target_relation.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = df.copy()
    data["log_response_time"] = np.log(data["response_time_ms"])

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    model_text = []

    formulas = {
        "trust_model": "trust_rating ~ ingroup_target * identity_salience + group_identification + perceived_threat + norm_strength + status_asymmetry + condition + institutional_context",
        "fairness_model": "fairness_rating ~ ingroup_target * identity_salience + group_identification + perceived_threat + norm_strength + status_asymmetry + condition + institutional_context",
        "allocation_model": "resource_allocation ~ ingroup_target * identity_salience + group_identification + perceived_threat + norm_strength + status_asymmetry + condition + institutional_context",
        "moral_blame_model": "moral_blame ~ ingroup_target * identity_salience + group_identification + perceived_threat + norm_strength + status_asymmetry + condition + institutional_context",
        "punishment_model": "punishment_severity ~ ingroup_target * identity_salience + group_identification + perceived_threat + norm_strength + status_asymmetry + condition + institutional_context",
        "cooperation_model": "cooperation_choice ~ ingroup_target * identity_salience + trust_rating + perceived_threat + norm_strength + condition + institutional_context",
        "response_time_model": "log_response_time ~ ingroup_target * identity_salience + perceived_threat + norm_strength + condition + institutional_context",
    }

    coefficient_frames = []
    for name, formula in formulas.items():
        if name == "cooperation_model":
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


def simulate_institutional_accumulation(outputs: Path, n_decisions: int = 5000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    contexts = rng.choice(CONTEXTS, size=n_decisions)
    ingroup = rng.integers(0, 2, size=n_decisions)
    identity_salience = rng.uniform(0, 10, size=n_decisions)
    threat = rng.uniform(0, 10, size=n_decisions)
    fairness_norm = rng.uniform(0, 10, size=n_decisions)

    score = (
        50
        + ingroup * (1.8 + 0.30 * identity_salience + 0.22 * threat)
        - (1 - ingroup) * (0.35 * threat)
        - 0.45 * fairness_norm
        + rng.normal(0, 5, size=n_decisions)
    )
    selected = score >= np.quantile(score, 0.70)

    sim = pd.DataFrame({
        "decision_id": np.arange(1, n_decisions + 1),
        "institutional_context": contexts,
        "ingroup_target": ingroup,
        "identity_salience": identity_salience,
        "perceived_threat": threat,
        "fairness_norm": fairness_norm,
        "selection_score": score,
        "selected": selected.astype(int),
    })

    summary = (
        sim.groupby(["institutional_context", "ingroup_target"])
        .agg(
            n=("selected", "size"),
            selection_rate=("selected", "mean"),
            mean_score=("selection_score", "mean"),
            mean_threat=("perceived_threat", "mean"),
            mean_identity_salience=("identity_salience", "mean"),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "institutional_accumulation_simulation.csv", index=False)
    summary.to_csv(outputs / "institutional_accumulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/ingroup_bias_trials.csv"))
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
        default_input = Path("data/ingroup_bias_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_accumulation(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
