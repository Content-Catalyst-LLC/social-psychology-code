#!/usr/bin/env julia

using Random
using Printf
using DelimitedFiles

function logistic(x)
    return 1.0 / (1.0 + exp(-clamp(x, -40.0, 40.0)))
end

function run_simulation(; cases=10000, seed=42, output_path="../outputs/julia_side_simulation.csv")
    rng = MersenneTwister(seed)
    rows = Any[]
    conditions = ["identified", "anonymous_prosocial_norm", "anonymous_antisocial_norm", "moderated_platform"]

    for condition in conditions
        for i in 1:cases
            anonymity = condition == "identified" ? 1.5 : condition == "moderated_platform" ? 6.0 : 8.5
            group_identity = condition == "identified" ? 3.0 : condition == "moderated_platform" ? 7.0 : 8.0
            norm_valence = condition == "anonymous_antisocial_norm" ? -4.0 : condition == "identified" ? 0.0 : 4.0
            accountability = condition == "identified" ? 8.0 : condition == "moderated_platform" ? 7.0 : 2.5
            norm_clarity = condition == "identified" ? 3.0 : 8.0

            lambda_group = logistic(-2.0 + 0.32 * anonymity + 0.30 * group_identity + 0.18 * norm_clarity - 0.20 * accountability)
            norm_congruence = clamp(2.0 + 7.0 * lambda_group + randn(rng) * 0.9, 0.0, 10.0)
            prosocial = clamp(40.0 + 7.0 * max(norm_valence, 0.0) + 2.5 * norm_congruence * (norm_valence > 0) + accountability + randn(rng) * 6.0, 0.0, 100.0)
            antisocial = clamp(20.0 + 8.0 * max(-norm_valence, 0.0) + 2.8 * norm_congruence * (norm_valence < 0) - 1.3 * accountability + randn(rng) * 6.0, 0.0, 100.0)

            push!(rows, [condition, anonymity, group_identity, norm_valence, accountability, norm_clarity, lambda_group, norm_congruence, prosocial, antisocial])
        end
    end

    header = ["condition" "anonymity" "group_identity_salience" "group_norm_valence" "accountability" "norm_clarity" "lambda_group" "norm_congruence" "prosocial_behavior" "antisocial_behavior"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("SIDE simulation complete. Output: %s\n", output_path)
end

run_simulation()
