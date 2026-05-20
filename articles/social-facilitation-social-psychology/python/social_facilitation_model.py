#!/usr/bin/env python3
"""
Social facilitation research model.

This script can:
1. Generate synthetic social facilitation data.
2. Estimate performance, accuracy, error, arousal, distraction, and response-time models.
3. Test audience-by-task difficulty and audience-by-mastery interactions.
4. Simulate drive-theory, evaluation-apprehension, distraction-conflict, and digital monitoring dynamics.
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
    "alone", "audience", "coaction", "evaluation", "non_evaluative_presence",
    "digital_monitoring", "supportive_audience", "critical_audience"
]

TASK_DOMAINS = ["motor", "cognitive", "verbal", "perceptual", "sport", "workplace", "digital"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 360, trials_per_participant: int = 8, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    effects: Dict[str, Dict[str, float]] = {
        "alone": {"aud": 0, "co": 0, "eval": 0.4, "expert": 0, "size": 0, "valence": 0, "monitor": 0},
        "audience": {"aud": 1, "co": 0, "eval": 5.0, "expert": 4, "size": 4, "valence": 0.5, "monitor": 0},
        "coaction": {"aud": 0, "co": 1, "eval": 3.8, "expert": 2, "size": 2, "valence": 0.3, "monitor": 0},
        "evaluation": {"aud": 1, "co": 0, "eval": 8.0, "expert": 8, "size": 3, "valence": -0.5, "monitor": 0},
        "non_evaluative_presence": {"aud": 1, "co": 0, "eval": 1.5, "expert": 1, "size": 2, "valence": 0, "monitor": 0},
        "digital_monitoring": {"aud": 0, "co": 0, "eval": 7.0, "expert": 5, "size": 0, "valence": 0, "monitor": 1},
        "supportive_audience": {"aud": 1, "co": 0, "eval": 5.5, "expert": 5, "size": 8, "valence": 3.5, "monitor": 0},
        "critical_audience": {"aud": 1, "co": 0, "eval": 8.5, "expert": 7, "size": 8, "valence": -3.5, "monitor": 0},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 31):02d}"
        session_id = f"SE{p:04d}"
        baseline_skill = float(np.clip(rng.normal(5.8, 1.5), 0, 10))
        social_anxiety = float(np.clip(rng.normal(4.5, 1.7), 0, 10))

        for t in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            task_domain = rng.choice(TASK_DOMAINS)
            e = effects[condition]

            task_difficulty = float(np.clip(rng.normal(5.0, 2.2), 0, 10))
            task_mastery = float(np.clip(
                baseline_skill
                + rng.normal(0, 1.4)
                - 0.25 * task_difficulty
                + 0.35 * (task_domain in ["motor", "sport", "workplace"]),
                0, 10
            ))

            dominant_response_correct_prob = logistic(-1.2 + 0.45 * task_mastery - 0.40 * task_difficulty + 0.25 * baseline_skill)
            dominant_response_correct = int(rng.random() < dominant_response_correct_prob)

            audience_present = int(e["aud"])
            coaction_present = int(e["co"])
            digital_monitoring = int(e["monitor"])
            audience_size = int(max(0, round(rng.normal(e["size"], 1.2)))) if e["size"] > 0 else 0
            audience_valence = float(np.clip(rng.normal(e["valence"], 0.8), -5, 5))
            observer_expertise = float(np.clip(rng.normal(e["expert"], 1.0), 0, 10))
            evaluation_pressure = float(np.clip(
                rng.normal(
                    e["eval"]
                    + 0.25 * observer_expertise
                    + 0.35 * digital_monitoring
                    + 0.20 * social_anxiety
                    - 0.15 * max(audience_valence, 0),
                    1.0
                ),
                0, 10
            ))

            perceived_scrutiny = float(np.clip(
                rng.normal(
                    0.65 * evaluation_pressure
                    + 0.25 * audience_present * max(audience_size, 1)
                    + 0.45 * digital_monitoring
                    + 0.22 * social_anxiety,
                    1.0
                ),
                0, 10
            ))

            arousal_index = float(np.clip(
                rng.normal(
                    2.5
                    + 0.40 * audience_present
                    + 0.35 * coaction_present
                    + 0.48 * evaluation_pressure
                    + 0.22 * digital_monitoring
                    + 0.16 * social_anxiety,
                    1.0
                ),
                0, 10
            ))

            distraction_index = float(np.clip(
                rng.normal(
                    1.2
                    + 0.20 * audience_present
                    + 0.28 * coaction_present
                    + 0.45 * perceived_scrutiny
                    + 0.25 * max(-audience_valence, 0)
                    + 0.16 * digital_monitoring,
                    1.0
                ),
                0, 10
            ))

            attentional_conflict = float(np.clip(
                rng.normal(
                    0.50 * distraction_index
                    + 0.25 * task_difficulty
                    + 0.20 * perceived_scrutiny
                    - 0.10 * task_mastery,
                    1.0
                ),
                0, 10
            ))

            social_presence_intensity = audience_present + 0.65 * coaction_present + 0.50 * digital_monitoring
            mastery_advantage = task_mastery - task_difficulty

            facilitation_component = 1.9 * social_presence_intensity * arousal_index * (dominant_response_correct == 1) / 10.0
            inhibition_component = 2.2 * social_presence_intensity * arousal_index * (dominant_response_correct == 0) / 10.0
            distraction_penalty = 1.4 * attentional_conflict * max(task_difficulty - task_mastery, 0) / 10.0
            valence_component = 0.8 * audience_valence * social_presence_intensity

            performance_score = float(np.clip(
                55
                + 3.5 * baseline_skill
                + 2.5 * task_mastery
                - 2.2 * task_difficulty
                + facilitation_component
                - inhibition_component
                - distraction_penalty
                + valence_component
                + rng.normal(0, 5.0),
                0, 100
            ))

            accuracy = float(np.clip(logistic(-2.0 + 0.07 * performance_score + 0.12 * task_mastery - 0.10 * task_difficulty), 0, 1))
            error_rate = float(np.clip(1 - accuracy + rng.normal(0, 0.02), 0, 1))

            response_time_ms = int(np.clip(np.exp(
                math.log(850)
                + 0.06 * task_difficulty
                + 0.05 * attentional_conflict
                - 0.04 * task_mastery
                + 0.02 * perceived_scrutiny
                + rng.normal(0, 0.18)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "session_id": session_id,
                "site_id": site_id,
                "condition": condition,
                "task_domain": task_domain,
                "trial": t,
                "audience_present": audience_present,
                "coaction_present": coaction_present,
                "evaluation_pressure": round(evaluation_pressure, 3),
                "observer_expertise": round(observer_expertise, 3),
                "audience_size": audience_size,
                "audience_valence": round(audience_valence, 3),
                "task_difficulty": round(task_difficulty, 3),
                "task_mastery": round(task_mastery, 3),
                "dominant_response_correct": dominant_response_correct,
                "baseline_skill": round(baseline_skill, 3),
                "arousal_index": round(arousal_index, 3),
                "distraction_index": round(distraction_index, 3),
                "attentional_conflict": round(attentional_conflict, 3),
                "perceived_scrutiny": round(perceived_scrutiny, 3),
                "performance_score": round(performance_score, 3),
                "accuracy": round(accuracy, 3),
                "error_rate": round(error_rate, 3),
                "response_time_ms": response_time_ms,
                "digital_monitoring": digital_monitoring,
                "social_anxiety": round(social_anxiety, 3),
            })

    return pd.DataFrame(rows)


def add_indices(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["social_presence_intensity"] = (
        data["audience_present"]
        + 0.65 * data["coaction_present"]
        + 0.50 * data["digital_monitoring"]
    )
    data["mastery_advantage"] = data["task_mastery"] - data["task_difficulty"]
    data["simple_or_mastered"] = (data["mastery_advantage"] >= 1.0).astype(int)
    data["complex_or_unmastered"] = (data["mastery_advantage"] < 0.0).astype(int)
    data["evaluation_apprehension_index"] = (
        data["evaluation_pressure"]
        + data["perceived_scrutiny"]
        + data["observer_expertise"]
        + data["social_anxiety"]
    ) / 4.0
    data["distraction_conflict_index"] = (
        data["distraction_index"]
        + data["attentional_conflict"]
        + data["perceived_scrutiny"]
    ) / 3.0
    data["log_response_time"] = np.log(data["response_time_ms"])
    return data


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    summary = (
        data.groupby(["condition", "task_domain"])
        .agg(
            n=("participant", "size"),
            participants=("participant", "nunique"),
            mean_performance=("performance_score", "mean"),
            mean_accuracy=("accuracy", "mean"),
            mean_error_rate=("error_rate", "mean"),
            mean_response_time=("response_time_ms", "mean"),
            mean_arousal=("arousal_index", "mean"),
            mean_distraction=("distraction_index", "mean"),
            mean_evaluation=("evaluation_pressure", "mean"),
            mean_task_difficulty=("task_difficulty", "mean"),
            mean_task_mastery=("task_mastery", "mean"),
            mean_social_presence=("social_presence_intensity", "mean"),
        )
        .reset_index()
    )

    difficulty_summary = (
        data.assign(
            difficulty_band=pd.cut(
                data["task_difficulty"],
                bins=[-0.1, 3.33, 6.66, 10.1],
                labels=["low", "medium", "high"]
            )
        )
        .groupby(["condition", "difficulty_band"], observed=True)
        .agg(
            n=("participant", "size"),
            mean_performance=("performance_score", "mean"),
            mean_accuracy=("accuracy", "mean"),
            mean_response_time=("response_time_ms", "mean"),
            mean_arousal=("arousal_index", "mean"),
            mean_scrutiny=("perceived_scrutiny", "mean"),
        )
        .reset_index()
    )

    summary.to_csv(outputs / "summary_by_condition_domain.csv", index=False)
    difficulty_summary.to_csv(outputs / "summary_by_condition_difficulty.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = add_indices(df)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    formulas = {
        "performance_model": "performance_score ~ social_presence_intensity * task_difficulty + social_presence_intensity * task_mastery + evaluation_pressure + perceived_scrutiny + arousal_index + distraction_conflict_index + dominant_response_correct + baseline_skill + audience_valence + condition + task_domain",
        "accuracy_model": "accuracy ~ social_presence_intensity * task_difficulty + social_presence_intensity * task_mastery + evaluation_pressure + arousal_index + attentional_conflict + dominant_response_correct + baseline_skill + condition + task_domain",
        "error_model": "error_rate ~ social_presence_intensity * task_difficulty + evaluation_pressure + arousal_index + distraction_conflict_index + dominant_response_correct + task_mastery + social_anxiety + condition + task_domain",
        "arousal_model": "arousal_index ~ audience_present + coaction_present + digital_monitoring + evaluation_pressure + perceived_scrutiny + observer_expertise + audience_size + audience_valence + social_anxiety + condition",
        "response_time_model": "log_response_time ~ social_presence_intensity * task_difficulty + task_mastery + evaluation_pressure + perceived_scrutiny + attentional_conflict + arousal_index + condition + task_domain",
    }

    model_text = []
    coefficient_frames = []

    for name, formula in formulas.items():
        model_data = data[data["response_time_ms"] >= 150] if name == "response_time_model" else data
        if name == "accuracy_model":
            model = smf.glm(formula, data=model_data, family=sm.families.Gaussian()).fit(
                cov_type="cluster", cov_kwds={"groups": model_data["participant"]}
            )
        else:
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


def simulate_drive_theory(outputs: Path, n_cases: int = 5000, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    for condition in ["alone", "mere_presence", "evaluation", "digital_monitoring"]:
        for _ in range(n_cases):
            baseline_skill = rng.uniform(0, 10)
            task_difficulty = rng.uniform(0, 10)
            task_mastery = np.clip(baseline_skill + rng.normal(0, 1.2) - 0.25 * task_difficulty, 0, 10)
            dominant_correct = int(task_mastery >= task_difficulty)
            social_presence = {"alone": 0.0, "mere_presence": 1.0, "evaluation": 1.4, "digital_monitoring": 1.1}[condition]
            evaluation_pressure = {"alone": 0.3, "mere_presence": 2.0, "evaluation": 8.0, "digital_monitoring": 7.0}[condition]
            arousal = np.clip(2.0 + 0.8 * social_presence + 0.55 * evaluation_pressure + rng.normal(0, 0.9), 0, 10)
            performance = np.clip(
                55
                + 3.0 * baseline_skill
                + 2.0 * task_mastery
                - 2.0 * task_difficulty
                + 2.0 * arousal * dominant_correct
                - 2.2 * arousal * (1 - dominant_correct)
                + rng.normal(0, 5),
                0, 100
            )
            rows.append({
                "condition": condition,
                "baseline_skill": baseline_skill,
                "task_difficulty": task_difficulty,
                "task_mastery": task_mastery,
                "dominant_response_correct": dominant_correct,
                "social_presence": social_presence,
                "evaluation_pressure": evaluation_pressure,
                "arousal": arousal,
                "performance": performance,
            })

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.assign(
            difficulty_band=pd.cut(simulation["task_difficulty"], [-0.1, 3.33, 6.66, 10.1], labels=["low", "medium", "high"])
        )
        .groupby(["condition", "difficulty_band"], observed=True)
        .agg(
            n=("performance", "size"),
            mean_performance=("performance", "mean"),
            mean_arousal=("arousal", "mean"),
            dominant_correct_rate=("dominant_response_correct", "mean"),
        )
        .reset_index()
    )

    simulation.to_csv(outputs / "drive_theory_simulation.csv", index=False)
    summary.to_csv(outputs / "drive_theory_simulation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/social_facilitation_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=360)
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
        default_input = Path("data/social_facilitation_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_drive_theory(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and simulation outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
