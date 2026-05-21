#!/usr/bin/env python3
"""
Intergroup conflict research model.

This script can:
1. Generate synthetic intergroup-conflict data.
2. Estimate hostility, aggression, avoidance, exclusion, cooperation, and response-time models.
3. Test realistic competition, zero-sum perception, identity salience, status threat, symbolic threat, realistic threat, stereotypes, contact, legitimacy, and superordinate-goal effects.
4. Simulate escalation and de-escalation dynamics.
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
    "baseline", "resource_competition", "zero_sum", "identity_salience",
    "status_threat", "symbolic_threat", "realistic_threat",
    "polarization_discussion", "contact_intervention", "superordinate_goal",
    "high_legitimacy", "low_legitimacy"
]

CONTEXT_TYPES = ["laboratory", "online", "organization", "political", "community", "international", "education", "workplace"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 600, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "baseline": {"res": 4.0, "zero": 4.0, "sal": 5.0, "id": 5.5, "stat": 3.5, "sym": 3.5, "real": 3.5, "stereo": 3.0, "warm": 5.5, "comp": 5.5, "anx": 4.0, "inj": 3.5, "dehum": 2.0, "leg": 5.5, "trust": 5.0, "ret": 3.0, "pol": 2.0, "contact": 4.0, "equal": 4.5, "goal": 4.0, "support": 5.0, "task": 45},
        "resource_competition": {"res": 8.5, "zero": 8.0, "sal": 6.0, "id": 6.5, "stat": 5.5, "sym": 4.5, "real": 7.5, "stereo": 5.2, "warm": 3.8, "comp": 5.0, "anx": 6.2, "inj": 6.0, "dehum": 3.5, "leg": 4.0, "trust": 4.0, "ret": 5.2, "pol": 4.5, "contact": 2.5, "equal": 3.0, "goal": 2.0, "support": 3.5, "task": 22},
        "zero_sum": {"res": 7.5, "zero": 9.0, "sal": 6.5, "id": 7.0, "stat": 6.0, "sym": 5.2, "real": 7.0, "stereo": 5.8, "warm": 3.5, "comp": 5.2, "anx": 6.5, "inj": 6.8, "dehum": 4.0, "leg": 4.2, "trust": 4.0, "ret": 6.0, "pol": 5.2, "contact": 2.0, "equal": 2.5, "goal": 2.0, "support": 3.0, "task": 18},
        "identity_salience": {"res": 5.0, "zero": 5.5, "sal": 9.0, "id": 8.5, "stat": 5.0, "sym": 6.0, "real": 5.0, "stereo": 5.5, "warm": 4.0, "comp": 5.0, "anx": 6.0, "inj": 5.8, "dehum": 3.5, "leg": 5.0, "trust": 5.0, "ret": 5.5, "pol": 6.0, "contact": 3.0, "equal": 3.5, "goal": 3.0, "support": 4.0, "task": 35},
        "status_threat": {"res": 5.5, "zero": 6.0, "sal": 7.5, "id": 8.0, "stat": 9.0, "sym": 6.5, "real": 5.8, "stereo": 6.0, "warm": 3.5, "comp": 5.5, "anx": 6.8, "inj": 8.0, "dehum": 4.8, "leg": 3.5, "trust": 3.8, "ret": 6.5, "pol": 6.8, "contact": 2.0, "equal": 2.0, "goal": 2.0, "support": 3.0, "task": 12},
        "symbolic_threat": {"res": 4.5, "zero": 5.5, "sal": 8.0, "id": 8.0, "stat": 6.5, "sym": 9.0, "real": 5.0, "stereo": 7.5, "warm": 2.5, "comp": 5.0, "anx": 7.5, "inj": 7.0, "dehum": 6.5, "leg": 3.0, "trust": 3.5, "ret": 7.0, "pol": 7.5, "contact": 1.5, "equal": 2.0, "goal": 2.0, "support": 2.5, "task": 10},
        "realistic_threat": {"res": 7.0, "zero": 7.5, "sal": 7.0, "id": 7.5, "stat": 6.5, "sym": 5.5, "real": 9.0, "stereo": 6.5, "warm": 3.0, "comp": 5.5, "anx": 7.0, "inj": 7.2, "dehum": 5.0, "leg": 3.8, "trust": 3.5, "ret": 6.8, "pol": 6.5, "contact": 1.8, "equal": 2.5, "goal": 2.0, "support": 3.0, "task": 14},
        "polarization_discussion": {"res": 6.0, "zero": 6.5, "sal": 8.0, "id": 8.0, "stat": 7.0, "sym": 7.0, "real": 6.0, "stereo": 7.0, "warm": 2.8, "comp": 4.8, "anx": 7.5, "inj": 7.0, "dehum": 5.5, "leg": 4.0, "trust": 4.0, "ret": 8.5, "pol": 9.0, "contact": 1.5, "equal": 2.0, "goal": 2.0, "support": 2.5, "task": 8},
        "contact_intervention": {"res": 3.5, "zero": 3.0, "sal": 5.5, "id": 6.0, "stat": 3.5, "sym": 3.2, "real": 3.0, "stereo": 2.8, "warm": 6.8, "comp": 6.5, "anx": 3.0, "inj": 3.2, "dehum": 1.5, "leg": 7.0, "trust": 7.2, "ret": 2.5, "pol": 2.0, "contact": 8.0, "equal": 7.8, "goal": 6.5, "support": 7.5, "task": 78},
        "superordinate_goal": {"res": 4.0, "zero": 3.5, "sal": 6.0, "id": 6.5, "stat": 4.0, "sym": 3.8, "real": 3.5, "stereo": 3.0, "warm": 6.5, "comp": 6.8, "anx": 3.2, "inj": 3.5, "dehum": 1.8, "leg": 7.5, "trust": 7.5, "ret": 2.8, "pol": 2.2, "contact": 7.5, "equal": 7.5, "goal": 9.0, "support": 8.0, "task": 86},
        "high_legitimacy": {"res": 5.0, "zero": 4.5, "sal": 6.5, "id": 7.0, "stat": 4.0, "sym": 4.0, "real": 4.0, "stereo": 3.8, "warm": 6.0, "comp": 6.5, "anx": 4.0, "inj": 4.0, "dehum": 2.0, "leg": 9.0, "trust": 8.8, "ret": 3.5, "pol": 3.0, "contact": 6.5, "equal": 7.5, "goal": 7.0, "support": 8.8, "task": 72},
        "low_legitimacy": {"res": 5.0, "zero": 6.0, "sal": 7.0, "id": 7.5, "stat": 6.5, "sym": 6.0, "real": 5.5, "stereo": 6.5, "warm": 3.2, "comp": 5.0, "anx": 6.8, "inj": 7.5, "dehum": 5.2, "leg": 2.0, "trust": 2.2, "ret": 6.8, "pol": 6.5, "contact": 2.0, "equal": 2.5, "goal": 2.5, "support": 2.0, "task": 18},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 16):02d}"
        outgroup_id = f"G{rng.integers(16, 31):02d}"
        dyad_id = f"D{rng.integers(1, 30):02d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        group_identity_trait = float(np.clip(rng.normal(6.0, 1.5), 0, 10))
        threat_sensitivity = float(np.clip(rng.normal(5.5, 1.6), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context_type = rng.choice(CONTEXT_TYPES)
            scenario_id = f"SC{rng.integers(1, 120):03d}"
            e = effects[condition]

            resource_competition = float(np.clip(rng.normal(e["res"], 1.0), 0, 10))
            zero_sum_perception = float(np.clip(rng.normal(e["zero"], 1.0), 0, 10))
            identity_salience = float(np.clip(rng.normal(e["sal"], 1.0), 0, 10))
            group_identification = float(np.clip(rng.normal(0.55 * e["id"] + 0.45 * group_identity_trait, 1.0), 0, 10))
            status_threat = float(np.clip(rng.normal(e["stat"], 1.0), 0, 10))
            symbolic_threat = float(np.clip(rng.normal(e["sym"], 1.0), 0, 10))
            realistic_threat = float(np.clip(rng.normal(e["real"], 1.0), 0, 10))
            stereotype_endorsement = float(np.clip(rng.normal(e["stereo"], 1.1), 0, 10))
            outgroup_warmth = float(np.clip(rng.normal(e["warm"], 1.0), 0, 10))
            outgroup_competence = float(np.clip(rng.normal(e["comp"], 1.0), 0, 10))
            intergroup_anxiety = float(np.clip(rng.normal(e["anx"], 1.0), 0, 10))
            perceived_injustice = float(np.clip(rng.normal(0.70 * e["inj"] + 0.30 * threat_sensitivity, 1.0), 0, 10))
            dehumanization = float(np.clip(rng.normal(e["dehum"], 1.0), 0, 10))
            perceived_legitimacy = float(np.clip(rng.normal(e["leg"], 1.0), 0, 10))
            institutional_trust = float(np.clip(rng.normal(e["trust"], 1.0), 0, 10))
            norm_of_retaliation = float(np.clip(rng.normal(e["ret"], 1.0), 0, 10))
            group_polarization = float(np.clip(rng.normal(e["pol"], 1.0), 0, 10))
            contact_quality = float(np.clip(rng.normal(e["contact"], 1.0), 0, 10))
            equal_status = float(np.clip(rng.normal(e["equal"], 1.0), 0, 10))
            common_goal_salience = float(np.clip(rng.normal(e["goal"], 1.0), 0, 10))
            institutional_support = float(np.clip(rng.normal(e["support"], 1.0), 0, 10))
            cooperative_task_success = float(np.clip(rng.normal(e["task"], 10), 0, 100))

            hostility_latent = (
                -1.8
                + 0.22 * resource_competition
                + 0.28 * zero_sum_perception
                + 0.18 * identity_salience
                + 0.18 * group_identification
                + 0.30 * status_threat
                + 0.34 * symbolic_threat
                + 0.30 * realistic_threat
                + 0.26 * stereotype_endorsement
                + 0.20 * intergroup_anxiety
                + 0.30 * perceived_injustice
                + 0.34 * dehumanization
                + 0.25 * norm_of_retaliation
                + 0.28 * group_polarization
                - 0.24 * outgroup_warmth
                - 0.18 * perceived_legitimacy
                - 0.16 * institutional_trust
                - 0.28 * contact_quality
                - 0.20 * equal_status
                - 0.24 * common_goal_salience
                - 0.18 * institutional_support
            )

            hostility_score = float(np.clip(100 * logistic(hostility_latent / 3.0) + rng.normal(0, 6), 0, 100))

            aggression_intention = float(np.clip(
                0.60 * hostility_score
                + 3.0 * norm_of_retaliation
                + 2.5 * dehumanization
                + 2.0 * perceived_injustice
                - 2.0 * perceived_legitimacy
                - 1.5 * institutional_trust
                + rng.normal(0, 8),
                0, 100
            ))

            avoidance_intention = float(np.clip(
                0.65 * hostility_score
                + 2.8 * intergroup_anxiety
                + 2.0 * stereotype_endorsement
                - 2.5 * contact_quality
                - 1.5 * outgroup_warmth
                + rng.normal(0, 8),
                0, 100
            ))

            support_for_exclusion = float(np.clip(
                0.55 * hostility_score
                + 3.2 * symbolic_threat
                + 2.6 * realistic_threat
                + 2.8 * dehumanization
                + 2.0 * status_threat
                - 2.2 * perceived_legitimacy
                - 1.8 * institutional_trust
                + rng.normal(0, 8),
                0, 100
            ))

            support_for_cooperation = float(np.clip(
                20
                + 5.0 * contact_quality
                + 4.0 * equal_status
                + 4.5 * common_goal_salience
                + 3.5 * institutional_support
                + 0.20 * cooperative_task_success
                + 2.2 * perceived_legitimacy
                + 2.0 * institutional_trust
                - 0.45 * hostility_score
                - 2.0 * zero_sum_perception
                + rng.normal(0, 8),
                0, 100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(950)
                + 0.006 * hostility_score
                + 0.045 * intergroup_anxiety
                + 0.035 * symbolic_threat
                - 0.030 * perceived_legitimacy
                - 0.030 * contact_quality
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "outgroup_id": outgroup_id,
                "dyad_id": dyad_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "condition": condition,
                "context_type": context_type,
                "trial": t,
                "resource_competition": round(resource_competition, 3),
                "zero_sum_perception": round(zero_sum_perception, 3),
                "identity_salience": round(identity_salience, 3),
                "group_identification": round(group_identification, 3),
                "status_threat": round(status_threat, 3),
                "symbolic_threat": round(symbolic_threat, 3),
                "realistic_threat": round(realistic_threat, 3),
                "stereotype_endorsement": round(stereotype_endorsement, 3),
                "outgroup_warmth": round(outgroup_warmth, 3),
                "outgroup_competence": round(outgroup_competence, 3),
                "intergroup_anxiety": round(intergroup_anxiety, 3),
                "perceived_injustice": round(perceived_injustice, 3),
                "dehumanization": round(dehumanization, 3),
                "perceived_legitimacy": round(perceived_legitimacy, 3),
                "institutional_trust": round(institutional_trust, 3),
                "norm_of_retaliation": round(norm_of_retaliation, 3),
                "group_polarization": round(group_polarization, 3),
                "hostility_score": round(hostility_score, 3),
                "aggression_intention": round(aggression_intention, 3),
                "avoidance_intention": round(avoidance_intention, 3),
                "support_for_exclusion": round(support_for_exclusion, 3),
                "support_for_cooperation": round(support_for_cooperation, 3),
                "contact_quality": round(contact_quality, 3),
                "equal_status": round(equal_status, 3),
                "common_goal_salience": round(common_goal_salience, 3),
                "institutional_support": round(institutional_support, 3),
                "cooperative_task_success": round(cooperative_task_success, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["material_conflict_index"] = (data["resource_competition"] + data["zero_sum_perception"] + data["realistic_threat"]) / 3.0
    data["identity_threat_index"] = (data["identity_salience"] + data["group_identification"] + data["status_threat"] + data["symbolic_threat"]) / 4.0
    data["dehumanization_exclusion_index"] = (data["stereotype_endorsement"] + data["dehumanization"] + data["support_for_exclusion"] / 10.0) / 3.0
    data["cooperative_contact_index"] = (data["contact_quality"] + data["equal_status"] + data["common_goal_salience"] + data["institutional_support"]) / 4.0
    data["legitimacy_index"] = (data["perceived_legitimacy"] + data["institutional_trust"]) / 2.0
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
            groups=("group_id", "nunique"),
            dyads=("dyad_id", "nunique"),
            mean_hostility=("hostility_score", "mean"),
            mean_aggression=("aggression_intention", "mean"),
            mean_avoidance=("avoidance_intention", "mean"),
            mean_exclusion=("support_for_exclusion", "mean"),
            mean_cooperation=("support_for_cooperation", "mean"),
            mean_material_conflict=("material_conflict_index", "mean"),
            mean_identity_threat=("identity_threat_index", "mean"),
            mean_dehumanization_exclusion=("dehumanization_exclusion_index", "mean"),
            mean_contact=("cooperative_contact_index", "mean"),
            mean_legitimacy=("legitimacy_index", "mean"),
            mean_response_time=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    condition_summary = (
        data.groupby("condition")
        .agg(
            n=("participant", "size"),
            mean_hostility=("hostility_score", "mean"),
            mean_aggression=("aggression_intention", "mean"),
            mean_exclusion=("support_for_exclusion", "mean"),
            mean_cooperation=("support_for_cooperation", "mean"),
            mean_contact=("cooperative_contact_index", "mean"),
            mean_legitimacy=("legitimacy_index", "mean"),
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
        "hostility_model": "hostility_score ~ material_conflict_index + identity_threat_index + stereotype_endorsement + outgroup_warmth + outgroup_competence + intergroup_anxiety + perceived_injustice + dehumanization + norm_of_retaliation + group_polarization + cooperative_contact_index + legitimacy_index + cooperative_task_success + condition + context_type",
        "aggression_model": "aggression_intention ~ hostility_score + norm_of_retaliation + dehumanization + perceived_injustice + material_conflict_index + identity_threat_index + legitimacy_index + cooperative_contact_index + condition + context_type",
        "exclusion_model": "support_for_exclusion ~ hostility_score + symbolic_threat + realistic_threat + status_threat + dehumanization + stereotype_endorsement + legitimacy_index + cooperative_contact_index + condition + context_type",
        "cooperation_model": "support_for_cooperation ~ cooperative_contact_index + common_goal_salience + equal_status + institutional_support + legitimacy_index + cooperative_task_success + hostility_score + zero_sum_perception + condition + context_type",
        "response_time_model": "log_response_time ~ hostility_score + intergroup_anxiety + symbolic_threat + realistic_threat + cooperative_contact_index + legitimacy_index + condition + context_type",
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


def simulate_escalation(outputs: Path, n_cases: int = 10000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []

    for scenario in ["competition_only", "identity_threat", "polarization", "contact_intervention", "superordinate_goal", "low_legitimacy"]:
        for _ in range(n_cases):
            conflict = {"competition_only": 55, "identity_threat": 62, "polarization": 70, "contact_intervention": 42, "superordinate_goal": 40, "low_legitimacy": 66}[scenario] + rng.normal(0, 6)
            threat = {"competition_only": 6.5, "identity_threat": 8.5, "polarization": 8.0, "contact_intervention": 4.0, "superordinate_goal": 4.2, "low_legitimacy": 7.0}[scenario] + rng.normal(0, 0.8)
            contact = {"contact_intervention": 8.0, "superordinate_goal": 7.5}.get(scenario, 2.5) + rng.normal(0, 0.8)
            common_goal = {"superordinate_goal": 9.0, "contact_intervention": 6.5}.get(scenario, 2.5) + rng.normal(0, 0.8)
            legitimacy = {"low_legitimacy": 2.5, "contact_intervention": 7.0, "superordinate_goal": 7.5}.get(scenario, 4.5) + rng.normal(0, 0.8)
            retaliation = {"polarization": 8.5, "identity_threat": 7.0, "low_legitimacy": 7.0}.get(scenario, 5.0) + rng.normal(0, 0.8)

            for period in range(1, 16):
                hostile_interaction = np.clip(0.55 * conflict + 3.0 * threat + 2.5 * retaliation - 2.8 * contact - 2.5 * common_goal - 2.5 * legitimacy + rng.normal(0, 5), 0, 100)
                threat = np.clip(threat + 0.020 * hostile_interaction - 0.22 * contact - 0.22 * common_goal - 0.15 * legitimacy + rng.normal(0, 0.25), 0, 10)
                conflict = np.clip(conflict + 0.25 * hostile_interaction + 2.5 * threat + 1.5 * retaliation - 3.0 * contact - 3.2 * common_goal - 2.0 * legitimacy + rng.normal(0, 5), 0, 100)

                rows.append({
                    "scenario": scenario,
                    "period": period,
                    "conflict_intensity": conflict,
                    "perceived_threat": threat,
                    "contact_quality": contact,
                    "common_goal_salience": common_goal,
                    "institutional_legitimacy": legitimacy,
                    "norm_of_retaliation": retaliation,
                    "hostile_interaction": hostile_interaction,
                })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby(["scenario", "period"])
        .agg(
            mean_conflict=("conflict_intensity", "mean"),
            mean_threat=("perceived_threat", "mean"),
            mean_hostility=("hostile_interaction", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "intergroup_escalation_simulation.csv", index=False)
    summary.to_csv(outputs / "intergroup_escalation_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/intergroup_conflict_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=600)
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
        default_input = Path("data/intergroup_conflict_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_escalation(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
