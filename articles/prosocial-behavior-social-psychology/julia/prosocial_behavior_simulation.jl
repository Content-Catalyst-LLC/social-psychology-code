#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_public_goods_prosocial_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    conditions = ["weak_norm_low_trust", "strong_norm_high_trust", "high_efficacy", "low_legitimacy", "shared_identity"]

    for condition in conditions
        for i in 1:cases
            empathy = 6.0 + randn(rng) * 0.8
            norms = condition == "weak_norm_low_trust" ? 3.0 : condition == "strong_norm_high_trust" ? 8.5 : condition == "high_efficacy" ? 7.0 : condition == "low_legitimacy" ? 5.0 : 7.0
            efficacy = condition == "high_efficacy" ? 9.0 : condition == "low_legitimacy" ? 5.0 : 7.0
            trust = condition == "weak_norm_low_trust" ? 3.0 : condition == "strong_norm_high_trust" ? 8.0 : condition == "low_legitimacy" ? 3.0 : 6.5
            legitimacy = condition == "weak_norm_low_trust" ? 3.0 : condition == "strong_norm_high_trust" ? 8.0 : condition == "low_legitimacy" ? 2.5 : 7.0
            identity = condition == "shared_identity" ? 8.5 : 5.0
            cost = 4.0

            latent = -4.0 + 0.20*empathy + 0.35*norms + 0.38*efficacy + 0.25*trust + 0.30*legitimacy + 0.22*identity - 0.35*cost
            prob = logistic(latent)
            helping = rand(rng) < prob ? 1 : 0
            contribution = clamp(8 + 8*helping + 3.0*norms + 3.2*efficacy + 2.4*trust + 2.8*legitimacy + 2.0*identity - 2.0*cost + randn(rng)*7.0, 0.0, 100.0)

            push!(rows, [condition, empathy, norms, efficacy, trust, legitimacy, identity, cost, prob, helping, contribution])
        end
    end

    header = ["condition" "empathy_score" "norm_salience" "efficacy_belief" "trust_level" "institutional_legitimacy" "identity_overlap" "helping_cost" "helping_probability" "helping_decision" "cooperation_contribution"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Public-goods prosocial simulation complete. Output: %s\n", output_path)
end

run_simulation()
