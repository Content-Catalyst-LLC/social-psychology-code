#!/usr/bin/env python3
"""
Collective action and social change research model.

This script can:
1. Generate synthetic collective-action trial data.
2. Estimate participation models, intention models, digital/offline engagement models,
   response-time models, and institutional-response summaries.
3. Simulate network diffusion and threshold mobilization.
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
    "control", "identity_prime", "injustice_prime", "efficacy_prime",
    "network_mobilization", "high_cost", "repression_risk",
    "digital_mobilization", "offline_mobilization"
]
DOMAINS = ["labor", "civil_rights", "climate", "gender_justice", "racial_justice", "housing", "health", "education", "democracy", "community"]
RECRUITMENT = ["none", "friend", "organization", "workplace", "school", "religious", "digital_platform", "media", "family"]
RESPONSES = ["none", "symbolic", "negotiation", "concession", "reform", "repression", "cooptation", "backlash"]


def logistic(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def generate_dataset(n_participants: int = 450, trials_per_participant: int = 4, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    condition_effects: Dict[str, Dict[str, float]] = {
        "control": {"identity": 0.0, "injustice": 0.0, "efficacy": 0.0, "network": 0.0, "cost": 0.0, "risk": 0.0, "digital": 0.0, "offline": 0.0},
        "identity_prime": {"identity": 1.8, "injustice": 0.4, "efficacy": 0.3, "network": 0.4, "cost": 0.0, "risk": 0.0, "digital": 0.2, "offline": 0.2},
        "injustice_prime": {"identity": 0.6, "injustice": 2.2, "efficacy": 0.2, "network": 0.2, "cost": 0.0, "risk": 0.0, "digital": 0.2, "offline": 0.2},
        "efficacy_prime": {"identity": 0.4, "injustice": 0.4, "efficacy": 2.3, "network": 0.5, "cost": -0.2, "risk": 0.0, "digital": 0.4, "offline": 0.5},
        "network_mobilization": {"identity": 0.8, "injustice": 0.5, "efficacy": 0.7, "network": 2.4, "cost": -0.2, "risk": 0.0, "digital": 1.2, "offline": 0.8},
        "high_cost": {"identity": 0.3, "injustice": 0.6, "efficacy": -0.3, "network": 0.1, "cost": 2.8, "risk": 0.8, "digital": -0.2, "offline": -1.0},
        "repression_risk": {"identity": 0.6, "injustice": 1.0, "efficacy": -0.4, "network": 0.2, "cost": 1.2, "risk": 3.0, "digital": -0.4, "offline": -1.3},
        "digital_mobilization": {"identity": 0.5, "injustice": 0.6, "efficacy": 0.5, "network": 1.6, "cost": -0.6, "risk": -0.2, "digital": 2.7, "offline": 0.3},
        "offline_mobilization": {"identity": 1.0, "injustice": 0.8, "efficacy": 0.8, "network": 1.5, "cost": 0.4, "risk": 0.4, "digital": 0.6, "offline": 2.6},
    }

    for p in range(1, n_participants + 1):
        participant = f"P{p:04d}"
        group_id = f"G{rng.integers(1, 31):02d}"
        activism_trait = rng.normal(0, 0.55)
        risk_tolerance = rng.normal(0, 0.45)
        baseline_identity = rng.normal(5.6, 1.2)
        baseline_efficacy = rng.normal(5.0, 1.2)
        baseline_trust = rng.normal(5.0, 1.0)

        for trial in range(1, trials_per_participant + 1):
            condition = rng.choice(CONDITIONS)
            domain = rng.choice(DOMAINS)
            ce = condition_effects[condition]

            identity_strength = float(np.clip(baseline_identity + ce["identity"] + 0.35 * activism_trait + rng.normal(0, 0.9), 0, 10))
            perceived_injustice = float(np.clip(rng.normal(5.8 + ce["injustice"] + 0.30 * identity_strength + 0.20 * activism_trait, 1.1), 0, 10))
            moral_outrage = float(np.clip(rng.normal(0.55 * perceived_injustice + 0.28 * identity_strength + 0.35 * ce["injustice"], 1.0), 0, 10))
            collective_efficacy = float(np.clip(baseline_efficacy + ce["efficacy"] + 0.22 * identity_strength + 0.18 * ce["network"] + rng.normal(0, 0.9), 0, 10))
            network_support = float(np.clip(rng.normal(4.6 + ce["network"] + 0.30 * identity_strength + 0.20 * activism_trait, 1.2), 0, 10))
            mobilization_exposure = float(np.clip(rng.normal(3.8 + 0.65 * ce["network"] + 0.45 * ce["digital"] + 0.35 * ce["offline"] + 0.22 * network_support, 1.2), 0, 10))
            participation_cost = float(np.clip(rng.normal(4.2 + ce["cost"] + 0.18 * (domain in ["labor", "democracy", "civil_rights"]), 1.1), 0, 10))
            perceived_repression_risk = float(np.clip(rng.normal(3.4 + ce["risk"] + 0.20 * (domain in ["democracy", "labor", "racial_justice"]) - 0.20 * baseline_trust, 1.2), 0, 10))
            free_rider_incentive = float(np.clip(rng.normal(4.6 + 0.20 * participation_cost - 0.18 * identity_strength - 0.10 * moral_outrage, 1.0), 0, 10))
            perceived_legitimacy = float(np.clip(rng.normal(4.0 + 0.35 * identity_strength + 0.25 * perceived_injustice + 0.18 * moral_outrage - 0.16 * perceived_repression_risk, 1.0), 0, 10))

            intention_latent = (
                -3.2
                + 0.22 * identity_strength
                + 0.18 * perceived_injustice
                + 0.20 * moral_outrage
                + 0.20 * collective_efficacy
                + 0.16 * network_support
                + 0.12 * mobilization_exposure
                - 0.18 * participation_cost
                - 0.15 * perceived_repression_risk
                - 0.08 * free_rider_incentive
                + 0.20 * activism_trait
                + rng.normal(0, 0.35)
            )
            participation_intention = float(np.clip(logistic(intention_latent), 0, 1))

            action_latent = (
                -2.6
                + 2.2 * participation_intention
                + 0.10 * identity_strength
                + 0.09 * moral_outrage
                + 0.11 * collective_efficacy
                + 0.12 * network_support
                - 0.16 * participation_cost
                - 0.14 * perceived_repression_risk
                - 0.10 * free_rider_incentive
                + 0.18 * risk_tolerance
                + rng.normal(0, 0.35)
            )
            action_participation = int(rng.random() < logistic(action_latent))

            digital_engagement = float(np.clip(rng.normal(1.5 + 4.8 * participation_intention + ce["digital"] + 0.22 * network_support + 0.15 * mobilization_exposure - 0.10 * perceived_repression_risk, 1.2), 0, 10))
            offline_engagement = float(np.clip(rng.normal(0.8 + 4.0 * participation_intention + ce["offline"] + 0.22 * network_support - 0.20 * participation_cost - 0.20 * perceived_repression_risk, 1.2), 0, 10))

            if condition == "digital_mobilization":
                recruitment_source = "digital_platform"
            elif condition == "offline_mobilization":
                recruitment_source = rng.choice(["organization", "friend", "workplace", "school"])
            elif network_support > 6:
                recruitment_source = rng.choice(["friend", "organization", "workplace", "school", "religious", "family"])
            else:
                recruitment_source = rng.choice(RECRUITMENT)

            if action_participation and collective_efficacy > 6.5 and network_support > 6:
                institutional_response = rng.choice(["negotiation", "concession", "reform", "symbolic"], p=[0.30, 0.25, 0.25, 0.20])
            elif perceived_repression_risk > 7 or condition == "repression_risk":
                institutional_response = rng.choice(["repression", "backlash", "none", "symbolic"], p=[0.45, 0.20, 0.20, 0.15])
            elif action_participation:
                institutional_response = rng.choice(["symbolic", "negotiation", "none", "cooptation"], p=[0.40, 0.25, 0.25, 0.10])
            else:
                institutional_response = rng.choice(["none", "symbolic", "backlash"], p=[0.75, 0.15, 0.10])

            movement_outcome = float(np.clip(
                rng.normal(
                    2.0
                    + 0.25 * collective_efficacy
                    + 0.20 * network_support
                    + 0.22 * action_participation
                    + 0.25 * (institutional_response in ["concession", "reform"])
                    - 0.25 * (institutional_response in ["repression", "backlash"]),
                    1.0,
                ),
                0,
                10,
            ))

            response_time_ms = int(np.clip(np.exp(
                math.log(1200)
                - 0.05 * identity_strength
                - 0.04 * collective_efficacy
                + 0.05 * participation_cost
                + 0.04 * perceived_repression_risk
                + 0.10 * (0.45 < participation_intention < 0.55)
                + rng.normal(0, 0.18)
            ), 150, 60000))

            rows.append({
                "participant": participant,
                "group_id": group_id,
                "condition": condition,
                "trial": trial,
                "movement_domain": domain,
                "identity_strength": round(identity_strength, 3),
                "perceived_injustice": round(perceived_injustice, 3),
                "moral_outrage": round(moral_outrage, 3),
                "collective_efficacy": round(collective_efficacy, 3),
                "network_support": round(network_support, 3),
                "mobilization_exposure": round(mobilization_exposure, 3),
                "participation_cost": round(participation_cost, 3),
                "perceived_repression_risk": round(perceived_repression_risk, 3),
                "free_rider_incentive": round(free_rider_incentive, 3),
                "participation_intention": round(participation_intention, 4),
                "action_participation": action_participation,
                "digital_engagement": round(digital_engagement, 3),
                "offline_engagement": round(offline_engagement, 3),
                "recruitment_source": recruitment_source,
                "institutional_response": institutional_response,
                "perceived_legitimacy": round(perceived_legitimacy, 3),
                "movement_outcome": round(movement_outcome, 3),
                "response_time_ms": response_time_ms,
            })

    return pd.DataFrame(rows)


def summarize_data(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)

    condition_summary = (
        df.groupby("condition")
        .agg(
            n=("action_participation", "size"),
            participants=("participant", "nunique"),
            groups=("group_id", "nunique"),
            participation_rate=("action_participation", "mean"),
            mean_intention=("participation_intention", "mean"),
            mean_identity=("identity_strength", "mean"),
            mean_injustice=("perceived_injustice", "mean"),
            mean_outrage=("moral_outrage", "mean"),
            mean_efficacy=("collective_efficacy", "mean"),
            mean_network_support=("network_support", "mean"),
            mean_cost=("participation_cost", "mean"),
            mean_repression_risk=("perceived_repression_risk", "mean"),
            mean_digital_engagement=("digital_engagement", "mean"),
            mean_offline_engagement=("offline_engagement", "mean"),
            mean_outcome=("movement_outcome", "mean"),
            mean_response_time_ms=("response_time_ms", "mean"),
        )
        .reset_index()
    )

    domain_summary = (
        df.groupby("movement_domain")
        .agg(
            n=("action_participation", "size"),
            participation_rate=("action_participation", "mean"),
            mean_intention=("participation_intention", "mean"),
            mean_injustice=("perceived_injustice", "mean"),
            mean_efficacy=("collective_efficacy", "mean"),
            mean_cost=("participation_cost", "mean"),
            mean_repression_risk=("perceived_repression_risk", "mean"),
        )
        .reset_index()
    )

    response_summary = (
        df.groupby("institutional_response")
        .agg(
            n=("action_participation", "size"),
            participation_rate=("action_participation", "mean"),
            mean_efficacy=("collective_efficacy", "mean"),
            mean_outcome=("movement_outcome", "mean"),
            mean_repression_risk=("perceived_repression_risk", "mean"),
        )
        .reset_index()
    )

    condition_summary.to_csv(outputs / "summary_by_condition.csv", index=False)
    domain_summary.to_csv(outputs / "summary_by_domain.csv", index=False)
    response_summary.to_csv(outputs / "summary_by_institutional_response.csv", index=False)


def simulate_network(outputs: Path, n: int = 250, seed: int = 42) -> None:
    outputs.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    if NETWORKX_AVAILABLE:
        graph = nx.watts_strogatz_graph(n=n, k=6, p=0.12, seed=seed)
        edges = list(graph.edges())
        degree = dict(graph.degree())
    else:
        edges = []
        degree = {i: 0 for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.025:
                    edges.append((i, j))
                    degree[i] += 1
                    degree[j] += 1

    identity = rng.uniform(0, 10, n)
    injustice = rng.uniform(0, 10, n)
    efficacy = rng.uniform(0, 10, n)
    cost = rng.uniform(1, 9, n)
    threshold = rng.normal(8.5, 1.2, n)
    active = np.zeros(n, dtype=int)

    seeds = rng.choice(n, size=max(3, n // 25), replace=False)
    active[seeds] = 1

    history = []
    for step in range(1, 16):
        new_active = active.copy()
        adjacency_count = np.zeros(n)
        for a, b in edges:
            adjacency_count[a] += active[b]
            adjacency_count[b] += active[a]
        for i in range(n):
            if active[i] == 0:
                network_exposure = adjacency_count[i]
                propensity = 0.22 * identity[i] + 0.22 * injustice[i] + 0.22 * efficacy[i] + 0.55 * network_exposure - 0.20 * cost[i]
                if propensity >= threshold[i]:
                    new_active[i] = 1
        active = new_active
        history.append({
            "step": step,
            "active_count": int(active.sum()),
            "active_rate": float(active.mean()),
            "mean_degree_active": float(np.mean([degree[i] for i in range(n) if active[i] == 1])) if active.sum() > 0 else 0,
        })

    node_df = pd.DataFrame({
        "node": np.arange(n),
        "identity_strength": identity,
        "perceived_injustice": injustice,
        "collective_efficacy": efficacy,
        "participation_cost": cost,
        "threshold": threshold,
        "final_active": active,
        "degree": [degree[i] for i in range(n)],
    })
    edge_df = pd.DataFrame(edges, columns=["source", "target"])
    history_df = pd.DataFrame(history)

    node_df.to_csv(outputs / "network_nodes.csv", index=False)
    edge_df.to_csv(outputs / "network_edges.csv", index=False)
    history_df.to_csv(outputs / "network_mobilization_history.csv", index=False)


def run_models(df: pd.DataFrame, outputs: Path) -> None:
    outputs.mkdir(parents=True, exist_ok=True)

    if not STATSMODELS_AVAILABLE:
        with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
            f.write("statsmodels is not available. Install requirements.txt to run models.\n")
        return

    model_text = []
    df = df.copy()
    df["log_response_time"] = np.log(df["response_time_ms"])

    participation_model = smf.glm(
        "action_participation ~ condition + movement_domain + identity_strength + perceived_injustice + "
        "moral_outrage + collective_efficacy + network_support + mobilization_exposure + "
        "participation_cost + perceived_repression_risk + free_rider_incentive + perceived_legitimacy",
        data=df,
        family=sm.families.Binomial(),
    ).fit(cov_type="cluster", cov_kwds={"groups": df["participant"]})
    model_text.append("\n\n=== Action participation logistic model ===\n")
    model_text.append(str(participation_model.summary()))

    intention_model = smf.ols(
        "participation_intention ~ condition + movement_domain + identity_strength + perceived_injustice + "
        "moral_outrage + collective_efficacy + network_support + mobilization_exposure + "
        "participation_cost + perceived_repression_risk + free_rider_incentive",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["participant"]})
    model_text.append("\n\n=== Participation intention model ===\n")
    model_text.append(str(intention_model.summary()))

    digital_model = smf.ols(
        "digital_engagement ~ condition + movement_domain + participation_intention + identity_strength + "
        "network_support + mobilization_exposure + participation_cost + perceived_repression_risk",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["participant"]})
    model_text.append("\n\n=== Digital engagement model ===\n")
    model_text.append(str(digital_model.summary()))

    offline_model = smf.ols(
        "offline_engagement ~ condition + movement_domain + participation_intention + identity_strength + "
        "network_support + collective_efficacy + participation_cost + perceived_repression_risk",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["participant"]})
    model_text.append("\n\n=== Offline engagement model ===\n")
    model_text.append(str(offline_model.summary()))

    outcome_model = smf.ols(
        "movement_outcome ~ condition + action_participation + collective_efficacy + network_support + "
        "digital_engagement + offline_engagement + perceived_repression_risk + perceived_legitimacy",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["group_id"]})
    model_text.append("\n\n=== Movement outcome model ===\n")
    model_text.append(str(outcome_model.summary()))

    rt_model = smf.ols(
        "log_response_time ~ condition + participation_intention + identity_strength + perceived_injustice + "
        "collective_efficacy + participation_cost + perceived_repression_risk + free_rider_incentive",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["participant"]})
    model_text.append("\n\n=== Response-time model ===\n")
    model_text.append(str(rt_model.summary()))

    with open(outputs / "model_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(model_text))

    pd.DataFrame({"term": participation_model.params.index, "participation_coef": participation_model.params.values, "participation_se": participation_model.bse.values}).to_csv(outputs / "participation_model_coefficients.csv", index=False)
    pd.DataFrame({"term": intention_model.params.index, "intention_coef": intention_model.params.values, "intention_se": intention_model.bse.values}).to_csv(outputs / "intention_model_coefficients.csv", index=False)
    pd.DataFrame({"term": digital_model.params.index, "digital_coef": digital_model.params.values, "digital_se": digital_model.bse.values}).to_csv(outputs / "digital_engagement_model_coefficients.csv", index=False)
    pd.DataFrame({"term": offline_model.params.index, "offline_coef": offline_model.params.values, "offline_se": offline_model.bse.values}).to_csv(outputs / "offline_engagement_model_coefficients.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Generate synthetic data.")
    parser.add_argument("--input", type=Path, help="Input CSV for modeling.")
    parser.add_argument("--output", type=Path, default=Path("data/collective_action_trials.csv"))
    parser.add_argument("--outputs", type=Path, default=Path("outputs"))
    parser.add_argument("--participants", type=int, default=450)
    parser.add_argument("--trials", type=int, default=4)
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
        default_input = Path("data/collective_action_trials.csv")
        if default_input.exists():
            df = pd.read_csv(default_input)
        else:
            df = generate_dataset(seed=args.seed)
            default_input.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(default_input, index=False)
            print(f"No input provided. Generated default dataset: {default_input}")

    summarize_data(df, args.outputs)
    run_models(df, args.outputs)
    simulate_network(args.outputs, seed=args.seed)
    print(f"Wrote summaries, models, and network outputs to: {args.outputs}")


if __name__ == "__main__":
    main()
