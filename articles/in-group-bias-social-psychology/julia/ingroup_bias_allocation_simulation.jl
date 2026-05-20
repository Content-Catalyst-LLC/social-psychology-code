#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function run_simulation(; n=5000, seed=42, output_path="../outputs/julia_ingroup_bias_allocation.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n, 9)

    for i in 1:n
        ingroup_target = rand(rng) < 0.5 ? 1 : 0
        identity_salience = 10.0 * rand(rng)
        threat = 10.0 * rand(rng)
        norm_strength = 10.0 * rand(rng)
        fairness_norm = 10.0 * rand(rng)

        bias_force = ingroup_target * (0.30 * identity_salience + 0.25 * threat + 0.20 * norm_strength)
        allocation = clamp(50.0 + 5.0 * bias_force - 1.5 * fairness_norm + 6.0 * randn(rng), 0.0, 100.0)
        trust = clamp(5.0 + 0.55 * bias_force - 0.15 * fairness_norm + randn(rng), 0.0, 10.0)
        blame = clamp(5.0 - 0.45 * bias_force + 0.18 * threat + randn(rng), 0.0, 10.0)

        rows[i, :] = [i, ingroup_target, identity_salience, threat, norm_strength, fairness_norm, allocation, trust, blame]
    end

    header = ["case_id" "ingroup_target" "identity_salience" "perceived_threat" "norm_strength" "fairness_norm" "resource_allocation" "trust_rating" "moral_blame"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("In-group bias allocation simulation complete: %d cases\n", n)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
