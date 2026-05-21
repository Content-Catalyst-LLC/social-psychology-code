#!/usr/bin/env python3
"""
Attribution theory model.

This script can:
1. Generate synthetic attribution trial data.
2. Estimate internal attribution, external attribution, responsibility, hostile attribution, achievement expectation, and response-time models.
3. Simulate institutional blame under different system-visibility and accountability conditions.
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
    "control", "high_constraint", "low_constraint", "high_consensus", "low_consensus",
    "high_distinctiveness", "low_distinctiveness", "high_consistency", "low_consistency",
    "accountability", "system_visibility", "hostile_ambiguity", "achievement_feedback",
]

CONTEXTS = ["laboratory", "education", "law", "organization", "public_policy", "medicine", "platform", "intergroup_conflict"]
DOMAINS = ["achievement", "harm", "helping", "workplace", "legal", "health", "political", "intergroup", "everyday"]
TARGET_TYPES = ["self", "other", "ingroup", "outgroup", "institution", "leader", "subordinate"]
VALENCES = ["success", "failure", "harm", "help", "neutral"]


def generate_dataset(n_participants: int = 800, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    profiles: Dict[str, Dict[str, float]] = {
        "control": {"constraint": 5, "consensus": 5, "distinct": 5, "consistency": 5, "intent": 5, "choice": 5, "complex": 5},
        "high_constraint": {"constraint": 9, "consensus": 7, "distinct": 8, "consistency": 7, "intent": 4, "choice": 3, "complex": 7},
        "low_constraint": {"constraint": 1, "consensus": 2, "distinct": 2, "consistency": 8, "intent": 8, "choice": 9, "complex": 4},
        "high_consensus": {"constraint": 6, "consensus": 9, "distinct": 7, "consistency": 8, "intent": 6, "choice": 5, "complex": 7},
        "low_consensus": {"constraint": 2, "consensus": 1, "distinct": 3, "consistency": 8, "intent": 8, "choice": 8, "complex": 4},
        "high_distinctiveness": {"constraint": 7, "consensus": 6, "distinct": 9, "consistency": 8, "intent": 5, "choice": 5, "complex": 7},
        "low_distinctiveness": {"constraint": 2, "consensus": 3, "distinct": 1, "consistency": 8, "intent": 8, "choice": 8, "complex": 4},
        "high_consistency": {"constraint": 4, "consensus": 4, "distinct": 4, "consistency": 9, "intent": 8, "choice": 7, "complex": 5},
        "low_consistency": {"constraint": 6, "consensus": 6, "distinct": 7, "consistency": 2, "intent": 4, "choice": 5, "complex": 7},
        "accountability": {"constraint": 7, "consensus": 7, "distinct": 7, "consistency": 8, "intent": 6, "choice": 6, "complex": 8},
        "system_visibility": {"constraint": 8, "consensus": 8, "distinct": 8, "consistency": 8, "intent": 5, "choice": 5, "complex": 8},
        "hostile_ambiguity": {"constraint": 4, "consensus": 3, "distinct": 3, "consistency": 6, "intent": 7, "choice": 7, "complex": 3},
        "achievement_feedback": {"constraint": 5, "consensus": 5, "distinct": 5, "consistency": 8, "intent": 6, "choice": 7, "complex": 6},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 160):03d}"
        site_id = f"S{rng.integers(1, 55):02d}"
        agency_orientation = np.clip(rng.normal(5, 1.8), 0, 10)
        threat_sensitivity = np.clip(rng.normal(5, 1.5), 0, 10)

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            profile = profiles[condition]
            context = rng.choice(CONTEXTS)
            domain = rng.choice(DOMAINS)
            target_type = rng.choice(TARGET_TYPES)
            self_other = "self" if target_type == "self" else "other"
            outcome_valence = rng.choice(VALENCES)
            scenario_id = f"SC{rng.integers(1, 240):03d}"

            ambiguity = float(np.clip(rng.normal(7 if condition == "hostile_ambiguity" else 5, 1.5), 0, 10))
            intentionality = float(np.clip(rng.normal(profile["intent"], 1.2), 0, 10))
            perceived_choice = float(np.clip(rng.normal(profile["choice"], 1.2), 0, 10))
            perceived_effort = float(np.clip(rng.normal(7 if outcome_valence == "success" else 5, 1.5), 0, 10))
            perceived_ability = float(np.clip(rng.normal(7 if outcome_valence == "success" else 4.5, 1.5), 0, 10))
            situational_constraint = float(np.clip(rng.normal(profile["constraint"], 1.2), 0, 10))
            consensus = float(np.clip(rng.normal(profile["consensus"], 1.2), 0, 10))
            distinctiveness = float(np.clip(rng.normal(profile["distinct"], 1.2), 0, 10))
            consistency = float(np.clip(rng.normal(profile["consistency"], 1.2), 0, 10))
            attributional_complexity = float(np.clip(rng.normal(profile["complex"], 1.2), 0, 10))
            cultural_agency_orientation = float(np.clip(rng.normal(agency_orientation, 1.0), 0, 10))

            negative_event = 1 if outcome_valence in {"failure", "harm"} else 0
            positive_event = 1 if outcome_valence in {"success", "help"} else 0
            outgroup = 1 if target_type == "outgroup" else 0
            self_case = 1 if self_other == "self" else 0

            internal = (
                25
                + 4.0 * intentionality
                + 3.4 * perceived_choice
                + 2.0 * perceived_effort
                + 2.2 * perceived_ability
                + 2.3 * consistency
                - 3.5 * situational_constraint
                - 1.8 * consensus
                - 1.2 * distinctiveness
                + 2.2 * cultural_agency_orientation
                + 4.5 * outgroup * negative_event
                - 4.0 * self_case * negative_event
                + rng.normal(0, 9)
            )
            internal = float(np.clip(internal, 0, 100))

            external = (
                30
                + 4.0 * situational_constraint
                + 2.3 * consensus
                + 2.8 * distinctiveness
                + 1.2 * ambiguity
                - 2.5 * intentionality
                - 2.0 * perceived_choice
                + 1.8 * attributional_complexity
                - 2.0 * cultural_agency_orientation
                + 5.0 * self_case * negative_event
                + rng.normal(0, 9)
            )
            external = float(np.clip(external, 0, 100))

            stability = float(np.clip(
                0.08 * internal + 0.30 * consistency + 0.20 * perceived_ability + rng.normal(0, 1.2),
                0, 10
            ))
            controllability = float(np.clip(
                0.32 * intentionality + 0.32 * perceived_choice + 0.20 * perceived_effort - 0.22 * situational_constraint + rng.normal(0, 1.2),
                0, 10
            ))

            responsibility = float(np.clip(
                10
                + 0.42 * internal
                - 0.25 * external
                + 3.8 * controllability
                + 2.8 * intentionality
                + 2.0 * perceived_choice
                - 2.5 * situational_constraint
                + rng.normal(0, 8),
                0, 100
            ))

            blame = float(np.clip(
                5
                + 0.70 * responsibility
                + 1.5 * negative_event
                - 0.18 * external
                + rng.normal(0, 8),
                0, 100
            ))
            sympathy = float(np.clip(
                65
                + 0.25 * external
                - 0.45 * responsibility
                + 1.8 * situational_constraint
                + rng.normal(0, 8),
                0, 100
            ))
            anger = float(np.clip(
                8
                + 0.65 * blame
                + 1.5 * intentionality
                - 0.25 * sympathy
                + rng.normal(0, 8),
                0, 100
            ))
            punishment = float(np.clip(
                5
                + 0.70 * blame
                + 0.25 * anger
                - 0.18 * external
                + rng.normal(0, 8),
                0, 100
            ))
            help_support = float(np.clip(
                45
                + 0.35 * sympathy
                + 0.25 * external
                - 0.28 * blame
                + rng.normal(0, 8),
                0, 100
            ))
            achievement_expectation = float(np.clip(
                45
                + 3.0 * perceived_ability
                + 2.0 * perceived_effort
                + 2.5 * stability
                - 1.8 * situational_constraint
                + rng.normal(0, 9),
                0, 100
            ))
            hostile = float(np.clip(
                10
                + 4.5 * ambiguity
                + 3.5 * threat_sensitivity
                + 4.0 * outgroup
                + 2.0 * negative_event
                - 2.0 * attributional_complexity
                - 1.8 * situational_constraint
                + rng.normal(0, 9),
                0, 100
            ))

            response_time = int(np.clip(np.exp(
                math.log(820)
                + 0.030 * ambiguity
                + 0.015 * abs(internal - external) / 10
                - 0.020 * attributional_complexity
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "behavior_domain": domain,
                "target_type": target_type,
                "self_other": self_other,
                "outcome_valence": outcome_valence,
                "condition": condition,
                "trial": t,
                "ambiguity_level": round(ambiguity, 3),
                "intentionality": round(intentionality, 3),
                "perceived_choice": round(perceived_choice, 3),
                "perceived_effort": round(perceived_effort, 3),
                "perceived_ability": round(perceived_ability, 3),
                "situational_constraint": round(situational_constraint, 3),
                "consensus": round(consensus, 3),
                "distinctiveness": round(distinctiveness, 3),
                "consistency": round(consistency, 3),
                "attribution_internal": round(internal, 3),
                "attribution_external": round(external, 3),
                "stability_rating": round(stability, 3),
                "controllability_rating": round(controllability, 3),
                "responsibility_rating": round(responsibility, 3),
                "blame_rating": round(blame, 3),
                "sympathy_rating": round(sympathy, 3),
                "anger_rating": round(anger, 3),
                "punishment_support": round(punishment, 3),
                "help_support": round(help_support, 3),
                "achievement_expectation": round(achievement_expectation, 3),
                "hostile_attribution_score": round(hostile, 3),
                "attributional_complexity": round(attributional_complexity, 3),
                "cultural_agency_orientation": round(cultural_agency_orientation, 3),
                "response_time_ms": response_time,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["log_response_time"] = np.log(data["response_time_ms"])
    data["disposition_bias_index"] = data["attribution_internal"] - data["attribution_external"]
    data["covariation_situation_index"] = (data["consensus"] + data["distinctiveness"] + data["consistency"]) / 3.0
    data["responsibility_inference_index"] = (
        data["intentionality"] + data["perceived_choice"] + data["controllability_rating"] - data["situational_constraint"]
    ) / 3.0
    data["system_visible_attribution_index"] = data["attribution_external"] + 2.0 * data["attributional_complexity"]
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "target_type", "outcome_valence"], observed=True)
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_internal=("attribution_internal", "mean"),
            mean_external=("attribution_external", "mean"),
            mean_responsibility=("responsibility_rating", "mean"),
            mean_blame=("blame_rating", "mean"),
            mean_sympathy=("sympathy_rating", "mean"),
            mean_punishment=("punishment_support", "mean"),
            mean_help=("help_support", "mean"),
            mean_hostile=("hostile_attribution_score", "mean"),
        )
        .reset_index()
    )

    context_summary = (
        data.groupby(["institution_context", "behavior_domain"], observed=True)
        .agg(
            n=("participant", "size"),
            mean_disposition_bias=("disposition_bias_index", "mean"),
            mean_covariation_situation=("covariation_situation_index", "mean"),
            mean_responsibility=("responsibility_rating", "mean"),
            mean_attributional_complexity=("attributional_complexity", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_target_valence.csv", index=False)
    context_summary.to_csv(outputs / "summary_by_context_domain.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "internal_attribution_model": (
            "attribution_internal ~ ambiguity_level + intentionality + perceived_choice "
            "+ perceived_effort + perceived_ability + situational_constraint "
            "+ consensus + distinctiveness + consistency + target_type + outcome_valence + condition"
        ),
        "external_attribution_model": (
            "attribution_external ~ ambiguity_level + situational_constraint "
            "+ consensus + distinctiveness + consistency + intentionality + perceived_choice "
            "+ attributional_complexity + target_type + outcome_valence + condition"
        ),
        "responsibility_model": (
            "responsibility_rating ~ attribution_internal + attribution_external "
            "+ intentionality + perceived_choice + controllability_rating + situational_constraint "
            "+ outcome_valence + condition"
        ),
        "hostile_attribution_model": (
            "hostile_attribution_score ~ ambiguity_level + target_type + outcome_valence "
            "+ situational_constraint + attributional_complexity + condition"
        ),
        "achievement_expectation_model": (
            "achievement_expectation ~ perceived_effort + perceived_ability + stability_rating "
            "+ controllability_rating + situational_constraint + outcome_valence + condition"
        ),
        "response_time_model": (
            "log_response_time ~ ambiguity_level + attribution_internal + attribution_external "
            "+ attributional_complexity + target_type + condition"
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


def simulate_institutional_blame(outputs: Path, steps: int = 80, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    scenarios = [
        "low_system_visibility",
        "high_system_visibility",
        "accountability_review",
        "individual_blame_culture",
        "systems_learning_culture",
    ]

    for scenario in scenarios:
        individual_blame = 0.65
        system_attribution = 0.35

        for step in range(1, steps + 1):
            if scenario == "low_system_visibility":
                actor_salience, system_visibility, accountability = 0.85, 0.20, 0.25
            elif scenario == "high_system_visibility":
                actor_salience, system_visibility, accountability = 0.45, 0.75, 0.55
            elif scenario == "accountability_review":
                actor_salience, system_visibility, accountability = 0.45, 0.80, 0.85
            elif scenario == "individual_blame_culture":
                actor_salience, system_visibility, accountability = 0.90, 0.15, 0.20
            else:
                actor_salience, system_visibility, accountability = 0.35, 0.90, 0.90

            blame_pressure = actor_salience - system_visibility - 0.35 * accountability
            individual_blame = np.clip(individual_blame + 0.05 * blame_pressure + rng.normal(0, 0.025), 0, 1)
            system_attribution = np.clip(system_attribution + 0.05 * (system_visibility + accountability - actor_salience) + rng.normal(0, 0.025), 0, 1)
            learning_quality = np.clip(0.25 + 0.45 * system_attribution + 0.25 * accountability - 0.25 * individual_blame, 0, 1)

            rows.append({
                "scenario": scenario,
                "step": step,
                "individual_blame": individual_blame,
                "system_attribution": system_attribution,
                "learning_quality": learning_quality,
                "actor_salience": actor_salience,
                "system_visibility": system_visibility,
                "accountability": accountability,
            })

    pd.DataFrame(rows).to_csv(outputs / "institutional_blame_simulation.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/attribution_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=800)
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
        default_input = Path("data/attribution_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_institutional_blame(args.outputs, seed=args.seed)
    print(f"Wrote outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
