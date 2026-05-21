#!/usr/bin/env python3
"""
Deindividuation research model.

This script can:
1. Generate synthetic deindividuation/SIDE data.
2. Estimate norm-congruence, prosocial behavior, antisocial behavior, self-awareness, accountability, and response-time models.
3. Test anonymity-by-group-identity-by-norm-valence interactions.
4. Simulate identity-shift dynamics in online, crowd, and laboratory contexts.
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
    "identified", "anonymous", "anonymous_prosocial_norm", "anonymous_antisocial_norm",
    "high_accountability", "low_self_awareness", "side_group_salient",
    "digital_pseudonym", "moderated_platform"
]

CONTEXT_TYPES = ["laboratory", "crowd", "online", "organization", "political", "platform", "classroom"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 420, trials_per_participant: int = 6, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "identified": {"anon": 1.0, "ident": 8.0, "group": 2.5, "personal": 8.0, "aware": 8.0, "acct": 8.0, "norm": 0.0, "clarity": 3.0, "moderation": 7.0},
        "anonymous": {"anon": 8.0, "ident": 1.5, "group": 4.5, "personal": 3.0, "aware": 3.5, "acct": 2.5, "norm": 0.0, "clarity": 4.0, "moderation": 2.0},
        "anonymous_prosocial_norm": {"anon": 8.3, "ident": 1.4, "group": 8.0, "personal": 2.8, "aware": 3.2, "acct": 3.0, "norm": 4.0, "clarity": 8.0, "moderation": 5.5},
        "anonymous_antisocial_norm": {"anon": 8.5, "ident": 1.2, "group": 8.0, "personal": 2.5, "aware": 3.0, "acct": 2.2, "norm": -4.0, "clarity": 8.0, "moderation": 1.8},
        "high_accountability": {"anon": 3.0, "ident": 7.0, "group": 5.0, "personal": 7.5, "aware": 7.5, "acct": 8.5, "norm": 1.5, "clarity": 6.0, "moderation": 7.5},
        "low_self_awareness": {"anon": 6.5, "ident": 3.0, "group": 5.5, "personal": 2.5, "aware": 2.0, "acct": 3.0, "norm": -1.0, "clarity": 5.0, "moderation": 2.5},
        "side_group_salient": {"anon": 7.0, "ident": 2.2, "group": 9.0, "personal": 3.2, "aware": 3.5, "acct": 3.5, "norm": 3.0, "clarity": 8.5, "moderation": 4.5},
        "digital_pseudonym": {"anon": 7.5, "ident": 3.0, "group": 7.0, "personal": 3.8, "aware": 3.8, "acct": 4.0, "norm": -2.0, "clarity": 6.5, "moderation": 3.0},
        "moderated_platform": {"anon": 6.0, "ident": 4.2, "group": 7.0, "personal": 4.8, "aware": 5.0, "acct": 6.8, "norm": 3.0, "clarity": 8.0, "moderation": 8.5},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        session_id = f"SE{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        baseline_prosociality = float(np.clip(rng.normal(5.0, 1.5), 0, 10))
        baseline_aggression = float(np.clip(rng.normal(3.5, 1.5), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            context_type = rng.choice(CONTEXT_TYPES)
            group_id = f"G{rng.integers(1, 121):03d}"
            e = effects[condition]

            group_size = int(np.clip(round(np.exp(rng.normal(math.log(18 if context_type in ["online", "platform", "crowd"] else 6), 0.8))), 1, 10000))

            anonymity = float(np.clip(rng.normal(e["anon"], 0.9), 0, 10))
            identifiability = float(np.clip(rng.normal(e["ident"], 0.9), 0, 10))
            group_identity_salience = float(np.clip(rng.normal(e["group"], 1.0), 0, 10))
            personal_identity_salience = float(np.clip(rng.normal(e["personal"], 1.0), 0, 10))
            self_awareness = float(np.clip(rng.normal(e["aware"] + 0.25 * identifiability - 0.25 * anonymity, 1.0), 0, 10))
            accountability = float(np.clip(rng.normal(e["acct"] + 0.30 * identifiability - 0.20 * anonymity + 0.25 * e["moderation"], 1.0), 0, 10))
            group_norm_valence = float(np.clip(rng.normal(e["norm"], 1.2), -5, 5))
            norm_clarity = float(np.clip(rng.normal(e["clarity"], 1.0), 0, 10))
            crowd_immersion = float(np.clip(rng.normal(2.0 + 0.30 * anonymity + 0.16 * group_identity_salience + 0.20 * math.log1p(group_size), 1.0), 0, 10))
            arousal_index = float(np.clip(rng.normal(2.0 + 0.35 * crowd_immersion + 0.18 * group_identity_salience + 0.10 * abs(group_norm_valence), 1.0), 0, 10))
            emotional_contagion = float(np.clip(rng.normal(1.5 + 0.40 * crowd_immersion + 0.20 * arousal_index + 0.12 * norm_clarity, 1.0), 0, 10))
            responsibility_diffusion = float(np.clip(rng.normal(1.0 + 0.42 * anonymity + 0.20 * math.log1p(group_size) - 0.30 * accountability, 1.0), 0, 10))
            moral_disengagement = float(np.clip(rng.normal(2.0 + 0.28 * responsibility_diffusion + 0.22 * max(-group_norm_valence, 0) - 0.25 * self_awareness, 1.1), 0, 10))
            perceived_surveillance = float(np.clip(rng.normal(0.40 * identifiability + 0.25 * accountability + 0.35 * e["moderation"], 1.0), 0, 10))
            moderation_visibility = float(np.clip(rng.normal(e["moderation"], 1.0), 0, 10))

            lambda_group = float(np.clip(
                logistic(
                    -2.0
                    + 0.28 * anonymity
                    + 0.24 * crowd_immersion
                    + 0.30 * group_identity_salience
                    - 0.22 * personal_identity_salience
                    - 0.18 * accountability
                ),
                0, 1
            ))

            norm_congruence = float(np.clip(
                2.0
                + 6.0 * lambda_group
                + 0.20 * norm_clarity
                + 0.15 * emotional_contagion
                - 0.10 * perceived_surveillance
                + rng.normal(0, 0.8),
                0, 10
            ))

            prosocial_behavior = float(np.clip(
                35
                + 4.0 * baseline_prosociality
                + 4.2 * max(group_norm_valence, 0)
                + 2.2 * norm_congruence * (group_norm_valence > 0)
                + 1.2 * moderation_visibility
                + 0.9 * accountability
                - 0.6 * moral_disengagement
                + rng.normal(0, 6),
                0, 100
            ))

            antisocial_behavior = float(np.clip(
                18
                + 4.0 * baseline_aggression
                + 5.0 * max(-group_norm_valence, 0)
                + 2.6 * norm_congruence * (group_norm_valence < 0)
                + 1.8 * moral_disengagement
                + 1.2 * responsibility_diffusion
                - 1.2 * accountability
                - 1.1 * moderation_visibility
                - 0.6 * self_awareness
                + rng.normal(0, 6),
                0, 100
            ))

            behavior_score = float(np.clip(
                50
                + (prosocial_behavior - antisocial_behavior) * 0.35
                + group_norm_valence * norm_congruence
                + rng.normal(0, 5),
                0, 100
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(950)
                + 0.04 * arousal_index
                + 0.03 * norm_clarity
                - 0.03 * self_awareness
                + rng.normal(0, 0.18)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "group_id": group_id,
                "site_id": site_id,
                "condition": condition,
                "context_type": context_type,
                "trial": t,
                "anonymity": round(anonymity, 3),
                "identifiability": round(identifiability, 3),
                "group_size": group_size,
                "crowd_immersion": round(crowd_immersion, 3),
                "self_awareness": round(self_awareness, 3),
                "accountability": round(accountability, 3),
                "group_identity_salience": round(group_identity_salience, 3),
                "personal_identity_salience": round(personal_identity_salience, 3),
                "group_norm_valence": round(group_norm_valence, 3),
                "norm_clarity": round(norm_clarity, 3),
                "norm_congruence": round(norm_congruence, 3),
                "arousal_index": round(arousal_index, 3),
                "emotional_contagion": round(emotional_contagion, 3),
                "responsibility_diffusion": round(responsibility_diffusion, 3),
                "moral_disengagement": round(moral_disengagement, 3),
                "perceived_surveillance": round(perceived_surveillance, 3),
                "moderation_visibility": round(moderation_visibility, 3),
                "behavior_score": round(behavior_score, 3),
                "prosocial_behavior": round(prosocial_behavior, 3),
                "antisocial_behavior": round(antisocial_behavior, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["log_group_size"] = np.log1p(data["group_size"])
    data["identity_shift_index"] = data["group_identity_salience"] - data["personal_identity_salience"]
    data["deindividuation_index"] = (
        data["anonymity"]
        + data["crowd_immersion"]
        + data["responsibility_diffusion"]
        + data["arousal_index"]
        - data["self_awareness"]
        - data["accountability"]
    ) / 4.0
    data["side_norm_activation"] = (
        data["anonymity"]
        * data["group_identity_salience"]
        * data["norm_clarity"]
    ) / 100.0
    data["antisocial_norm"] = (data["group_norm_valence"] < 0).astype(int)
    data["prosocial_norm"] = (data["group_norm_valence"] > 0).astype(int)
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
            mean_behavior=("behavior_score", "mean"),
            mean_prosocial=("prosocial_behavior", "mean"),
            mean_antisocial=("antisocial_behavior", "mean"),
            mean_anonymity=("anonymity", "mean"),
            mean_self_awareness=("self_awareness", "mean"),
            mean_accountability=("accountability", "mean"),
            mean_group_identity=("group_identity_salience", "mean"),
            mean_norm_congruence=("norm_congruence", "mean"),
            mean_deindividuation=("deindividuation_index", "mean"),
            mean_response_time=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    norm_summary = (
        data.assign(
            norm_band=pd.cut(
                data["group_norm_valence"],
                bins=[-5.1, -1.0, 1.0, 5.1],
                labels=["antisocial_norm", "neutral_norm", "prosocial_norm"]
            )
        )
        .groupby(["condition", "norm_band"], observed=True)
        .agg(
            n=("participant", "size"),
            mean_norm_congruence=("norm_congruence", "mean"),
            mean_prosocial=("prosocial_behavior", "mean"),
            mean_antisocial=("antisocial_behavior", "mean"),
            mean_deindividuation=("deindividuation_index", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_context.csv", index=False)
    norm_summary.to_csv(outputs / "summary_by_condition_norm_valence.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "norm_congruence_model": "norm_congruence ~ anonymity * group_identity_salience * group_norm_valence + self_awareness + accountability + norm_clarity + crowd_immersion + perceived_surveillance + moderation_visibility + condition + context_type",
        "prosocial_model": "prosocial_behavior ~ anonymity * group_identity_salience * group_norm_valence + norm_congruence + self_awareness + accountability + moral_disengagement + moderation_visibility + condition + context_type",
        "antisocial_model": "antisocial_behavior ~ anonymity * group_identity_salience * group_norm_valence + norm_congruence + responsibility_diffusion + moral_disengagement + accountability + moderation_visibility + self_awareness + condition + context_type",
        "deindividuation_index_model": "deindividuation_index ~ anonymity + identifiability + log_group_size + crowd_immersion + group_identity_salience + personal_identity_salience + accountability + moderation_visibility + condition + context_type",
        "response_time_model": "log_response_time ~ deindividuation_index + norm_clarity + arousal_index + self_awareness + accountability + condition + context_type",
    }

    model_text = []
    coefficient_frames = []

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


def simulate_side(outputs: Path, n_cases: int = 8000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    for condition in ["identified", "anonymous_prosocial_norm", "anonymous_antisocial_norm", "moderated_platform"]:
        for _ in range(n_cases):
            anonymity = {"identified": 1.5, "anonymous_prosocial_norm": 8.5, "anonymous_antisocial_norm": 8.5, "moderated_platform": 6.0}[condition] + rng.normal(0, 0.8)
            group_identity = {"identified": 3.0, "anonymous_prosocial_norm": 8.0, "anonymous_antisocial_norm": 8.0, "moderated_platform": 7.0}[condition] + rng.normal(0, 0.8)
            norm_valence = {"identified": 0.0, "anonymous_prosocial_norm": 4.0, "anonymous_antisocial_norm": -4.0, "moderated_platform": 3.0}[condition] + rng.normal(0, 0.8)
            accountability = {"identified": 8.0, "anonymous_prosocial_norm": 3.0, "anonymous_antisocial_norm": 2.0, "moderated_platform": 7.0}[condition] + rng.normal(0, 0.8)
            self_awareness = {"identified": 8.0, "anonymous_prosocial_norm": 3.2, "anonymous_antisocial_norm": 3.0, "moderated_platform": 5.0}[condition] + rng.normal(0, 0.8)
            norm_clarity = {"identified": 3.0, "anonymous_prosocial_norm": 8.0, "anonymous_antisocial_norm": 8.0, "moderated_platform": 8.0}[condition] + rng.normal(0, 0.8)
            lambda_group = logistic(-2.0 + 0.32 * anonymity + 0.30 * group_identity + 0.18 * norm_clarity - 0.20 * accountability)
            norm_congruence = np.clip(2.0 + 7.0 * lambda_group + rng.normal(0, 0.9), 0, 10)
            prosocial = np.clip(40 + 7 * max(norm_valence, 0) + 2.5 * norm_congruence * (norm_valence > 0) + 1.0 * accountability + rng.normal(0, 6), 0, 100)
            antisocial = np.clip(20 + 8 * max(-norm_valence, 0) + 2.8 * norm_congruence * (norm_valence < 0) - 1.3 * accountability - 0.9 * self_awareness + rng.normal(0, 6), 0, 100)

            rows.append({
                "condition": condition,
                "anonymity": anonymity,
                "group_identity_salience": group_identity,
                "group_norm_valence": norm_valence,
                "accountability": accountability,
                "self_awareness": self_awareness,
                "norm_clarity": norm_clarity,
                "lambda_group": lambda_group,
                "norm_congruence": norm_congruence,
                "prosocial_behavior": prosocial,
                "antisocial_behavior": antisocial,
            })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby("condition")
        .agg(
            n=("condition", "size"),
            mean_lambda_group=("lambda_group", "mean"),
            mean_norm_congruence=("norm_congruence", "mean"),
            mean_prosocial=("prosocial_behavior", "mean"),
            mean_antisocial=("antisocial_behavior", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "side_simulation.csv", index=False)
    summary.to_csv(outputs / "side_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/deindividuation_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=420)
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
        default_input = Path("data/deindividuation_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_side(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
