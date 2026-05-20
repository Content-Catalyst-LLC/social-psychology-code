#!/usr/bin/env python3
"""
Contact hypothesis research model.

This script can:
1. Generate synthetic intergroup-contact data.
2. Estimate prejudice-change models, anxiety/empathy/trust models,
   social-distance models, response-time models, and contact-condition summaries.
3. Simulate network diffusion of inclusive norms through cross-group contact.
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
    "control", "equal_status", "common_goals", "cooperation",
    "institutional_support", "optimal_contact", "negative_contact",
    "indirect_contact", "extended_contact"
]
TARGET_GROUPS = ["outgroup_a", "outgroup_b", "outgroup_c", "outgroup_d", "outgroup_e"]
GROUP_STATUS = ["dominant", "marginalized", "mixed", "other"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 500, waves: int = 3, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"equal": 0.0, "goals": 0.0, "coop": 0.0, "support": 0.0, "quality": 0.0, "negative": 0.0, "indirect": 0.0},
        "equal_status": {"equal": 2.8, "goals": 0.3, "coop": 0.3, "support": 0.4, "quality": 0.9, "negative": -0.2, "indirect": 0.2},
        "common_goals": {"equal": 0.5, "goals": 3.0, "coop": 0.8, "support": 0.4, "quality": 1.0, "negative": -0.2, "indirect": 0.2},
        "cooperation": {"equal": 0.5, "goals": 0.9, "coop": 3.1, "support": 0.4, "quality": 1.2, "negative": -0.3, "indirect": 0.2},
        "institutional_support": {"equal": 0.5, "goals": 0.5, "coop": 0.5, "support": 3.0, "quality": 1.0, "negative": -0.2, "indirect": 0.2},
        "optimal_contact": {"equal": 2.6, "goals": 2.8, "coop": 2.9, "support": 2.8, "quality": 2.3, "negative": -0.8, "indirect": 0.4},
        "negative_contact": {"equal": -1.8, "goals": -1.4, "coop": -1.6, "support": -1.4, "quality": -2.4, "negative": 3.6, "indirect": -0.3},
        "indirect_contact": {"equal": 0.2, "goals": 0.2, "coop": 0.2, "support": 0.3, "quality": 0.6, "negative": -0.1, "indirect": 3.0},
        "extended_contact": {"equal": 0.3, "goals": 0.3, "coop": 0.3, "support": 0.5, "quality": 0.7, "negative": -0.1, "indirect": 3.4},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        site_id = f"S{rng.integers(1, 26):02d}"
        target_group = rng.choice(TARGET_GROUPS)
        group_status = rng.choice(GROUP_STATUS, p=[0.44, 0.34, 0.16, 0.06])
        prejudice_trait = rng.normal(0, 0.75)
        anxiety_trait = rng.normal(0, 0.65)
        empathy_trait = rng.normal(0, 0.65)
        initial_prejudice = float(np.clip(rng.normal(6.0 + prejudice_trait, 1.0), 0, 10))

        for wave in range(1, waves + 1):
            condition = rng.choice(CONDITIONS)
            ce = condition_effects[condition]

            contact_frequency = float(np.clip(rng.normal(3.2 + 0.55 * wave + 0.5 * (condition in ["optimal_contact", "cooperation", "common_goals"]) + 0.3 * ce["indirect"], 1.2), 0, 10))
            equal_status = float(np.clip(rng.normal(4.0 + ce["equal"], 1.0), 0, 10))
            common_goals = float(np.clip(rng.normal(4.0 + ce["goals"], 1.0), 0, 10))
            cooperation = float(np.clip(rng.normal(4.0 + ce["coop"], 1.0), 0, 10))
            institutional_support = float(np.clip(rng.normal(4.0 + ce["support"], 1.0), 0, 10))
            voluntariness = float(np.clip(rng.normal(5.4 + 0.4 * ce["quality"] - 0.2 * ce["negative"], 1.0), 0, 10))
            negative_contact = float(np.clip(rng.normal(2.0 + ce["negative"], 1.0), 0, 10))
            indirect_contact = float(np.clip(rng.normal(2.0 + ce["indirect"], 1.0), 0, 10))

            allport_quality = np.mean([equal_status, common_goals, cooperation, institutional_support, voluntariness])
            contact_quality = float(np.clip(rng.normal(0.55 * allport_quality + 0.30 * contact_frequency + ce["quality"] - 0.45 * negative_contact, 0.85), 0, 10))

            intergroup_anxiety = float(np.clip(
                rng.normal(6.2 + anxiety_trait - 0.30 * contact_quality - 0.18 * contact_frequency + 0.45 * negative_contact - 0.10 * indirect_contact, 1.0),
                0, 10
            ))
            empathy = float(np.clip(
                rng.normal(3.6 + empathy_trait + 0.30 * contact_quality + 0.12 * contact_frequency + 0.12 * indirect_contact - 0.20 * negative_contact, 0.9),
                0, 10
            ))
            perspective_taking = float(np.clip(
                rng.normal(3.8 + 0.25 * contact_quality + 0.18 * common_goals + 0.14 * cooperation - 0.15 * negative_contact, 0.9),
                0, 10
            ))
            trust = float(np.clip(
                rng.normal(3.4 + 0.26 * contact_quality + 0.16 * equal_status + 0.14 * institutional_support - 0.28 * negative_contact - 0.20 * intergroup_anxiety, 0.9),
                0, 10
            ))
            perceived_threat = float(np.clip(
                rng.normal(6.0 + 0.30 * intergroup_anxiety + 0.30 * negative_contact - 0.20 * trust - 0.12 * empathy, 1.0),
                0, 10
            ))

            prejudice_pre = float(np.clip(initial_prejudice - 0.20 * (wave - 1) + rng.normal(0, 0.4), 0, 10))
            prejudice_reduction = (
                0.12 * contact_frequency
                + 0.18 * contact_quality
                + 0.08 * equal_status
                + 0.07 * common_goals
                + 0.08 * cooperation
                + 0.07 * institutional_support
                + 0.12 * empathy
                + 0.10 * perspective_taking
                + 0.10 * trust
                + 0.08 * indirect_contact
                - 0.20 * negative_contact
                - 0.13 * intergroup_anxiety
                - 0.10 * perceived_threat
                + rng.normal(0, 0.45)
            )
            prejudice_post = float(np.clip(prejudice_pre - prejudice_reduction, 0, 10))
            stereotype_endorsement = float(np.clip(rng.normal(0.65 * prejudice_post + 0.15 * perceived_threat - 0.15 * empathy + 1.0, 0.8), 0, 10))
            future_contact_willingness = float(np.clip(rng.normal(3.0 + 0.35 * contact_quality + 0.18 * empathy + 0.16 * trust - 0.22 * intergroup_anxiety - 0.20 * negative_contact, 0.9), 0, 10))
            social_distance = float(np.clip(rng.normal(6.2 + 0.25 * prejudice_post + 0.20 * perceived_threat - 0.20 * trust - 0.15 * empathy, 0.9), 0, 10))
            inclusive_norm_perception = float(np.clip(rng.normal(3.8 + 0.24 * institutional_support + 0.18 * contact_quality + 0.10 * cooperation - 0.12 * negative_contact, 0.9), 0, 10))

            response_time_ms = int(np.clip(np.exp(
                math.log(1100)
                + 0.04 * intergroup_anxiety
                + 0.03 * perceived_threat
                - 0.03 * contact_quality
                - 0.03 * trust
                + 0.08 * (abs(prejudice_post - 5.0) < 0.75)
                + rng.normal(0, 0.16)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "site_id": site_id,
                "condition": condition,
                "wave": wave,
                "target_group": target_group,
                "group_status": group_status,
                "contact_frequency": round(contact_frequency, 3),
                "contact_quality": round(contact_quality, 3),
                "equal_status": round(equal_status, 3),
                "common_goals": round(common_goals, 3),
                "cooperation": round(cooperation, 3),
                "institutional_support": round(institutional_support, 3),
                "voluntariness": round(voluntariness, 3),
                "negative_contact": round(negative_contact, 3),
                "indirect_contact": round(indirect_contact, 3),
                "intergroup_anxiety": round(intergroup_anxiety, 3),
                "empathy": round(empathy, 3),
                "perspective_taking": round(perspective_taking, 3),
                "trust": round(trust, 3),
                "perceived_threat": round(perceived_threat, 3),
                "prejudice_pre": round(prejudice_pre, 3),
                "prejudice_post": round(prejudice_post, 3),
                "stereotype_endorsement": round(stereotype_endorsement, 3),
                "future_contact_willingness": round(future_contact_willingness, 3),
                "social_distance": round(social_distance, 3),
                "inclusive_norm_perception": round(inclusive_norm_perception, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    data = df.copy()
    data["prejudice_change"] = data["prejudice_post"] - data["prejudice_pre"]
    data["allport_quality"] = data[["equal_status", "common_goals", "cooperation", "institutional_support", "voluntariness"]].mean(axis=1)

    condition_summary = (
        data.groupby("condition")
        .agg(
            n=("prejudice_post", "size"),
            participants=("participant", "nunique"),
            sites=("site_id", "nunique"),
            mean_contact_frequency=("contact_frequency", "mean"),
            mean_contact_quality=("contact_quality", "mean"),
            mean_allport_quality=("allport_quality", "mean"),
            mean_negative_contact=("negative_contact", "mean"),
            mean_indirect_contact=("indirect_contact", "mean"),
            mean_anxiety=("intergroup_anxiety", "mean"),
            mean_empathy=("empathy", "mean"),
            mean_trust=("trust", "mean"),
            mean_prejudice_pre=("prejudice_pre", "mean"),
            mean_prejudice_post=("prejudice_post", "mean"),
            mean_prejudice_change=("prejudice_change", "mean"),
            mean_social_distance=("social_distance", "mean"),
            mean_future_contact=("future_contact_willingness", "mean"),
        )
        .reset_index()
    )

    group_status_summary = (
        data.groupby(["group_status", "condition"])
        .agg(
            n=("prejudice_post", "size"),
            mean_prejudice_change=("prejudice_change", "mean"),
            mean_anxiety=("intergroup_anxiety", "mean"),
            mean_empathy=("empathy", "mean"),
            mean_trust=("trust", "mean"),
            mean_negative_contact=("negative_contact", "mean"),
        )
        .reset_index()
    )

    condition_summary.to_csv(outputs / "summary_by_condition.csv", index=False)
    group_status_summary.to_csv(outputs / "summary_by_group_status_condition.csv", index=False)


def simulate_contact_network(outputs: Path, n: int = 240, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    if NETWORKX_AVAILABLE:
        graph = nx.watts_strogatz_graph(n=n, k=6, p=0.10, seed=seed)
        edges = list(graph.edges())
    else:
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.025:
                    edges.append((i, j))

    group = rng.integers(0, 2, n)
    prejudice = rng.uniform(4.5, 8.5, n)
    trust = rng.uniform(2.0, 5.5, n)
    inclusive_norm = rng.uniform(2.0, 5.5, n)

    history = []
    for step in range(1, 16):
        delta_prejudice = np.zeros(n)
        delta_trust = np.zeros(n)
        cross_group_ties = np.zeros(n)
        for a, b in edges:
            if group[a] != group[b]:
                cross_group_ties[a] += 1
                cross_group_ties[b] += 1
                quality = rng.uniform(0.2, 1.0)
                delta_prejudice[a] -= 0.03 * quality * inclusive_norm[a]
                delta_prejudice[b] -= 0.03 * quality * inclusive_norm[b]
                delta_trust[a] += 0.04 * quality
                delta_trust[b] += 0.04 * quality

        prejudice = np.clip(prejudice + delta_prejudice + rng.normal(0, 0.04, n), 0, 10)
        trust = np.clip(trust + delta_trust, 0, 10)
        inclusive_norm = np.clip(inclusive_norm + 0.02 * cross_group_ties, 0, 10)

        history.append({
            "step": step,
            "mean_prejudice": float(prejudice.mean()),
            "mean_trust": float(trust.mean()),
            "mean_inclusive_norm": float(inclusive_norm.mean()),
            "mean_cross_group_ties": float(cross_group_ties.mean()),
        })

    node_df = pd.DataFrame({
        "node": np.arange(n),
        "group": group,
        "final_prejudice": prejudice,
        "final_trust": trust,
        "final_inclusive_norm": inclusive_norm,
    })
    edge_df = pd.DataFrame(edges, columns=["source", "target"])
    history_df = pd.DataFrame(history)

    node_df.to_csv(outputs / "contact_network_nodes.csv", index=False)
    edge_df.to_csv(outputs / "contact_network_edges.csv", index=False)
    history_df.to_csv(outputs / "contact_network_history.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    data = df.copy()
    data["prejudice_change"] = data["prejudice_post"] - data["prejudice_pre"]
    data["allport_quality"] = data[["equal_status", "common_goals", "cooperation", "institutional_support", "voluntariness"]].mean(axis=1)
    data["log_response_time"] = np.log(data["response_time_ms"])

    model_text = []

    prejudice_model = smf.ols(
        "prejudice_post ~ prejudice_pre + condition + group_status + contact_frequency + contact_quality + "
        "allport_quality + negative_contact + indirect_contact + intergroup_anxiety + empathy + "
        "perspective_taking + trust + perceived_threat",
        data=data,
    ).fit(cov_type="cluster", cov_kwds={"groups": data["participant"]})
    model_text.append("\n\n=== Post-contact prejudice model ===\n")
    model_text.append(str(prejudice_model.summary()))

    change_model = smf.ols(
        "prejudice_change ~ condition + group_status + contact_frequency + contact_quality + allport_quality + "
        "negative_contact + indirect_contact + intergroup_anxiety + empathy + trust + perceived_threat",
        data=data,
    ).fit(cov_type="cluster", cov_kwds={"groups": data["participant"]})
    model_text.append("\n\n=== Prejudice-change model ===\n")
    model_text.append(str(change_model.summary()))

    anxiety_model = smf.ols(
        "intergroup_anxiety ~ condition + contact_frequency + contact_quality + allport_quality + "
        "negative_contact + indirect_contact + group_status",
        data=data,
    ).fit(cov_type="cluster", cov_kwds={"groups": data["participant"]})
    model_text.append("\n\n=== Intergroup anxiety model ===\n")
    model_text.append(str(anxiety_model.summary()))

    empathy_model = smf.ols(
        "empathy ~ condition + contact_frequency + contact_quality + allport_quality + "
        "negative_contact + indirect_contact + group_status",
        data=data,
    ).fit(cov_type="cluster", cov_kwds={"groups": data["participant"]})
    model_text.append("\n\n=== Empathy model ===\n")
    model_text.append(str(empathy_model.summary()))

    social_distance_model = smf.ols(
        "social_distance ~ prejudice_post + contact_quality + negative_contact + intergroup_anxiety + "
        "empathy + trust + perceived_threat + group_status",
        data=data,
    ).fit(cov_type="cluster", cov_kwds={"groups": data["participant"]})
    model_text.append("\n\n=== Social-distance model ===\n")
    model_text.append(str(social_distance_model.summary()))

    rt_model = smf.ols(
        "log_response_time ~ condition + contact_quality + negative_contact + intergroup_anxiety + "
        "empathy + trust + prejudice_post + perceived_threat",
        data=data[data["response_time_ms"] >= 150],
    ).fit(cov_type="cluster", cov_kwds={"groups": data[data["response_time_ms"] >= 150]["participant"]})
    model_text.append("\n\n=== Response-time model ===\n")
    model_text.append(str(rt_model.summary()))

    with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(model_text))

    pd.DataFrame({"term": prejudice_model.params.index, "prejudice_post_coef": prejudice_model.params.values, "prejudice_post_se": prejudice_model.bse.values}).to_csv(outputs / "prejudice_model_coefficients.csv", index=False)
    pd.DataFrame({"term": change_model.params.index, "prejudice_change_coef": change_model.params.values, "prejudice_change_se": change_model.bse.values}).to_csv(outputs / "prejudice_change_model_coefficients.csv", index=False)
    pd.DataFrame({"term": anxiety_model.params.index, "anxiety_coef": anxiety_model.params.values, "anxiety_se": anxiety_model.bse.values}).to_csv(outputs / "anxiety_model_coefficients.csv", index=False)
    pd.DataFrame({"term": empathy_model.params.index, "empathy_coef": empathy_model.params.values, "empathy_se": empathy_model.bse.values}).to_csv(outputs / "empathy_model_coefficients.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/contact_hypothesis_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=500)
    parser.add_argument("--waves", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.simulate:
        df = generate_dataset(n_participants=args.participants, waves=args.waves, seed=args.seed)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote simulated dataset: {args.output}")
    elif args.input:
        df = pd.read_csv(args.input)
    else:
        default_input = Path("data/contact_hypothesis_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_contact_network(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and network outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
