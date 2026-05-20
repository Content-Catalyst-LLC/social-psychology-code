#!/usr/bin/env julia

using Random
using Statistics
using Printf
using DelimitedFiles

function run_simulation(; n=3000, days=30, seed=42, output_path="../outputs/julia_social_comparison_longitudinal.csv")
    rng = MersenneTwister(seed)
    rows = Matrix{Any}(undef, n * days, 9)
    row = 1

    self_eval = 4.5 .+ 2.5 .* rand(rng, n)
    orientation = 10.0 .* rand(rng, n)

    for day in 1:days
        for i in 1:n
            digital_exposure = rand(rng) * 10.0
            upward_gap = max(0.0, 2.0 + 0.20 * digital_exposure + randn(rng))
            attainability = clamp(5.0 - 0.25 * digital_exposure + randn(rng), 0.0, 10.0)
            inspiration = clamp(0.30 * upward_gap * attainability / 10.0 + 0.4 * randn(rng), 0.0, 10.0)
            discouragement = clamp(0.28 * upward_gap * max(0.0, 5.0 - attainability) / 5.0 + 0.4 * randn(rng), 0.0, 10.0)

            self_eval[i] = clamp(
                self_eval[i] - 0.04 * upward_gap * orientation[i] / 10.0 +
                0.05 * inspiration - 0.05 * discouragement,
                0.0, 10.0
            )

            rows[row, :] = [i, day, digital_exposure, upward_gap, attainability, inspiration, discouragement, orientation[i], self_eval[i]]
            row += 1
        end
    end

    header = ["participant" "day" "digital_exposure" "upward_gap" "attainability" "inspiration" "discouragement" "comparison_orientation" "self_eval"]
    mkpath(dirname(output_path))
    open(output_path, "w") do io
        writedlm(io, header, ",")
        writedlm(io, rows, ",")
    end

    @printf("Longitudinal social-comparison simulation complete: %d participants, %d days\n", n, days)
    @printf("Output written to: %s\n", output_path)
end

run_simulation()
