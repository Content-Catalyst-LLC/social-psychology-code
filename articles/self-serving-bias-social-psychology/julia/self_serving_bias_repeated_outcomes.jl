#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function run_simulation(; n=3000, trials=12, seed=42, output_path="../outputs/julia_self_serving_bias_repeated_outcomes.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n * trials, 10)
    row = 1

    for i in 1:n
        self_esteem = clamp(6.0 + randn(rng), 0.0, 10.0)
        defensiveness = randn(rng)

        for t in 1:trials
            success = rand(rng) < 0.5 ? 1 : 0
            accountability = 10.0 * rand(rng)
            evidence = 10.0 * rand(rng)
            ego_threat = clamp(2.0 + 4.0 * (1 - success) + defensiveness + randn(rng), 0.0, 10.0)

            internal_attr = clamp(
                5.0 + 1.5 * success - 1.2 * (1 - success) +
                0.25 * ego_threat * (2 * success - 1) - 0.20 * accountability + 0.15 * evidence,
                0.0, 10.0
            )
            external_attr = clamp(
                5.0 - 1.0 * success + 1.5 * (1 - success) +
                0.25 * ego_threat * (1 - success) - 0.25 * accountability,
                0.0, 10.0
            )
            learning = clamp(4.0 + 0.35 * accountability + 0.25 * evidence - 0.30 * external_attr * (1 - success), 0.0, 10.0)

            rows[row, :] = [i, t, success, self_esteem, ego_threat, accountability, evidence, internal_attr, external_attr, learning]
            row += 1
        end
    end

    header = ["participant" "trial" "success" "self_esteem" "ego_threat" "accountability" "evidence_strength" "internal_attribution" "external_attribution" "learning_intention"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Repeated self-serving attribution simulation complete: %d participants, %d trials\n", n, trials)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
