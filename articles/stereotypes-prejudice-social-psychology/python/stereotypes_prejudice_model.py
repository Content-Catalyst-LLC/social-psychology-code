#!/usr/bin/env python3
"""
Stereotypes, prejudice, and discrimination model.

This script can:
1. Generate synthetic data for stereotype-content, prejudice, discrimination, contact, and stereotype-threat studies.
2. Estimate models for prejudice, discrimination tendency, response time, stereotype content, and performance.
3. Simulate cumulative institutional disparity from repeated small decision differences.
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
    "control", "contact_quality", "equal_status_contact", "cooperative_goals",
    "threat_salience", "stereotype_threat", "structured_criteria",
    "accountability", "identity_safety", "counter_stereotypical_exposure"
]

CONTEXTS = [
    "laboratory", "education", "employment", "healthcare", "criminal_justice",
    "housing", "public_policy", "platform", "organization"
]


def generate_dataset(n_participants: int = 750, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "control": {"st": 5.2, "warm": 5.0, "comp": 5.4, "prej": 4.8, "threat": 4.5, "competition": 4.2, "status": 5.5, "dist": 4.5, "cq": 3.0, "cnum": 3.5, "support": 3.0, "stth": 2.0, "safe": 4.0, "implicit": 0.35, "explicit": 5, "disc": 48, "out": 62, "perf": 70, "struct": 3, "acct": 3},
        "threat_salience": {"st": 7.4, "warm": 3.2, "comp": 6.2, "prej": 7.5, "threat": 8.6, "competition": 8.0, "status": 6.5, "dist": 7.8, "cq": 2.0, "cnum": 2.5, "support": 2.0, "stth": 3.0, "safe": 2.5, "implicit": 0.82, "explicit": -10, "disc": 70, "out": 50, "perf": 66, "struct": 2, "acct": 2},
        "stereotype_threat": {"st": 6.8, "warm": 4.0, "comp": 5.0, "prej": 6.2, "threat": 6.4, "competition": 5.8, "status": 5.0, "dist": 6.0, "cq": 3.0, "cnum": 3.0, "support": 3.0, "stth": 8.8, "safe": 2.0, "implicit": 0.60, "explicit": 0, "disc": 63, "out": 55, "perf": 58, "struct": 3, "acct": 3},
        "identity_safety": {"st": 4.5, "warm": 6.5, "comp": 6.2, "prej": 3.8, "threat": 3.0, "competition": 3.0, "status": 5.5, "dist": 3.5, "cq": 5.5, "cnum": 5.0, "support": 7.5, "stth": 3.0, "safe": 8.5, "implicit": 0.22, "explicit": 12, "disc": 36, "out": 74, "perf": 78, "struct": 6, "acct": 7},
        "structured_criteria": {"st": 4.8, "warm": 5.8, "comp": 6.2, "prej": 4.2, "threat": 4.0, "competition": 4.2, "status": 6.0, "dist": 4.0, "cq": 4.0, "cnum": 3.5, "support": 6.0, "stth": 2.0, "safe": 6.0, "implicit": 0.25, "explicit": 10, "disc": 35, "out": 76, "perf": 73, "struct": 9, "acct": 7},
        "accountability": {"st": 5.0, "warm": 5.7, "comp": 6.0, "prej": 4.0, "threat": 4.0, "competition": 4.0, "status": 6.0, "dist": 3.8, "cq": 4.0, "cnum": 4.0, "support": 6.5, "stth": 2.0, "safe": 6.5, "implicit": 0.28, "explicit": 15, "disc": 34, "out": 78, "perf": 75, "struct": 7, "acct": 9},
        "contact_quality": {"st": 4.0, "warm": 6.8, "comp": 5.5, "prej": 3.2, "threat": 2.8, "competition": 3.0, "status": 5.5, "dist": 2.8, "cq": 8.5, "cnum": 7.0, "support": 8.0, "stth": 2.0, "safe": 7.5, "implicit": 0.10, "explicit": 20, "disc": 28, "out": 82, "perf": 76, "struct": 6, "acct": 7},
        "equal_status_contact": {"st": 3.8, "warm": 7.2, "comp": 5.8, "prej": 3.0, "threat": 2.5, "competition": 2.5, "status": 5.5, "dist": 2.5, "cq": 8.0, "cnum": 6.0, "support": 8.8, "stth": 2.0, "safe": 8.0, "implicit": 0.05, "explicit": 25, "disc": 25, "out": 84, "perf": 78, "struct": 7, "acct": 8},
        "cooperative_goals": {"st": 4.2, "warm": 7.0, "comp": 6.0, "prej": 3.4, "threat": 3.0, "competition": 2.8, "status": 5.8, "dist": 3.0, "cq": 7.8, "cnum": 6.5, "support": 8.2, "stth": 2.5, "safe": 7.8, "implicit": 0.12, "explicit": 18, "disc": 30, "out": 80, "perf": 77, "struct": 7, "acct": 7},
        "counter_stereotypical_exposure": {"st": 3.5, "warm": 7.0, "comp": 6.8, "prej": 2.8, "threat": 2.2, "competition": 2.5, "status": 6.5, "dist": 2.2, "cq": 5.5, "cnum": 5.0, "support": 6.5, "stth": 2.0, "safe": 7.2, "implicit": -0.05, "explicit": 30, "disc": 22, "out": 86, "perf": 80, "struct": 6, "acct": 7},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 140):03d}"
        site_id = f"S{rng.integers(1, 50):02d}"
        egalitarian_trait = rng.normal(0, 1)

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context = rng.choice(CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 180):03d}"
            e = effects[condition]

            stereotype_strength = float(np.clip(rng.normal(e["st"] - 0.20 * egalitarian_trait, 1.0), 0, 10))
            warmth = float(np.clip(rng.normal(e["warm"], 1.0), 0, 10))
            competence = float(np.clip(rng.normal(e["comp"], 1.0), 0, 10))
            threat = float(np.clip(rng.normal(e["threat"], 1.0), 0, 10))
            competition = float(np.clip(rng.normal(e["competition"], 1.0), 0, 10))
            status = float(np.clip(rng.normal(e["status"], 1.0), 0, 10))
            contact_quality = float(np.clip(rng.normal(e["cq"], 1.0), 0, 10))
            contact_quantity = float(np.clip(rng.normal(e["cnum"], 1.0), 0, 10))
            institutional_support = float(np.clip(rng.normal(e["support"], 1.0), 0, 10))
            stereotype_threat = float(np.clip(rng.normal(e["stth"], 1.0), 0, 10))
            identity_safety = float(np.clip(rng.normal(e["safe"], 1.0), 0, 10))
            implicit_score = float(np.clip(rng.normal(e["implicit"], 0.35), -3, 3))
            explicit_attitude = float(np.clip(rng.normal(e["explicit"] + 8 * egalitarian_trait, 18), -100, 100))
            structured_criteria = float(np.clip(rng.normal(e["struct"], 1.0), 0, 10))
            accountability = float(np.clip(rng.normal(e["acct"], 1.0), 0, 10))

            prejudice_rating = float(np.clip(
                e["prej"]
                + 0.30 * stereotype_strength
                + 0.35 * threat
                + 0.20 * competition
                - 0.30 * contact_quality
                - 0.20 * institutional_support
                - 0.04 * explicit_attitude
                + rng.normal(0, 1.2),
                0,
                10
            ))

            social_distance = float(np.clip(
                e["dist"]
                + 0.45 * prejudice_rating
                + 0.20 * threat
                - 0.25 * contact_quality
                + rng.normal(0, 1.1),
                0,
                10
            ))

            discrimination_tendency = float(np.clip(
                e["disc"]
                + 4.0 * prejudice_rating
                + 3.0 * stereotype_strength
                + 8.0 * implicit_score
                + 2.0 * threat
                - 2.8 * structured_criteria
                - 2.2 * accountability
                - 1.5 * institutional_support
                + rng.normal(0, 8),
                0,
                100
            ))

            behavioral_outcome = float(np.clip(
                e["out"]
                - 0.28 * discrimination_tendency
                + 1.5 * structured_criteria
                + 1.2 * accountability
                + rng.normal(0, 8),
                0,
                100
            ))

            performance_score = float(np.clip(
                e["perf"]
                - 3.0 * stereotype_threat
                + 2.0 * identity_safety
                + 0.8 * institutional_support
                + rng.normal(0, 9),
                0,
                100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(850)
                + 0.040 * stereotype_strength
                + 0.035 * prejudice_rating
                + 0.020 * threat
                + 0.025 * stereotype_threat
                - 0.015 * structured_criteria
                + rng.normal(0, 0.22)
            ), 250, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "condition": condition,
                "trial": t,
                "target_group": "group_a" if rng.random() < 0.5 else "group_b",
                "evaluator_group": "group_b" if rng.random() < 0.5 else "group_c",
                "stereotype_strength": round(stereotype_strength, 3),
                "warmth_rating": round(warmth, 3),
                "competence_rating": round(competence, 3),
                "prejudice_rating": round(prejudice_rating, 3),
                "perceived_threat": round(threat, 3),
                "perceived_competition": round(competition, 3),
                "perceived_status": round(status, 3),
                "social_distance": round(social_distance, 3),
                "contact_quality": round(contact_quality, 3),
                "contact_quantity": round(contact_quantity, 3),
                "institutional_support": round(institutional_support, 3),
                "stereotype_threat_salience": round(stereotype_threat, 3),
                "identity_safety": round(identity_safety, 3),
                "implicit_score": round(implicit_score, 3),
                "explicit_attitude": round(explicit_attitude, 3),
                "discrimination_tendency": round(discrimination_tendency, 3),
                "behavioral_outcome": round(behavioral_outcome, 3),
                "performance_score": round(performance_score, 3),
                "response_time_ms": response_time_ms,
                "structured_criteria": round(structured_criteria, 3),
                "accountability": round(accountability, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["log_response_time"] = np.log(data["response_time_ms"])
    data["contact_support_index"] = (
        data["contact_quality"] + data["contact_quantity"] + data["institutional_support"]
    ) / 3.0
    data["threat_competition_index"] = (
        data["perceived_threat"] + data["perceived_competition"]
    ) / 2.0
    data["decision_structure_index"] = (
        data["structured_criteria"] + data["accountability"]
    ) / 2.0
    data["stereotype_content_asymmetry"] = data["competence_rating"] - data["warmth_rating"]
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "institution_context"], observed=True)
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_stereotype_strength=("stereotype_strength", "mean"),
            mean_prejudice=("prejudice_rating", "mean"),
            mean_discrimination=("discrimination_tendency", "mean"),
            mean_behavioral_outcome=("behavioral_outcome", "mean"),
            mean_performance=("performance_score", "mean"),
            mean_contact_support=("contact_support_index", "mean"),
            mean_threat_competition=("threat_competition_index", "mean"),
            mean_decision_structure=("decision_structure_index", "mean"),
        )
        .reset_index()
    )

    target_summary = (
        data.groupby(["target_group", "condition"], observed=True)
        .agg(
            n=("participant", "size"),
            mean_warmth=("warmth_rating", "mean"),
            mean_competence=("competence_rating", "mean"),
            mean_prejudice=("prejudice_rating", "mean"),
            mean_discrimination=("discrimination_tendency", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    target_summary.to_csv(outputs / "summary_by_target_condition.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "prejudice_model": (
            "prejudice_rating ~ stereotype_strength + perceived_threat + perceived_competition "
            "+ contact_quality + contact_quantity + institutional_support "
            "+ implicit_score + explicit_attitude + condition + institution_context"
        ),
        "discrimination_model": (
            "discrimination_tendency ~ stereotype_strength + prejudice_rating + perceived_threat "
            "+ implicit_score + explicit_attitude + structured_criteria + accountability "
            "+ institutional_support + condition + institution_context"
        ),
        "performance_model": (
            "performance_score ~ stereotype_threat_salience + identity_safety "
            "+ institutional_support + condition + institution_context"
        ),
        "stereotype_content_model": (
            "warmth_rating ~ perceived_competition + perceived_threat + contact_quality "
            "+ institutional_support + condition + institution_context"
        ),
        "competence_model": (
            "competence_rating ~ perceived_status + perceived_competition "
            "+ stereotype_strength + condition + institution_context"
        ),
        "response_time_model": (
            "log_response_time ~ stereotype_strength + prejudice_rating + perceived_threat "
            "+ stereotype_threat_salience + structured_criteria + condition + institution_context"
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


def simulate_cumulative_disparity(outputs: Path, decisions: int = 10000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []
    scenarios = ["unstructured_discretion", "threat_salience", "structured_criteria", "accountability", "contact_and_structure"]

    for scenario in scenarios:
        cumulative = 0.0
        for decision in range(1, decisions + 1):
            if scenario == "unstructured_discretion":
                disparity = rng.normal(0.020, 0.055)
            elif scenario == "threat_salience":
                disparity = rng.normal(0.035, 0.065)
            elif scenario == "structured_criteria":
                disparity = rng.normal(0.006, 0.035)
            elif scenario == "accountability":
                disparity = rng.normal(0.008, 0.038)
            else:
                disparity = rng.normal(0.002, 0.030)

            cumulative += disparity
            if decision % 100 == 0:
                rows.append({
                    "scenario": scenario,
                    "decision": decision,
                    "decision_disparity": disparity,
                    "cumulative_disparity": cumulative,
                })

    pd.DataFrame(rows).to_csv(outputs / "cumulative_institutional_disparity_simulation.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/stereotypes_prejudice_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=750)
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
        default_input = Path("data/stereotypes_prejudice_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_cumulative_disparity(args.outputs, seed=args.seed)
    print(f"Wrote outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
