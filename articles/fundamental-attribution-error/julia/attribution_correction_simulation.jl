#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function run_simulation(; n=3000, trials=10, seed=42, output_path="../outputs/julia_attribution_correction.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n * trials, 10)
    row = 1

    for i in 1:n
        individualism = 10.0 * rand(rng)
        structural_awareness = 10.0 * rand(rng)

        for t in 1:trials
            constraint = 10.0 * rand(rng)
            load = 10.0 * rand(rng)
            accountability = 10.0 * rand(rng)
            perspective = 10.0 * rand(rng)

            perceived_constraint = clamp(constraint - 0.30 * load + 0.30 * accountability + 0.25 * perspective + 0.15 * structural_awareness, 0.0, 10.0)
            disposition = clamp(5.0 + 0.35 * load + 0.25 * individualism - 0.30 * perceived_constraint - 0.20 * accountability, 0.0, 10.0)
            situation = clamp(3.0 + 0.50 * perceived_constraint + 0.25 * accountability + 0.25 * perspective - 0.20 * load, 0.0, 10.0)
            fae = disposition - situation

            rows[row, :] = [i, t, constraint, perceived_constraint, load, accountability, perspective, disposition, situation, fae]
            row += 1
        end
    end

    header = ["participant" "trial" "actual_constraint" "perceived_constraint" "cognitive_load" "accountability" "perspective_taking" "dispositional_attribution" "situational_attribution" "fae_score"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Attribution correction simulation complete: %d participants, %d trials\n", n, trials)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
