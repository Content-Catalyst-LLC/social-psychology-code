#!/usr/bin/env python3
"""Synthetic data, models, and simulations for social loafing research."""

from __future__ import annotations
import argparse
import math
from pathlib import Path
import numpy as np
import pandas as pd

try:
    import statsmodels.formula.api as smf
    STATSMODELS_AVAILABLE = True
except Exception:
    STATSMODELS_AVAILABLE = False

CONDITIONS = [
    "solo", "pooled_group", "identifiable_group", "high_accountability",
    "low_accountability", "high_task_value", "low_task_value",
    "unique_contribution", "distributed_team", "traceable_digital_team"
]
TASK_TYPES = ["physical", "cognitive", "creative", "academic", "organizational", "digital", "public_goods"]

def generate_dataset(n_participants=450, trials_per_participant=6, seed=42):
    rng = np.random.default_rng(seed)
    rows = []

    effects = {
        "solo": (1, 10, 9, 6, 8, 9, 0, 1, 1, 2, 4, 4, 9, "solo"),
        "pooled_group": (6, 2, 2, 5, 2, 2, 0, 7, 7, 5, 4, 4, 2, "co-located"),
        "identifiable_group": (5, 8, 7, 6, 5, 8, 2, 3, 2, 3, 5, 5, 8, "co-located"),
        "high_accountability": (6, 7, 9, 6, 5, 8, 4, 3, 2, 3, 5, 5, 9, "hybrid"),
        "low_accountability": (7, 2, 2, 4, 3, 2, 1, 8, 8, 6, 3, 3, 2, "hybrid"),
        "high_task_value": (6, 6, 7, 9, 6, 7, 5, 3, 2, 3, 7, 7, 7, "co-located"),
        "low_task_value": (6, 3, 3, 2, 3, 3, 2, 7, 8, 6, 3, 3, 3, "remote"),
        "unique_contribution": (5, 7, 7, 7, 10, 8, 4, 1, 1, 2, 6, 6, 8, "co-located"),
        "distributed_team": (8, 3, 3, 6, 4, 3, 3, 7, 6, 7, 3, 3, 3, "remote"),
        "traceable_digital_team": (8, 8, 8, 7, 6, 9, 9, 3, 2, 3, 6, 6, 8, "remote"),
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        baseline_effort = np.clip(rng.normal(78, 9), 25, 100)
        compensation_trait = np.clip(rng.normal(4.5, 1.8), 0, 10)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            task_type = rng.choice(TASK_TYPES)
            (g, ident, acct, value, unique, visible, trace, disp, free, sucker,
             cohesion, identity, evalpot, remote_status) = effects[condition]

            group_size = max(1, int(round(rng.normal(g, 1.4))))
            identifiability = np.clip(rng.normal(ident, 1.0), 0, 10)
            accountability = np.clip(rng.normal(acct, 1.0), 0, 10)
            task_value = np.clip(rng.normal(value, 1.1), 0, 10)
            task_uniqueness = np.clip(rng.normal(unique, 1.0), 0, 10)
            task_visibility = np.clip(rng.normal(visible, 1.0), 0, 10)
            digital_traceability = np.clip(rng.normal(trace, 1.0), 0, 10)
            group_cohesion = np.clip(rng.normal(cohesion, 1.1), 0, 10)
            group_identity_salience = np.clip(rng.normal(identity, 1.1), 0, 10)
            evaluation_potential = np.clip(rng.normal(evalpot + 0.15*identifiability + 0.10*digital_traceability, 1.0), 0, 10)
            perceived_dispensability = np.clip(rng.normal(disp + 0.25*np.log1p(group_size) - 0.20*task_uniqueness, 1.0), 0, 10)
            perceived_instrumentality = np.clip(rng.normal(2 + 0.25*identifiability + 0.23*accountability + 0.25*task_uniqueness + 0.18*task_value - 0.25*perceived_dispensability, 1.0), 0, 10)
            free_rider_expectation = np.clip(rng.normal(free + 0.18*perceived_dispensability - 0.18*accountability, 1.0), 0, 10)
            sucker_effect_concern = np.clip(rng.normal(sucker + 0.20*free_rider_expectation - 0.15*group_cohesion, 1.0), 0, 10)
            social_compensation_tendency = np.clip(rng.normal(compensation_trait + 0.20*task_value + 0.15*group_identity_salience - 0.20*free_rider_expectation, 1.1), 0, 10)

            solo_effort = np.clip(baseline_effort + rng.normal(0, 4), 0, 100)
            coordination_loss = np.clip(rng.normal(1.0 + 0.65*np.log1p(group_size) + 0.7*(remote_status in ["remote", "hybrid"]) - 0.16*task_visibility - 0.10*group_cohesion, 1.4), 0, 30)
            motivation_loss = np.clip(rng.normal(
                2.0 + 1.1*np.log1p(group_size) + 0.9*free_rider_expectation + 0.75*perceived_dispensability + 0.50*sucker_effect_concern
                - 0.85*identifiability - 0.78*accountability - 0.60*task_value - 0.55*task_uniqueness
                - 0.50*perceived_instrumentality - 0.40*digital_traceability - 0.30*group_identity_salience,
                3.0), 0, 45)
            compensation_gain = max(0, 0.45 * social_compensation_tendency * (task_value/10) * (group_identity_salience/10))
            group_effort = np.clip(solo_effort - motivation_loss + compensation_gain + rng.normal(0, 3), 0, 100)
            effort_loss = np.clip(solo_effort - group_effort, -100, 100)
            output_score = np.clip(group_effort - 0.45*coordination_loss + 0.25*task_value + rng.normal(0, 4), 0, 100)
            response_time_ms = int(np.clip(np.exp(math.log(950) + 0.035*group_size + 0.025*coordination_loss - 0.020*identifiability + rng.normal(0, 0.18)), 150, 60000))

            rows.append({
                "participant": participant, "session_id": session_id, "team_id": f"T{rng.integers(1,151):03d}",
                "task_id": f"TA{rng.integers(1,80):03d}", "site_id": site_id, "condition": condition,
                "task_type": task_type, "trial": trial, "group_size": group_size,
                "solo_effort": solo_effort, "group_effort": group_effort, "effort_loss": effort_loss,
                "output_score": output_score, "coordination_loss": coordination_loss, "motivation_loss": motivation_loss,
                "identifiability": identifiability, "accountability": accountability, "task_value": task_value,
                "task_uniqueness": task_uniqueness, "task_visibility": task_visibility,
                "perceived_dispensability": perceived_dispensability, "perceived_instrumentality": perceived_instrumentality,
                "free_rider_expectation": free_rider_expectation, "sucker_effect_concern": sucker_effect_concern,
                "social_compensation_tendency": social_compensation_tendency, "group_cohesion": group_cohesion,
                "group_identity_salience": group_identity_salience, "evaluation_potential": evaluation_potential,
                "digital_traceability": digital_traceability, "remote_status": remote_status, "response_time_ms": response_time_ms
            })

    return pd.DataFrame(rows).round(3)

def add_indices(df):
    data = df.copy()
    data["log_group_size"] = np.log1p(data["group_size"])
    data["accountability_index"] = (data["identifiability"] + data["accountability"] + data["task_visibility"] + data["evaluation_potential"] + data["digital_traceability"]) / 5
    data["collective_effort_index"] = (data["perceived_instrumentality"] + data["task_value"] + data["task_uniqueness"] + data["group_identity_salience"] + data["group_cohesion"] - data["perceived_dispensability"]) / 5
    data["motivation_loss_share"] = data["motivation_loss"] / np.maximum(data["coordination_loss"] + data["motivation_loss"], 1e-6)
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data

def summarize_and_model(df, outputs):
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)
    summary = data.groupby(["condition", "task_type"], observed=True).agg(
        n=("participant", "size"),
        participants=("participant", "nunique"),
        mean_group_size=("group_size", "mean"),
        mean_solo_effort=("solo_effort", "mean"),
        mean_group_effort=("group_effort", "mean"),
        mean_effort_loss=("effort_loss", "mean"),
        mean_output=("output_score", "mean"),
        mean_coordination_loss=("coordination_loss", "mean"),
        mean_motivation_loss=("motivation_loss", "mean"),
        mean_identifiability=("identifiability", "mean"),
        mean_accountability=("accountability", "mean"),
        mean_task_value=("task_value", "mean"),
        mean_instrumentality=("perceived_instrumentality", "mean")
    ).reset_index()
    summary.to_csv(outputs / "summary_by_condition_task.csv", index=False)

    group_summary = data.assign(group_size_band=pd.cut(data["group_size"], [0,1,3,6,10,10000], labels=["solo","dyad_triads","small_group","medium_group","large_group"])).groupby(["condition","group_size_band"], observed=True).agg(
        n=("participant","size"),
        mean_effort_loss=("effort_loss","mean"),
        mean_motivation_loss=("motivation_loss","mean"),
        mean_output=("output_score","mean"),
        mean_accountability=("accountability_index","mean"),
        mean_collective_effort=("collective_effort_index","mean")
    ).reset_index()
    group_summary.to_csv(outputs / "summary_by_condition_group_size.csv", index=False)

    if STATSMODELS_AVAILABLE:
        formulas = {
            "effort_loss_model": "effort_loss ~ log_group_size + identifiability + accountability + task_value + task_uniqueness + perceived_dispensability + perceived_instrumentality + free_rider_expectation + sucker_effect_concern + group_cohesion + group_identity_salience + digital_traceability + condition + task_type + remote_status",
            "motivation_loss_model": "motivation_loss ~ log_group_size + accountability_index + collective_effort_index + perceived_dispensability + free_rider_expectation + sucker_effect_concern + social_compensation_tendency + condition + task_type + remote_status",
            "output_model": "output_score ~ group_effort + coordination_loss + motivation_loss + accountability_index + collective_effort_index + condition + task_type + remote_status",
            "response_time_model": "log_response_time ~ log_group_size + coordination_loss + motivation_loss + accountability_index + collective_effort_index + condition + task_type + remote_status",
        }
        text = []
        coefs = []
        for name, formula in formulas.items():
            model = smf.ols(formula, data=data).fit(cov_type="cluster", cov_kwds={"groups": data["participant"]})
            text.append(f"\n\n=== {name} ===\n{model.summary()}")
            coefs.append(pd.DataFrame({"model": name, "term": model.params.index, "estimate": model.params.values, "std_error": model.bse.values}))
        (outputs / "model_summary.txt").write_text("\n".join(text), encoding="utf-8")
        pd.concat(coefs, ignore_index=True).to_csv(outputs / "model_coefficients.csv", index=False)

