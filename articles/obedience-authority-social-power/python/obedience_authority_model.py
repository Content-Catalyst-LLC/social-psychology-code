#!/usr/bin/env python3
"""
Obedience, authority, and social power model.

This script can:
1. Generate synthetic obedience data for ethically modified authority paradigms.
2. Estimate obedience, resistance, escalation, and response-time models.
3. Test authority legitimacy, responsibility displacement, moral conflict, peer dissent, role identification, mission identification, and resistance support.
4. Simulate repeated escalation sequences under different authority and dissent conditions.
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
    "control", "high_legitimacy", "low_legitimacy", "authority_present",
    "authority_distant", "peer_dissent", "peer_compliance", "high_responsibility",
    "responsibility_displacement", "visible_harm", "abstract_harm",
    "mission_identification", "resistance_support"
]

CONTEXTS = [
    "laboratory", "workplace", "military", "hospital", "court",
    "school", "public_agency", "platform_team", "emergency_response"
]


def logistic(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def generate_dataset(n_participants: int = 720, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "control": {"leg": 5.8, "prox": 5.2, "prest": 5.5, "cmd": 5.4, "cost": 4.2, "respdisp": 4.8, "moral": 4.5, "victim": 4.0, "harm": 4.2, "dissent": 3.0, "peercomp": 5.5, "role": 5.0, "mission": 5.2, "responsibility": 5.0},
        "high_legitimacy": {"leg": 8.8, "prox": 7.0, "prest": 8.5, "cmd": 7.8, "cost": 5.5, "respdisp": 6.5, "moral": 5.0, "victim": 3.5, "harm": 4.0, "dissent": 2.0, "peercomp": 7.5, "role": 6.5, "mission": 7.0, "responsibility": 4.0},
        "low_legitimacy": {"leg": 2.8, "prox": 4.0, "prest": 3.0, "cmd": 5.0, "cost": 4.0, "respdisp": 3.0, "moral": 6.5, "victim": 6.0, "harm": 6.5, "dissent": 5.5, "peercomp": 3.5, "role": 4.5, "mission": 3.5, "responsibility": 8.0},
        "authority_present": {"leg": 7.5, "prox": 9.0, "prest": 7.0, "cmd": 8.0, "cost": 6.0, "respdisp": 7.0, "moral": 5.5, "victim": 4.0, "harm": 5.0, "dissent": 2.5, "peercomp": 8.0, "role": 6.0, "mission": 6.5, "responsibility": 3.5},
        "authority_distant": {"leg": 7.0, "prox": 2.5, "prest": 7.0, "cmd": 6.5, "cost": 4.5, "respdisp": 5.0, "moral": 6.0, "victim": 5.0, "harm": 5.5, "dissent": 3.5, "peercomp": 5.0, "role": 5.8, "mission": 6.0, "responsibility": 6.5},
        "peer_dissent": {"leg": 7.2, "prox": 6.5, "prest": 8.0, "cmd": 7.0, "cost": 5.0, "respdisp": 4.0, "moral": 8.0, "victim": 7.5, "harm": 8.0, "dissent": 9.0, "peercomp": 2.0, "role": 5.5, "mission": 6.0, "responsibility": 8.2},
        "peer_compliance": {"leg": 7.8, "prox": 7.5, "prest": 8.0, "cmd": 7.2, "cost": 5.5, "respdisp": 7.2, "moral": 5.5, "victim": 4.0, "harm": 4.5, "dissent": 1.0, "peercomp": 9.0, "role": 6.2, "mission": 7.0, "responsibility": 3.8},
        "high_responsibility": {"leg": 7.0, "prox": 6.0, "prest": 7.0, "cmd": 7.0, "cost": 5.0, "respdisp": 2.0, "moral": 8.5, "victim": 8.0, "harm": 8.5, "dissent": 5.0, "peercomp": 4.5, "role": 5.0, "mission": 5.5, "responsibility": 9.0},
        "responsibility_displacement": {"leg": 7.8, "prox": 7.0, "prest": 7.5, "cmd": 8.0, "cost": 6.0, "respdisp": 8.8, "moral": 5.0, "victim": 3.0, "harm": 4.0, "dissent": 2.0, "peercomp": 8.0, "role": 6.5, "mission": 7.5, "responsibility": 2.5},
        "visible_harm": {"leg": 7.0, "prox": 6.5, "prest": 7.5, "cmd": 7.0, "cost": 5.5, "respdisp": 3.0, "moral": 9.0, "victim": 9.0, "harm": 9.0, "dissent": 6.5, "peercomp": 4.0, "role": 5.8, "mission": 6.0, "responsibility": 9.2},
        "abstract_harm": {"leg": 7.5, "prox": 6.8, "prest": 7.8, "cmd": 7.5, "cost": 5.5, "respdisp": 7.5, "moral": 4.2, "victim": 2.0, "harm": 2.5, "dissent": 2.0, "peercomp": 7.8, "role": 6.4, "mission": 7.2, "responsibility": 3.2},
        "mission_identification": {"leg": 8.0, "prox": 7.0, "prest": 8.2, "cmd": 7.5, "cost": 5.5, "respdisp": 7.5, "moral": 5.5, "victim": 4.0, "harm": 4.5, "dissent": 2.5, "peercomp": 8.5, "role": 8.5, "mission": 9.0, "responsibility": 3.5},
        "resistance_support": {"leg": 6.5, "prox": 5.5, "prest": 6.8, "cmd": 6.0, "cost": 3.0, "respdisp": 3.0, "moral": 8.0, "victim": 7.5, "harm": 8.0, "dissent": 8.5, "peercomp": 2.5, "role": 5.0, "mission": 5.0, "responsibility": 8.8},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        group_id = f"G{rng.integers(1, 121):03d}"
        site_id = f"S{rng.integers(1, 41):02d}"
        moral_trait = float(np.clip(rng.normal(5.0, 1.5), 0, 10))
        deference_trait = float(np.clip(rng.normal(5.0, 1.5), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context = rng.choice(CONTEXTS)
            scenario_id = f"SC{rng.integers(1, 140):03d}"
            e = effects[condition]
            step = int(t)

            authority_legitimacy = float(np.clip(rng.normal(e["leg"], 1.0), 0, 10))
            authority_proximity = float(np.clip(rng.normal(e["prox"], 1.0), 0, 10))
            institutional_prestige = float(np.clip(rng.normal(e["prest"], 1.0), 0, 10))
            command_clarity = float(np.clip(rng.normal(e["cmd"], 1.0), 0, 10))
            cost_of_defiance = float(np.clip(rng.normal(e["cost"], 1.0), 0, 10))
            responsibility_displacement = float(np.clip(rng.normal(e["respdisp"], 1.0), 0, 10))
            moral_conflict = float(np.clip(rng.normal(0.75 * e["moral"] + 0.25 * moral_trait, 1.0), 0, 10))
            victim_proximity = float(np.clip(rng.normal(e["victim"], 1.0), 0, 10))
            harm_salience = float(np.clip(rng.normal(e["harm"], 1.0), 0, 10))
            peer_dissent = float(np.clip(rng.normal(e["dissent"], 1.0), 0, 10))
            peer_compliance = float(np.clip(rng.normal(e["peercomp"], 1.0), 0, 10))
            role_identification = float(np.clip(rng.normal(0.75 * e["role"] + 0.25 * deference_trait, 1.0), 0, 10))
            mission_identification = float(np.clip(rng.normal(e["mission"], 1.0), 0, 10))
            perceived_responsibility_after = float(np.clip(rng.normal(e["responsibility"], 1.0), 0, 10))

            authority_pressure = (
                authority_legitimacy + authority_proximity + institutional_prestige +
                command_clarity + cost_of_defiance + peer_compliance - peer_dissent
            ) / 6.0

            moral_resistance = (
                moral_conflict + victim_proximity + harm_salience +
                peer_dissent + perceived_responsibility_after
            ) / 5.0

            identification = (
                role_identification + mission_identification + institutional_prestige
            ) / 3.0

            latent_obedience = (
                -2.25
                + 0.38 * authority_legitimacy
                + 0.20 * authority_proximity
                + 0.18 * institutional_prestige
                + 0.18 * command_clarity
                + 0.20 * cost_of_defiance
                + 0.22 * step
                + 0.32 * responsibility_displacement
                + 0.24 * identification
                - 0.32 * moral_conflict
                - 0.22 * victim_proximity
                - 0.24 * harm_salience
                - 0.36 * peer_dissent
            )

            obedience_probability = logistic(latent_obedience)
            obeyed = int(rng.random() < obedience_probability)

            latent_resistance = (
                -1.5
                - 0.40 * authority_pressure
                + 0.48 * moral_resistance
                + 0.35 * peer_dissent
                + 0.20 * victim_proximity
                + 0.24 * perceived_responsibility_after
                - 0.25 * cost_of_defiance
            )

            resistance_probability = logistic(latent_resistance)
            resisted = int((rng.random() < resistance_probability) and not obeyed)
            protest = int((rng.random() < (0.18 + 0.07 * moral_conflict + 0.06 * peer_dissent)) or resisted)

            hesitation = float(np.clip(
                2.0
                + 0.55 * moral_conflict
                + 0.35 * harm_salience
                + 0.25 * peer_dissent
                - 0.20 * command_clarity
                + rng.normal(0, 1.2),
                0,
                10
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(900)
                + 0.045 * hesitation
                + 0.035 * moral_conflict
                + 0.025 * peer_dissent
                - 0.018 * command_clarity
                + rng.normal(0, 0.22)
            ), 150, 120000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "scenario_id": scenario_id,
                "site_id": site_id,
                "institution_context": context,
                "condition": condition,
                "trial": t,
                "authority_legitimacy": round(authority_legitimacy, 3),
                "authority_proximity": round(authority_proximity, 3),
                "institutional_prestige": round(institutional_prestige, 3),
                "command_clarity": round(command_clarity, 3),
                "cost_of_defiance": round(cost_of_defiance, 3),
                "escalation_step": step,
                "responsibility_displacement": round(responsibility_displacement, 3),
                "moral_conflict": round(moral_conflict, 3),
                "victim_proximity": round(victim_proximity, 3),
                "harm_salience": round(harm_salience, 3),
                "peer_dissent": round(peer_dissent, 3),
                "peer_compliance": round(peer_compliance, 3),
                "role_identification": round(role_identification, 3),
                "mission_identification": round(mission_identification, 3),
                "obeyed": obeyed,
                "resisted": resisted,
                "hesitation": round(hesitation, 3),
                "protest": protest,
                "response_time_ms": response_time_ms,
                "perceived_responsibility_after": round(perceived_responsibility_after, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["authority_pressure_index"] = (
        data["authority_legitimacy"]
        + data["authority_proximity"]
        + data["institutional_prestige"]
        + data["command_clarity"]
        + data["cost_of_defiance"]
        + data["peer_compliance"]
        - data["peer_dissent"]
    ) / 6.0
    data["moral_resistance_index"] = (
        data["moral_conflict"]
        + data["victim_proximity"]
        + data["harm_salience"]
        + data["peer_dissent"]
        + data["perceived_responsibility_after"]
    ) / 5.0
    data["identification_index"] = (
        data["role_identification"]
        + data["mission_identification"]
        + data["institutional_prestige"]
    ) / 3.0
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "institution_context"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            obedience_rate=("obeyed", "mean"),
            resistance_rate=("resisted", "mean"),
            protest_rate=("protest", "mean"),
            mean_hesitation=("hesitation", "mean"),
            mean_authority_pressure=("authority_pressure_index", "mean"),
            mean_moral_resistance=("moral_resistance_index", "mean"),
            mean_identification=("identification_index", "mean"),
            mean_responsibility_after=("perceived_responsibility_after", "mean"),
        )
        .reset_index()
    )

    escalation = (
        data.groupby(["condition", "escalation_step"])
        .agg(
            n=("participant", "size"),
            obedience_rate=("obeyed", "mean"),
            resistance_rate=("resisted", "mean"),
            mean_authority_pressure=("authority_pressure_index", "mean"),
            mean_moral_resistance=("moral_resistance_index", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    escalation.to_csv(outputs / "summary_by_condition_escalation.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "obedience_model": (
            "obeyed ~ authority_legitimacy + authority_proximity + institutional_prestige "
            "+ command_clarity + cost_of_defiance + escalation_step "
            "+ responsibility_displacement + moral_conflict + victim_proximity "
            "+ harm_salience + peer_dissent + peer_compliance "
            "+ role_identification + mission_identification + condition + institution_context"
        ),
        "resistance_model": (
            "resisted ~ authority_pressure_index + moral_resistance_index "
            "+ identification_index + peer_dissent + victim_proximity "
            "+ perceived_responsibility_after + cost_of_defiance + condition + institution_context"
        ),
        "protest_model": (
            "protest ~ moral_conflict + harm_salience + peer_dissent "
            "+ responsibility_displacement + authority_pressure_index + condition + institution_context"
        ),
        "response_time_model": (
            "log_response_time ~ authority_pressure_index + moral_resistance_index "
            "+ responsibility_displacement + escalation_step + peer_dissent "
            "+ hesitation + condition + institution_context"
        ),
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        if name == "response_time_model":
            model = smf.ols(formula, data=data[data["response_time_ms"] >= 150]).fit(
                cov_type="cluster", cov_kwds={"groups": data.loc[data["response_time_ms"] >= 150, "participant"]}
            )
        else:
            model = smf.glm(formula, data=data, family=sm.families.Binomial()).fit(
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


def simulate_escalation(outputs: Path, n_participants: int = 1000, steps: int = 12, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []
    scenarios = ["high_legitimacy", "peer_dissent", "high_responsibility", "mission_identification", "low_legitimacy", "visible_harm", "resistance_support"]

    for scenario in scenarios:
        for participant in range(1, n_participants + 1):
            for step in range(1, steps + 1):
                legitimacy = {"high_legitimacy": 8.8, "mission_identification": 8.0, "low_legitimacy": 3.0}.get(scenario, 7.0) + rng.normal(0, 0.8)
                peer_dissent = {"peer_dissent": 8.5, "resistance_support": 8.2, "visible_harm": 5.5, "low_legitimacy": 4.5}.get(scenario, 1.8) + rng.normal(0, 0.8)
                responsibility = {"high_responsibility": 8.8, "visible_harm": 8.2, "resistance_support": 8.0}.get(scenario, 3.5) + rng.normal(0, 0.8)
                moral_conflict = {"visible_harm": 8.8, "high_responsibility": 8.0, "peer_dissent": 7.2, "resistance_support": 7.8}.get(scenario, 5.2) + rng.normal(0, 0.8)
                identification = {"mission_identification": 9.0, "high_legitimacy": 7.2}.get(scenario, 4.8) + rng.normal(0, 0.8)
                responsibility_displacement = np.clip(10 - responsibility, 0, 10)

                latent = (
                    -2.1 + 0.38 * legitimacy + 0.25 * identification
                    + 0.20 * step + 0.32 * responsibility_displacement
                    - 0.36 * peer_dissent - 0.30 * moral_conflict
                    - 0.24 * responsibility
                )

                p_obey = 1 / (1 + np.exp(-latent))
                obeyed = int(rng.random() < p_obey)
                rows.append({
                    "scenario": scenario,
                    "participant": participant,
                    "escalation_step": step,
                    "authority_legitimacy": np.clip(legitimacy, 0, 10),
                    "peer_dissent": np.clip(peer_dissent, 0, 10),
                    "perceived_responsibility": np.clip(responsibility, 0, 10),
                    "responsibility_displacement": np.clip(responsibility_displacement, 0, 10),
                    "moral_conflict": np.clip(moral_conflict, 0, 10),
                    "identification": np.clip(identification, 0, 10),
                    "obedience_probability": p_obey,
                    "obeyed": obeyed,
                })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby(["scenario", "escalation_step"])
        .agg(
            obedience_rate=("obeyed", "mean"),
            mean_probability=("obedience_probability", "mean"),
            mean_legitimacy=("authority_legitimacy", "mean"),
            mean_peer_dissent=("peer_dissent", "mean"),
            mean_moral_conflict=("moral_conflict", "mean"),
            mean_responsibility=("perceived_responsibility", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "obedience_escalation_simulation.csv", index=False)
    summary.to_csv(outputs / "obedience_escalation_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/obedience_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=720)
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
        default_input = Path("data/obedience_trials.csv")
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
