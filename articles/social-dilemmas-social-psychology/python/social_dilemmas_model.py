#!/usr/bin/env python3
"""
Social dilemmas research model.

This script can:
1. Generate synthetic public-goods and commons-dilemma data.
2. Estimate contribution, extraction, payoff, trust, fairness, and response-time models.
3. Compute free-riding, cooperation, institutional-effectiveness, and welfare indices.
4. Simulate common-pool resource depletion and institutional enforcement.
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
    "baseline", "communication", "norm_salient", "monitoring", "sanction",
    "legitimacy_high", "legitimacy_low", "identity_shared", "asymmetry",
    "polycentric"
]
DILEMMA_TYPES = ["public_goods", "commons", "intergenerational", "threshold_public_good", "nested_public_good"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_groups: int = 160, group_size: int = 6, rounds_per_group: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "baseline": {"trust": 0, "norm": 0, "enforce": 0, "legit": 0, "monitor": 0, "identity": 0, "asym": 0},
        "communication": {"trust": 1.6, "norm": 1.4, "enforce": 0, "legit": 0.6, "monitor": 0.5, "identity": 0.5, "asym": 0},
        "norm_salient": {"trust": 0.8, "norm": 2.4, "enforce": 0.5, "legit": 0.8, "monitor": 0.5, "identity": 0.4, "asym": 0},
        "monitoring": {"trust": 0.4, "norm": 0.6, "enforce": 1.2, "legit": 0.4, "monitor": 3.2, "identity": 0, "asym": 0},
        "sanction": {"trust": 0.2, "norm": 0.8, "enforce": 3.0, "legit": 0.6, "monitor": 2.5, "identity": 0, "asym": 0},
        "legitimacy_high": {"trust": 1.2, "norm": 1.2, "enforce": 1.2, "legit": 3.2, "monitor": 1.2, "identity": 0.4, "asym": 0},
        "legitimacy_low": {"trust": -1.4, "norm": -0.8, "enforce": 1.5, "legit": -3.0, "monitor": 1.5, "identity": 0, "asym": 0.7},
        "identity_shared": {"trust": 1.8, "norm": 1.6, "enforce": 0.4, "legit": 1.0, "monitor": 0.5, "identity": 3.2, "asym": 0},
        "asymmetry": {"trust": -0.8, "norm": -0.5, "enforce": 0.6, "legit": -0.8, "monitor": 0.5, "identity": 0, "asym": 2.6},
        "polycentric": {"trust": 1.1, "norm": 1.3, "enforce": 1.8, "legit": 2.4, "monitor": 2.0, "identity": 1.0, "asym": 0.2},
    }

    for g in range(1, n_groups + 1):
        group_id = f"G{g:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        condition = rng.choice(CONDITIONS)
        dilemma_type = rng.choice(DILEMMA_TYPES, p=[0.45, 0.30, 0.10, 0.10, 0.05])
        e = effects[condition]
        resource_stock = float(rng.uniform(80, 120))
        mpcr = 0.35 if dilemma_type in ["public_goods", "threshold_public_good", "nested_public_good"] else 0.0

        for round_number in range(1, rounds_per_group + 1):
            participant_rows = []
            contributions = []
            extractions = []

            for member in range(1, group_size + 1):
                participant = f"P{g:04d}_{member:02d}"
                endowment = float(20 + rng.normal(0, 1.2))
                if condition == "asymmetry":
                    endowment += rng.normal(0, 5.0)
                endowment = max(5.0, endowment)

                trust = float(np.clip(rng.normal(5.0 + e["trust"] - 0.06 * (round_number - 1), 1.0), 0, 10))
                norm = float(np.clip(rng.normal(4.8 + e["norm"], 1.0), 0, 10))
                enforcement = float(np.clip(rng.normal(2.0 + e["enforce"], 1.0), 0, 10))
                legitimacy = float(np.clip(rng.normal(5.0 + e["legit"], 1.0), 0, 10))
                monitoring = float(np.clip(rng.normal(2.5 + e["monitor"], 1.0), 0, 10))
                sanction_probability = float(np.clip(0.05 + 0.07 * enforcement + 0.05 * monitoring, 0, 1))
                sanction_severity = float(np.clip(rng.normal(1.0 + 0.40 * enforcement, 1.0), 0, 10))
                reciprocity = float(np.clip(rng.normal(5.0 + 0.35 * trust + 0.20 * norm + 0.10 * e["identity"], 1.0), 0, 10))
                fairness = float(np.clip(rng.normal(5.0 + 0.40 * legitimacy - 0.25 * e["asym"], 1.0), 0, 10))
                institutional_effect = monitoring * sanction_probability * sanction_severity * (legitimacy / 10.0)

                if dilemma_type == "commons":
                    extraction_pressure = (
                        7.0
                        - 0.28 * trust
                        - 0.22 * norm
                        - 0.20 * institutional_effect
                        - 0.15 * legitimacy
                        + rng.normal(0, 1.0)
                    )
                    extraction = float(np.clip(extraction_pressure, 0, min(12, resource_stock / group_size)))
                    contribution = 0.0
                else:
                    contribution_propensity = logistic(
                        -2.0
                        + 0.25 * trust
                        + 0.24 * norm
                        + 0.17 * enforcement
                        + 0.22 * legitimacy
                        + 0.18 * reciprocity
                        + 0.12 * e["identity"]
                        - 0.16 * e["asym"]
                        - 0.08 * (round_number - 1)
                    )
                    contribution = float(np.clip(endowment * contribution_propensity + rng.normal(0, 1.2), 0, endowment))
                    extraction = 0.0

                contributions.append(contribution)
                extractions.append(extraction)

                participant_rows.append({
                    "participant": participant,
                    "group_id": group_id,
                    "site_id": site_id,
                    "condition": condition,
                    "dilemma_type": dilemma_type,
                    "round": round_number,
                    "endowment": round(endowment, 3),
                    "contribution": round(contribution, 3),
                    "extraction": round(extraction, 3),
                    "mpcr": mpcr,
                    "trust_score": round(trust, 3),
                    "norm_salience": round(norm, 3),
                    "enforcement_signal": round(enforcement, 3),
                    "fairness_score": round(fairness, 3),
                    "institutional_legitimacy": round(legitimacy, 3),
                    "monitoring_strength": round(monitoring, 3),
                    "sanction_probability": round(sanction_probability, 3),
                    "sanction_severity": round(sanction_severity, 3),
                    "reciprocity_expectation": round(reciprocity, 3),
                })

            total_contribution = sum(contributions)
            total_extraction = sum(extractions)
            if dilemma_type == "commons":
                regeneration = max(0, 0.12 * resource_stock * (1 - resource_stock / 150))
                resource_stock = max(0, resource_stock + regeneration - total_extraction)
                group_welfare = sum(20 - np.array(extractions)) + 0.35 * resource_stock
            else:
                group_return = mpcr * total_contribution
                group_welfare = sum([r["endowment"] - r["contribution"] + group_return for r in participant_rows])

            for r in participant_rows:
                if dilemma_type == "commons":
                    sanction = 0
                    if rng.random() < r["sanction_probability"] and r["extraction"] > np.mean(extractions):
                        sanction = r["sanction_severity"]
                    individual_payoff = r["endowment"] + r["extraction"] - sanction
                else:
                    sanction = 0
                    if rng.random() < r["sanction_probability"] and r["contribution"] < np.mean(contributions):
                        sanction = r["sanction_severity"]
                    individual_payoff = r["endowment"] - r["contribution"] + mpcr * total_contribution - sanction

                response_time_ms = int(np.clip(np.exp(
                    math.log(1000)
                    + 0.04 * abs(r["trust_score"] - 5)
                    + 0.03 * abs(r["fairness_score"] - 5)
                    + rng.normal(0, 0.18)
                ), 150, 60000))

                r["resource_stock"] = round(resource_stock, 3)
                r["group_welfare"] = round(group_welfare, 3)
                r["individual_payoff"] = round(individual_payoff, 3)
                r["response_time_ms"] = response_time_ms
                rows.append(r)

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["free_riding_index"] = np.where(
        data["endowment"] > 0,
        (data["endowment"] - data["contribution"]) / data["endowment"],
        np.nan,
    )
    data["institutional_effectiveness"] = (
        data["monitoring_strength"]
        * data["sanction_probability"]
        * data["sanction_severity"]
        * (data["institutional_legitimacy"] / 10.0)
    )
    data["cooperation_score"] = np.where(
        data["dilemma_type"].eq("commons"),
        -data["extraction"],
        data["contribution"],
    )
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "dilemma_type", "round"])
        .agg(
            n=("participant", "size"),
            groups=("group_id", "nunique"),
            mean_contribution=("contribution", "mean"),
            mean_extraction=("extraction", "mean"),
            mean_free_riding=("free_riding_index", "mean"),
            mean_trust=("trust_score", "mean"),
            mean_norm_salience=("norm_salience", "mean"),
            mean_enforcement=("enforcement_signal", "mean"),
            mean_legitimacy=("institutional_legitimacy", "mean"),
            mean_group_welfare=("group_welfare", "mean"),
            mean_resource_stock=("resource_stock", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby(["condition", "dilemma_type"])
        .agg(
            n=("participant", "size"),
            mean_contribution=("contribution", "mean"),
            mean_extraction=("extraction", "mean"),
            mean_free_riding=("free_riding_index", "mean"),
            mean_payoff=("individual_payoff", "mean"),
            mean_group_welfare=("group_welfare", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_type_round.csv", index=False)
    condition_summary.to_csv(outputs / "summary_by_condition_type.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    model_text = []
    coefficient_frames = []

    public_goods = data[data["dilemma_type"].ne("commons")].copy()
    commons = data[data["dilemma_type"].eq("commons")].copy()

    ols_formulas = {}

    if len(public_goods) > 0:
        ols_formulas["contribution_model"] = (
            public_goods,
            "contribution ~ round + trust_score + norm_salience + enforcement_signal + "
            "fairness_score + institutional_legitimacy + monitoring_strength + "
            "sanction_probability + sanction_severity + reciprocity_expectation + condition"
        )

    if len(commons) > 0:
        ols_formulas["extraction_model"] = (
            commons,
            "extraction ~ round + trust_score + norm_salience + enforcement_signal + "
            "fairness_score + institutional_legitimacy + monitoring_strength + "
            "sanction_probability + sanction_severity + reciprocity_expectation + resource_stock + condition"
        )

    ols_formulas["payoff_model"] = (
        data,
        "individual_payoff ~ contribution + extraction + trust_score + norm_salience + "
        "institutional_legitimacy + institutional_effectiveness + condition + dilemma_type"
    )

    ols_formulas["welfare_model"] = (
        data,
        "group_welfare ~ contribution + extraction + trust_score + norm_salience + "
        "institutional_legitimacy + institutional_effectiveness + condition + dilemma_type"
    )

    ols_formulas["response_time_model"] = (
        data[data["response_time_ms"] >= 150],
        "log_response_time ~ round + trust_score + norm_salience + enforcement_signal + "
        "fairness_score + institutional_legitimacy + condition + dilemma_type"
    )

    for name, (model_data, formula) in ols_formulas.items():
        model = smf.ols(formula, data=model_data).fit(
            cov_type="cluster", cov_kwds={"groups": model_data["participant"]}
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


def simulate_commons(outputs: Path, n_groups: int = 250, periods: int = 50, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    resource = rng.uniform(70, 120, n_groups)
    monitoring = rng.uniform(1, 9, n_groups)
    legitimacy = rng.uniform(1, 9, n_groups)
    sanction = rng.uniform(0, 8, n_groups)
    norm = rng.uniform(1, 9, n_groups)

    for t in range(1, periods + 1):
        extraction = np.clip(
            8.5 - 0.25 * monitoring - 0.25 * legitimacy - 0.25 * sanction - 0.25 * norm
            + rng.normal(0, 1.0, n_groups),
            0,
            15,
        )

        total_extraction = 6 * extraction
        regeneration = np.maximum(0, 0.12 * resource * (1 - resource / 150))
        resource = np.clip(resource + regeneration - total_extraction, 0, 150)

        for i in range(n_groups):
            rows.append({
                "group_id": f"G{i+1:04d}",
                "period": t,
                "resource_stock": resource[i],
                "mean_extraction": extraction[i],
                "monitoring": monitoring[i],
                "legitimacy": legitimacy[i],
                "sanction": sanction[i],
                "norm_salience": norm[i],
            })

    sim = pd.DataFrame(rows)
    summary = (
        sim.groupby("period")
        .agg(
            mean_resource_stock=("resource_stock", "mean"),
            mean_extraction=("mean_extraction", "mean"),
            depleted_rate=("resource_stock", lambda x: np.mean(x <= 1)),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "commons_simulation.csv", index=False)
    summary.to_csv(outputs / "commons_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/social_dilemmas_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--groups", type=int, default=160)
    parser.add_argument("--group-size", type=int, default=6)
    parser.add_argument("--rounds", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulate:
        df = generate_dataset(n_groups=args.groups, group_size=args.group_size, rounds_per_group=args.rounds, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote simulated dataset: {args.output}")
    elif args.input:
        df = pd.read_csv(args.input)
    else:
        default_input = Path("data/social_dilemmas_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_commons(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