def simulate_collective_effort(outputs, seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for condition in ["pooled_group", "identifiable_group", "high_accountability", "traceable_digital_team"]:
        for _ in range(8000):
            group_size = {"pooled_group": 8, "identifiable_group": 6, "high_accountability": 6, "traceable_digital_team": 8}[condition]
            ident = {"pooled_group": 2, "identifiable_group": 8, "high_accountability": 7, "traceable_digital_team": 8}[condition] + rng.normal(0, .8)
            acct = {"pooled_group": 2, "identifiable_group": 7, "high_accountability": 9, "traceable_digital_team": 8}[condition] + rng.normal(0, .8)
            value = {"pooled_group": 5, "identifiable_group": 6, "high_accountability": 6, "traceable_digital_team": 7}[condition] + rng.normal(0, .8)
            trace = {"pooled_group": 0, "identifiable_group": 2, "high_accountability": 4, "traceable_digital_team": 9}[condition] + rng.normal(0, .8)
            instr = np.clip(2 + .3*ident + .25*acct + .2*value - .25*np.log1p(group_size), 0, 10)
            mloss = np.clip(3 + 1.5*np.log1p(group_size) - .8*ident - .8*acct - .6*value - .5*instr - .4*trace + rng.normal(0,2), 0, 40)
            solo = np.clip(rng.normal(80,7), 0, 100)
            group = np.clip(solo - mloss + rng.normal(0,3), 0, 100)
            rows.append([condition, group_size, ident, acct, value, trace, instr, mloss, solo, group, solo-group])
    sim = pd.DataFrame(rows, columns=["condition","group_size","identifiability","accountability","task_value","digital_traceability","perceived_instrumentality","motivation_loss","solo_effort","group_effort","effort_loss"])
    sim.to_csv(outputs / "collective_effort_simulation.csv", index=False)
    sim.groupby("condition").agg(n=("condition","size"), mean_effort_loss=("effort_loss","mean"), mean_motivation_loss=("motivation_loss","mean"), mean_group_effort=("group_effort","mean")).reset_index().to_csv(outputs / "collective_effort_simulation_summary.csv", index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/social_loafing_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=450)
    parser.add_argument("--trials", type=int, default=6)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.simulate or not args.input:
        df = generate_dataset(args.participants, args.trials, args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
    else:
        df = pd.read_csv(args.input)
    summarize_and_model(df, args.outputs)
    simulate_collective_effort(args.outputs, args.seed)
    print(f"Wrote outputs to: {args.outputs}")

if __name__ == "__main__":
    main()
