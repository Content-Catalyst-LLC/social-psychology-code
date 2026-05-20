#!/usr/bin/env python3
"""
Tragedy of the commons research model.

This script can:
1. Generate synthetic commons-extraction data.
2. Estimate extraction, stock, payoff, depletion-risk, legitimacy, and response-time models.
3. Compute institutional-effectiveness, expected-sanction, and stewardship-restraint indices.
4. Simulate open-access collapse and governed-commons resilience.
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
    "open_access", "communication", "boundary_clarity", "monitoring",
    "graduated_sanctions", "participatory_rules", "external_rules",
    "legitimacy_high", "legitimacy_low", "polycentric"
]

PROPERTY_REGIMES = ["open_access", "common_property", "private_property", "state_property", "hybrid", "polycentric"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_groups: int = 180, group_size: int = 6, rounds_per_group: int = 10, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "open_access": {"trust": -1.5, "legit": -2.5, "monitor": -2.0, "sanction": -1.5, "boundary": -2.5, "participation": -2.5, "conflict": -2.0, "knowledge": -0.5, "fairness": -1.0, "norm": -1.5, "asym": 1.5},
        "communication": {"trust": 1.2, "legit": 0.8, "monitor": 0.0, "sanction": 0.0, "boundary": 0.5, "participation": 1.2, "conflict": 0.6, "knowledge": 0.6, "fairness": 0.8, "norm": 1.1, "asym": 0.0},
        "boundary_clarity": {"trust": 0.6, "legit": 0.8, "monitor": 0.7, "sanction": 0.2, "boundary": 3.0, "participation": 0.8, "conflict": 0.8, "knowledge": 0.8, "fairness": 0.6, "norm": 0.8, "asym": 0.0},
        "monitoring": {"trust": 0.4, "legit": 0.4, "monitor": 3.2, "sanction": 1.2, "boundary": 1.0, "participation": 0.4, "conflict": 0.6, "knowledge": 0.7, "fairness": 0.3, "norm": 0.5, "asym": 0.0},
        "graduated_sanctions": {"trust": 0.6, "legit": 1.4, "monitor": 2.4, "sanction": 2.8, "boundary": 1.4, "participation": 1.0, "conflict": 1.2, "knowledge": 0.8, "fairness": 1.2, "norm": 1.0, "asym": 0.0},
        "participatory_rules": {"trust": 1.6, "legit": 2.8, "monitor": 1.6, "sanction": 1.4, "boundary": 2.0, "participation": 3.4, "conflict": 2.0, "knowledge": 1.5, "fairness": 2.4, "norm": 2.0, "asym": -0.4},
        "external_rules": {"trust": -0.4, "legit": -1.2, "monitor": 1.8, "sanction": 2.0, "boundary": 1.2, "participation": -2.0, "conflict": -0.6, "knowledge": 0.2, "fairness": -1.2, "norm": -0.2, "asym": 0.8},
        "legitimacy_high": {"trust": 1.2, "legit": 3.2, "monitor": 1.4, "sanction": 1.4, "boundary": 1.4, "participation": 2.0, "conflict": 1.5, "knowledge": 1.0, "fairness": 2.4, "norm": 1.8, "asym": -0.2},
        "legitimacy_low": {"trust": -1.4, "legit": -3.2, "monitor": 1.8, "sanction": 2.4, "boundary": 0.8, "participation": -1.5, "conflict": -1.0, "knowledge": 0.2, "fairness": -2.5, "norm": -1.0, "asym": 2.5},
        "polycentric": {"trust": 1.4, "legit": 2.4, "monitor": 2.2, "sanction": 1.8, "boundary": 2.2, "participation": 2.5, "conflict": 2.3, "knowledge": 1.8, "fairness": 1.8, "norm": 2.2, "asym": -0.2},
    }

    regime_for_condition = {
        "open_access": "open_access",
        "communication": "common_property",
        "boundary_clarity": "common_property",
        "monitoring": "hybrid",
        "graduated_sanctions": "common_property",
        "participatory_rules": "common_property",
        "external_rules": "state_property",
        "legitimacy_high": "hybrid",
        "legitimacy_low": "state_property",
        "polycentric": "polycentric",
    }

    for g in range(1, n_groups + 1):
        group_id = f"G{g:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        condition = rng.choice(CONDITIONS)
        regime = regime_for_condition[condition]
        e = effects[condition]

        carrying_capacity = float(rng.uniform(120, 180))
        resource_stock = float(rng.uniform(0.65, 0.85) * carrying_capacity)
        regeneration_rate = float(rng.uniform(0.08, 0.16))

        for round_number in range(1, rounds_per_group + 1):
            previous_stock = resource_stock
            regeneration = max(0.0, regeneration_rate * resource_stock * (1 - resource_stock / carrying_capacity))
            sustainable_threshold = regeneration

            participant_rows = []
            extractions = []

            for member in range(1, group_size + 1):
                participant = f"P{g:04d}_{member:02d}"

                trust = float(np.clip(rng.normal(5.0 + e["trust"] - 0.04 * (round_number - 1), 1.0), 0, 10))
                legitimacy = float(np.clip(rng.normal(5.0 + e["legit"], 1.0), 0, 10))
                monitoring = float(np.clip(rng.normal(4.0 + e["monitor"], 1.0), 0, 10))
                sanction_probability = float(np.clip(0.05 + 0.06 * monitoring + 0.04 * max(e["sanction"], 0), 0, 1))
                sanction_severity = float(np.clip(rng.normal(1.0 + max(e["sanction"], 0) + 0.25 * legitimacy, 1.0), 0, 10))
                boundary_clarity = float(np.clip(rng.normal(5.0 + e["boundary"], 1.0), 0, 10))
                rule_participation = float(np.clip(rng.normal(5.0 + e["participation"], 1.0), 0, 10))
                conflict_resolution = float(np.clip(rng.normal(5.0 + e["conflict"], 1.0), 0, 10))
                local_knowledge = float(np.clip(rng.normal(5.0 + e["knowledge"], 1.0), 0, 10))
                fairness = float(np.clip(rng.normal(5.0 + e["fairness"], 1.0), 0, 10))
                reciprocity = float(np.clip(rng.normal(5.0 + 0.25 * trust + 0.15 * fairness + 0.10 * e["norm"], 1.0), 0, 10))
                stewardship_norm = float(np.clip(rng.normal(5.0 + e["norm"] + 0.15 * legitimacy, 1.0), 0, 10))
                asymmetry = float(np.clip(rng.normal(3.0 + e["asym"], 1.0), 0, 10))

                expected_sanction = monitoring * sanction_probability * sanction_severity / 10.0
                institutional_effectiveness = (
                    boundary_clarity
                    * monitoring
                    * max(sanction_probability, 0.01)
                    * max(sanction_severity, 0.01)
                    * (legitimacy / 10.0)
                    * (rule_participation / 10.0)
                )

                extraction_tendency = (
                    9.0
                    - 0.28 * trust
                    - 0.26 * legitimacy
                    - 0.16 * monitoring
                    - 0.18 * expected_sanction
                    - 0.17 * boundary_clarity
                    - 0.16 * rule_participation
                    - 0.14 * fairness
                    - 0.18 * reciprocity
                    - 0.20 * stewardship_norm
                    - 0.08 * local_knowledge
                    + 0.24 * asymmetry
                    + 0.03 * (round_number - 1)
                    + rng.normal(0, 1.0)
                )

                extraction = float(np.clip(extraction_tendency, 0, max(0.1, resource_stock / group_size)))
                extractions.append(extraction)

                participant_rows.append({
                    "participant": participant,
                    "group_id": group_id,
                    "site_id": site_id,
                    "condition": condition,
                    "property_regime": regime,
                    "round": round_number,
                    "resource_stock": round(previous_stock, 3),
                    "carrying_capacity": round(carrying_capacity, 3),
                    "regeneration_rate": round(regeneration_rate, 4),
                    "regeneration": round(regeneration, 3),
                    "extraction": round(extraction, 3),
                    "sustainable_threshold": round(sustainable_threshold, 3),
                    "trust_score": round(trust, 3),
                    "legitimacy_score": round(legitimacy, 3),
                    "monitoring_credibility": round(monitoring, 3),
                    "sanction_probability": round(sanction_probability, 3),
                    "sanction_severity": round(sanction_severity, 3),
                    "boundary_clarity": round(boundary_clarity, 3),
                    "rule_participation": round(rule_participation, 3),
                    "conflict_resolution_access": round(conflict_resolution, 3),
                    "local_ecological_knowledge": round(local_knowledge, 3),
                    "perceived_fairness": round(fairness, 3),
                    "reciprocity_expectation": round(reciprocity, 3),
                    "stewardship_norm_salience": round(stewardship_norm, 3),
                    "asymmetry_index": round(asymmetry, 3),
                    "institutional_effectiveness": institutional_effectiveness,
                    "expected_sanction": expected_sanction,
                })

            total_extraction = sum(extractions)
            resource_stock = float(np.clip(resource_stock + regeneration - total_extraction, 0, carrying_capacity))
            depletion_risk = float(np.clip(1 - resource_stock / carrying_capacity, 0, 1))
            group_welfare = float(sum([20 + r["extraction"] for r in participant_rows]) + 0.35 * resource_stock)

            for r in participant_rows:
                sanction = 0.0
                if r["extraction"] > (sustainable_threshold / group_size) and rng.random() < r["sanction_probability"]:
                    sanction = 0.6 * r["sanction_severity"]
                individual_payoff = 20 + r["extraction"] - sanction - 2.0 * depletion_risk

                response_time_ms = int(np.clip(np.exp(
                    math.log(1050)
                    + 0.05 * abs(r["legitimacy_score"] - 5)
                    + 0.04 * abs(r["trust_score"] - 5)
                    + rng.normal(0, 0.18)
                ), 150, 60000))

                r.pop("institutional_effectiveness", None)
                r.pop("expected_sanction", None)
                r["depletion_risk"] = round(depletion_risk, 3)
                r["group_welfare"] = round(group_welfare, 3)
                r["individual_payoff"] = round(individual_payoff, 3)
                r["response_time_ms"] = response_time_ms
                rows.append(r)

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["expected_sanction"] = (
        data["monitoring_credibility"]
        * data["sanction_probability"]
        * data["sanction_severity"]
        / 10.0
    )
    data["institutional_effectiveness"] = (
        data["boundary_clarity"]
        * data["monitoring_credibility"]
        * np.maximum(data["sanction_probability"], 0.01)
        * np.maximum(data["sanction_severity"], 0.01)
        * (data["legitimacy_score"] / 10.0)
        * (data["rule_participation"] / 10.0)
    )
    data["restraint_index"] = (
        data["trust_score"]
        + data["legitimacy_score"]
        + data["reciprocity_expectation"]
        + data["stewardship_norm_salience"]
        + data["local_ecological_knowledge"]
        - data["asymmetry_index"]
    ) / 5.0
    data["over_extraction"] = (
        data["extraction"] > (data["sustainable_threshold"] / data.groupby(["group_id", "round"])["participant"].transform("count"))
    ).astype(int)
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "property_regime", "round"])
        .agg(
            n=("participant", "size"),
            groups=("group_id", "nunique"),
            mean_extraction=("extraction", "mean"),
            total_extraction=("extraction", "sum"),
            mean_stock=("resource_stock", "mean"),
            mean_regeneration=("regeneration", "mean"),
            mean_depletion_risk=("depletion_risk", "mean"),
            over_extraction_rate=("over_extraction", "mean"),
            mean_trust=("trust_score", "mean"),
            mean_legitimacy=("legitimacy_score", "mean"),
            mean_monitoring=("monitoring_credibility", "mean"),
            mean_institutional_effectiveness=("institutional_effectiveness", "mean"),
            mean_group_welfare=("group_welfare", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby(["condition", "property_regime"])
        .agg(
            n=("participant", "size"),
            mean_extraction=("extraction", "mean"),
            mean_stock=("resource_stock", "mean"),
            mean_depletion_risk=("depletion_risk", "mean"),
            over_extraction_rate=("over_extraction", "mean"),
            mean_payoff=("individual_payoff", "mean"),
            mean_group_welfare=("group_welfare", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_regime_round.csv", index=False)
    condition_summary.to_csv(outputs / "summary_by_condition_regime.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    model_text = []
    coefficient_frames = []

    formulas = {
        "extraction_model": "extraction ~ round + trust_score + legitimacy_score + monitoring_credibility + expected_sanction + boundary_clarity + rule_participation + conflict_resolution_access + local_ecological_knowledge + perceived_fairness + reciprocity_expectation + stewardship_norm_salience + asymmetry_index + resource_stock + condition + property_regime",
        "stock_model": "resource_stock ~ round + extraction + regeneration + institutional_effectiveness + trust_score + legitimacy_score + monitoring_credibility + condition + property_regime",
        "depletion_risk_model": "depletion_risk ~ extraction + institutional_effectiveness + trust_score + legitimacy_score + stewardship_norm_salience + asymmetry_index + condition + property_regime",
        "payoff_model": "individual_payoff ~ extraction + depletion_risk + expected_sanction + legitimacy_score + perceived_fairness + condition + property_regime",
        "response_time_model": "log_response_time ~ round + extraction + trust_score + legitimacy_score + monitoring_credibility + depletion_risk + condition + property_regime",
    }

    for name, formula in formulas.items():
        model_data = data[data["response_time_ms"] >= 150] if name == "response_time_model" else data
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


def simulate_governance(outputs: Path, n_groups: int = 300, periods: int = 60, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    regimes = np.array(["open_access", "common_property", "state_property", "polycentric"])
    regime_index = rng.choice(len(regimes), size=n_groups, p=[0.30, 0.35, 0.15, 0.20])
    resource = rng.uniform(80, 130, n_groups)
    capacity = rng.uniform(130, 180, n_groups)
    regen_rate = rng.uniform(0.08, 0.16, n_groups)

    legitimacy = np.where(regimes[regime_index] == "open_access", rng.uniform(1, 4, n_groups), rng.uniform(4, 9, n_groups))
    monitoring = np.where(regimes[regime_index] == "open_access", rng.uniform(0, 3, n_groups), rng.uniform(3, 9, n_groups))
    stewardship = np.where(regimes[regime_index] == "open_access", rng.uniform(1, 4, n_groups), rng.uniform(4, 9, n_groups))

    for period in range(1, periods + 1):
        extraction = np.clip(
            9.0
            - 0.28 * legitimacy
            - 0.25 * monitoring
            - 0.30 * stewardship
            + rng.normal(0, 1.0, n_groups),
            0,
            14,
        )
        total_extraction = 6 * extraction
        regeneration = np.maximum(0, regen_rate * resource * (1 - resource / capacity))
        resource = np.clip(resource + regeneration - total_extraction, 0, capacity)
        depletion_risk = np.clip(1 - resource / capacity, 0, 1)

        for i in range(n_groups):
            rows.append({
                "group_id": f"G{i+1:04d}",
                "period": period,
                "property_regime": regimes[regime_index[i]],
                "resource_stock": resource[i],
                "mean_extraction": extraction[i],
                "regeneration": regeneration[i],
                "legitimacy": legitimacy[i],
                "monitoring": monitoring[i],
                "stewardship": stewardship[i],
                "depletion_risk": depletion_risk[i],
            })

    sim = pd.DataFrame(rows)
    summary = (
        sim.groupby(["property_regime", "period"])
        .agg(
            mean_resource_stock=("resource_stock", "mean"),
            mean_extraction=("mean_extraction", "mean"),
            mean_depletion_risk=("depletion_risk", "mean"),
            depleted_rate=("resource_stock", lambda x: np.mean(x <= 1)),
        )
        .reset_index()
    )

    sim.to_csv(outputs / "governance_simulation.csv", index=False)
    summary.to_csv(outputs / "governance_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/tragedy_commons_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--groups", type=int, default=180)
    parser.add_argument("--group-size", type=int, default=6)
    parser.add_argument("--rounds", type=int, default=10)
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
        default_input = Path("data/tragedy_commons_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_governance(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
